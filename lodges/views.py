from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.db.models import Q 
from django.core.paginator import Paginator

from .create_lodge import LodgeCreation as LodgeCreationClass
from .models import Amenity, LodgeImage, Lodge, Image
from .forms import *

# Create your views here.


def lodgeListingView(request):
    lodges = Lodge.objects.prefetch_related("pictures").filter(is_active=True)
    context = {
        'lodges': lodges,
    }
    return render(request, 'lodges/lodge-listing.html', context)


def lodgeDetailView(request, pk):
    lodge = get_object_or_404(Lodge, pk=pk)
    context = {
        'lodge': lodge,
    }
    return render(request, 'lodges/lodge-detail.html', context)


@login_required
def createLodgeView(request):
    session =request.session
    amenities = Amenity.objects.all()
    room_form = RoomFormset()
    if 'lodge_details' in request.session:
        lodge_form = LodgeCreationForm(
            initial={
                'property_name': session['lodge_details']['property_name'],
                'address': session['lodge_details']['address'],
                'city': session['lodge_details']['city'],
                'description': session['lodge_details']['description'],
                'location': session['lodge_details']['location'],
                'contact_email':session['lodge_details']['contact_email'],
                'contact_number': session['lodge_details']['contact_number'],
                'number_of_room_types': session['lodge_details']['number_of_room_types'],
            }
        )
    else:
        lodge_form = LodgeCreationForm()
    
    context = {
        'amenities':amenities,
        'room_form': room_form,
        'lodge_form': lodge_form,
    }
    return render(request, 'lodges/create-lodges.html', context)


@login_required
@require_POST
def handleLodge(request):
    if request.method == 'POST':
        form = LodgeCreationForm(request.POST)
        if form.is_valid():
            request.session['lodge_details'] = {
                'property_name': form.cleaned_data['property_name'],
                'address': form.cleaned_data['address'],
                'city': form.cleaned_data['city'],
                'description': form.cleaned_data['description'],
                'location': form.cleaned_data['location'],
                'contact_email':form.cleaned_data['contact_email'],
                'contact_number': form.cleaned_data['contact_number'],
                'number_of_room_types': form.cleaned_data['number_of_room_types'],
            }
        print(request.session['lodge_details'])
        return redirect('lodges:lodge-location')
    else:
        form = LodgeCreationForm()
        return render(request, 'lodges/create-lodges.html', {'form':form})


@login_required
def createLodgeLocation(request):
    session = request.session

    if 'lodge_details' not in session:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    if request.method == 'POST':
        form = MapLocationDetails(request.POST)
        if form.is_valid():
            request.session['lodge_location_details'] = {
                'map_location': form.cleaned_data['map_location'],
                'lat': form.cleaned_data['lat'],
                'long': form.cleaned_data['long'],
            }
            print(session['lodge_location_details'])
            return redirect('lodges:room-form-handler')
    else:
        if 'lodge_location_details' in request.session:
            form = MapLocationDetails(
                initial={
                    'map_location': session['lodge_location_details']['map_location'],
                    'lat': session['lodge_location_details']['lat'],
                    'long': session['lodge_location_details']['long'],
                }
            )
        else:
            form = MapLocationDetails()

    context = {
        'form': form,
    }
    return render(request, 'lodges/create-lodge-location.html', context)


@login_required
def handleRoomForm(request):
    rooms = []
    session = request.session

    if 'lodge_location_details' not in session:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    num_of_categories = 0
    if 'lodge_details' in session:
        num_of_categories = session['lodge_details']['number_of_room_types']
    else:
        redirect ('lodges:create-lodge')

    #Room creation formset
    RoomCreationFormSet = formset_factory(
        form=RoomCreationForm, 
        formset=RequiredFormSet, 
        extra=int(num_of_categories),
        max_num=int(num_of_categories),
    )
    
    #post handler
    if request.method == 'POST':
        room_form = RoomCreationFormSet(request.POST)
        
        if room_form.is_valid():
            print('passing')
            for form in room_form:

                room_detials = {
                    'room_type': form.cleaned_data['room_type'],
                    'adults': form.cleaned_data['adults'],
                    'children': form.cleaned_data['children'],
                    'beds': form.cleaned_data['beds'],
                    'price': form.cleaned_data['price'],
                    'quantity': form.cleaned_data['quantity'],
                }

                rooms.append(room_detials)
        else:
            # print(room_form.errors)
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
                
        request.session['lodge_rooms'] = rooms
        print(request.session['lodge_rooms'])
        return redirect('lodges:amenties-handler')
    else:
        if 'lodge_rooms' in session:
            room_form = RoomCreationFormSet(initial=[{
                'room_type': x['room_type'],
                'adults':x['adults'],
                'children': x['children'],
                'beds': x['beds'],
                'price': x['price'],
                'quantity': x['quantity'],
                } for x in session['lodge_rooms']]) 
            
        else:
            room_form = RoomCreationFormSet()

        return render(request, 'lodges/create-lodge-rooms.html', {'room_form': room_form})


def handleAmenities(request):
    session = request.session
    if 'lodge_rooms' not in session:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    
    amenity_list = []
    
    if request.method == 'POST':
        ameneity_form = LodgeAmenities(request.POST)
        if ameneity_form.is_valid():
            
            for amenity in ameneity_form.cleaned_data['amenity']:
                amenity_list.append({
                    'id': amenity.id,
                    'name': amenity.name
                })
            print(amenity_list)
            session['lodge_amenites'] = amenity_list

            return redirect('lodges:lodge-documents')
        else:
            print(ameneity_form.errors)
        
    else:
        ameneity_form = LodgeAmenities(request.GET)
    context = {
        'ameneity_form': ameneity_form,
    }
    return render(request, 'lodges/create-lodge-amenities.html', context) 


@login_required
def uploadLodgeDocumnetAndImages(request):
    session = request.session
    if 'lodge_amenites' not in session:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    uploaded_images = None
    if 'img_session' in session:
        uploaded_images = Image.objects.filter(id__in=session['img_session'])

    context = {
        'uploaded_images': uploaded_images,
    }
    return render(request, 'lodges/create-lodge-documents.html', context)


@login_required
def fileUploadView(request):
    
    if request.method == 'POST':
        image = request.FILES.get('file')

        #initialise lodge class to store image id's
        lodge_images = LodgeCreationClass(request)

        #store uploaded images in the database
        lodge_images.save_image(image=image)

        # del request.session['img_session']
    
    return HttpResponse('upload')


@login_required
@transaction.atomic
def createLodgeInstanceView(request):
    session = request.session

    with transaction.atomic():

        try: 
            #initialize lodge creation class
            lodge_instance = LodgeCreationClass(request)

            #create lodge
            lodge = lodge_instance.create_lodge(
                lodge=session['lodge_details'],
                location=session['lodge_location_details'],
                user_id=request.user.id
                )
            
            #create room categories
            lodge_instance.create_room_categories(rooms=session['lodge_rooms'])

            #create lodge rooms
            lodge_instance.create_rooms()

            #create lodge ameneities
            lodge_instance.assign_amenities(selected=session['lodge_amenites'])

            #assign images
            lodge_instance.add_images(image_id=session['img_session'])

            #delete session variables after lodge is created
            lodge_instance.clear_session()

            return redirect('lodges:lodge-detail', lodge)

        except:
            pass
            # return redirect('lodges:error-page')

    return redirect('lodges:create-lodge')


####### edit views ####### 

def editLodgeOptions(request, pk):
    context = {
        'pk':pk
    }
    return render(request, 'lodges/edit/index.html', context)


def editLodgeDetails(request, pk):

    lodge = Lodge.objects.get(id=pk)

    if request.method == 'POST':
        form = LodgeDetailsEditForm(request.POST, instance=lodge)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated sucessfully')
            return redirect('lodges:edit-details', pk)
    else:
        form= LodgeDetailsEditForm(instance=lodge)

    context = {
        'form': form,
        'pk':pk,
    }
    return render(request, 'lodges/edit/details.html', context)


def editLodgeLocation(request, pk):
    lodge = Lodge.objects.get(id=pk)

    if request.method == 'POST':
        form = LodgeLocationEditView(request.POST, instance=lodge)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated sucessfully')
            return redirect('lodges:edit-location', pk)
    else:
        form = LodgeLocationEditView(instance=lodge)

    context = {
        'form': form,
        'pk':pk,
    }
    return render(request, 'lodges/edit/location.html', context)


#not complete
def editLodgeRooms(request, pk):
    lodge = Lodge.objects.get(id=pk)
    rooms = Room.objects.filter(lodge_id=pk)

    RoomEditFormSet = modelformset_factory(
        form=LodgeRoomsEditForm, 
        formset=RequiredFormSet, 
        extra=lodge.number_of_room_types,
        max_num=lodge.number_of_room_types,
        model=Room
    )

    if request.method == 'POST':
        room_edit_form = RoomEditFormSet(request.POST)
        if room_edit_form.is_valid():

            for form in room_edit_form:
                pass
                
            messages.success(request, 'Edit successful!!!')
            return redirect('lodges:edit-rooms', pk)
    else:
        room_edit_form = RoomEditFormSet(initial=[{
            'room_type': i.room_type,
            'adults': i.adults,
            'beds': i.beds,
            'children': i.children,
            'price_per_night': i.price_per_night
        } for i in rooms])

    context = {
        'room_form': room_edit_form,
        'pk': pk,
    }
    return render(request, 'lodges/edit/rooms.html', context)


def editLodgeImages(request, pk):
    images = LodgeImage.objects.filter(lodge_id=pk)

    if request.method == 'POST':
        image = request.FILES.get('file')
        instance = Image.objects.create(image=image)

        LodgeImage.objects.create(
            lodge_id=pk,
            image_id=instance.id
        )
    
    context = {
        'images': images,
        'pk': pk,
    }
    return render(request, 'lodges/edit/images.html', context)


def editLodgeAmenities(request, pk):
    lodge = Lodge.objects.get(id=pk)
    amenites = LodgeAmenity.objects.get(lodge=lodge)

    if request.method =='POST':
        form = LodgeAmenities(request.POST, instance=amenites)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit successful!!!')
            return redirect('lodges:edit-amenities', pk)

    else:
        form = LodgeAmenities(instance=amenites)

    context = {
        'form': form,
        'pk': pk,
    }
    return render(request, 'lodges/edit/amenities.html', context)


def editLodgePolicies(request, pk):
    context = {

    }
    return render(request, 'lodges/edit/policies.html', context)


#services
def searchView(request):

    if request.method == 'POST':
        q = request.POST['lodge_search']

        results = Lodge.objects.filter(
            Q(name__icontains=q) | Q(street_name__icontains=q) | Q(city__icontains=q) | Q(map_location__icontains=q) | Q(country__icontains=q)
            ).filter(is_active=True).order_by('?').distinct()
        
    # print(results)
    # lodge_paginator = Paginator(results, 2)
    # lodge_page_number = request.GET.get('page', 1)
    # lodge_obj = lodge_paginator.get_page(lodge_page_number)

    context = {
        'lodges': results
    }

    if request.htmx:
        return render(request, 'lodges/partials/search-results.html', context)

    return render(request, 'lodges/search/lodge-results.html', context)


def bookingDetailsView(request, lodge, room):

    context = {

    }

    return render(request, 'lodges/bookings/booking-step-1.html', context)
