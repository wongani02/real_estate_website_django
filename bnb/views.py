from django.shortcuts import render, redirect
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q 
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from lodges.forms import RequiredFormSet

from bnb.models import *
from bnb.create_bnb import BNB
from bnb.forms import *


class BnbList(generic.ListView):
    model = Property
    paginate_by = 9
    template_name = 'bnb/bnb-listing.html'

    def get_context_data(self, **kwargs):
        context = super(BnbList, self).get_context_data(**kwargs)
        qs = Property.objects.all()
        context = {
            'bnbs': qs, 'bnb_count': qs.count(),
        }
        return context
    

class BnbDetail(generic.DetailView):
    model = Property
    template_name = 'bnb/bnb-detail.html'

    def get(self, request, **kwargs):
        qs = Property.objects.get(id=kwargs.get('pk'))
        imgs = PropertyImage.objects.filter(property=kwargs.get('pk'))
        context = {
            'property': qs, 'images': imgs
        }

        return render(request, self.template_name, context)


class SimpleSearch(generic.ListView):
    template_name = 'bnb/bnb-listing-v2.html'
    paginate_by = 12

    def post(self, request):
        qs = Property.objects.filter(
            Q(property_type__id__iexact=request.POST.get('bnb_type')) | 
            Q(city__id__iexact=request.POST.get('district'))
        ).order_by('created_at').distinct()

        # Set up a 12 object pagination with all properties
        p = Paginator(qs, 12)

        # Get current page number
        page = self.request.GET.get('page')

        # Save data to property variable
        results = p.get_page(page)

        context = ({
            'results': results, 'count': qs.count()
        })

        return render(request, self.template_name, context)

#Bnb creation views

@login_required
def bnbDetailsView(request):
    session = request.session

    if request.method == 'POST':
        form = BNBDetailsForm(request.POST)
        if form.is_valid():
            request.session['bnb_details'] = {
                'property_name': form.cleaned_data['property_name'],
                'street_name': form.cleaned_data['street_name'],
                'city': form.cleaned_data['city'],
                'description': form.cleaned_data['description'],
                'location': form.cleaned_data['location'],
                'contact_email':form.cleaned_data['contact_email'],
                'contact_number': form.cleaned_data['contact_number'],
                'number_of_rooms': form.cleaned_data['number_of_rooms'],
                'bnb_type': form.cleaned_data['bnb_type'].id,
                'price_per_night': form.cleaned_data['price_per_night'],
            }
            print(session['bnb_details'])
            return redirect('bnb:bnb-location')
        else:
            print(form.errors)
    else:
        
        if 'bnb_details' in session:
            form = BNBDetailsForm(
                initial={
                    'property_name': session['bnb_details']['property_name'],
                    'street_name': session['bnb_details']['street_name'],
                    'city': session['bnb_details']['city'],
                    'description': session['bnb_details']['description'],
                    'location': session['bnb_details']['location'],
                    'contact_email':session['bnb_details']['contact_email'],
                    'contact_number': session['bnb_details']['contact_number'],
                    'number_of_rooms': session['bnb_details']['number_of_rooms'],
                    'bnb_type': session['bnb_details']['bnb_type'],
                    'price_per_night': session['bnb_details']['price_per_night'],
                }
            )
        else:
            form = BNBDetailsForm()
    context = {
        'form': form,
    }
    return render(request, 'bnb/create/bnb-details-creation.html', context)


@login_required
def bnbRoomCreateView(request):
    rooms = []
    session = request.session

    if 'bnb_details' not in session:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    num_of_rooms = 0
    if 'bnb_details' in session:
        num_of_rooms = session['bnb_details']['number_of_rooms']
        print(num_of_rooms)
    else:
        redirect ('bnb:bnb-details-create')

    #Room creation formset
    RoomCreationFormSet = formset_factory(
        form=BNBRoomCreationForm, 
        formset=RequiredFormSet, 
        extra=int(num_of_rooms),
        max_num=int(num_of_rooms),
    )
    
    #post handler
    if request.method == 'POST':
        room_form = RoomCreationFormSet(request.POST)
        
        if room_form.is_valid():
            for form in room_form:

                room_detials = {
                    'adults': form.cleaned_data['adults'],
                    'beds': form.cleaned_data['beds'],
                    'baths': form.cleaned_data['baths'],
                }

                rooms.append(room_detials)

            request.session['bnb_rooms'] = rooms
            print(request.session['bnb_rooms'])
            return redirect('bnb:bnb-amenities-add')
        else:
            # print(room_form.errors)
            #display error pop up message
            return HttpResponseRedirect(request.META["HTTP_REFERER"])    
        
    else:
        if 'bnb_rooms' in session:
            room_form = RoomCreationFormSet(initial=[{
                'baths': x['baths'],
                'adults':x['adults'],
                'beds': x['beds'],
                } for x in session['bnb_rooms']]) 
            
        else:
            room_form = RoomCreationFormSet()
    context = {
        'room_form': room_form,
    }
    return render(request, 'bnb/create/bnb-rooms.html', context)


@login_required
def bnbLocationView(request):
    session = request.session

    if 'bnb_details' not in session:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    if request.method == 'POST':
        form = BNBLocationForm(request.POST)
        if form.is_valid():
            request.session['bnb_location_details'] = {
                'map_location': form.cleaned_data['map_location'],
                'lat': form.cleaned_data['lat'],
                'long': form.cleaned_data['long'],
            }
            # print(session['bnb_location_details'])
            return redirect('bnb:bnb-room')
    else:
        if 'bnb_location_details' in request.session:
            form = BNBLocationForm(
                initial={
                    'map_location': session['bnb_location_details']['map_location'],
                    'lat': session['bnb_location_details']['lat'],
                    'long': session['bnb_location_details']['long'],
                }
            )
        else:
            form = BNBLocationForm()

    context = {
        'form': form,
    }
    return render(request, 'bnb/create/bnb-location.html', context)


@login_required
def bnbAmenitiesView(request):
    session = request.session
    if 'bnb_location_details' not in session:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    amenity_list = []
    if request.method == 'POST':
        form = BnBAmenitiesForm(request.POST)
        if form.is_valid():
            for amenity in form.cleaned_data['amenity']:
                amenity_list.append({
                    'id': amenity.id,
                    'name': amenity.name
                })
            # print(amenity_list)
            session['bnb_amenites'] = amenity_list

            return redirect('bnb:bnb-images-add')    
    else:
        form = BnBAmenitiesForm()

    context = {
        'form': form,
    }
    return render(request, 'bnb/create/bnb-amenities.html', context)


@login_required
def bnbImagesView(request):
    session = request.session

    if 'bnb_amenites' not in session:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    uploaded_images = None
    if 'bnb_img_session' in session:
        uploaded_images = BNBImage.objects.filter(id__in=session['bnb_img_session'])

    context = {
        'uploaded_images': uploaded_images,
    }
    return render(request, 'bnb/create/bnb-images.html', context)


@login_required
def bnbImageHandler(request):
    if request.method == 'POST':
        image = request.FILES.get('file')
        print(str(image))
        # initialise BNB class to store image id's
        bnb = BNB(request)

        # store uploaded images in the database
        bnb.save_images(image=image)

        # del request.session['img_session']
    
    return HttpResponse('upload')


@login_required
def createBNBInstance(request):
    session = request.session

    if 'bnb_img_session' not in session:
        # display pop up message
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    
    if len(session['bnb_img_session']) == 0:
        # display pop up message
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    
    try:
        with transaction.atomic():
            bnb = BNB(request)

            #create bnb instance
            instance = bnb.create_bnb(
                user=request.user.id,
                bnb=session['bnb_details'], 
                location=session['bnb_location_details']
                )
            
            #create bnb rooms
            bnb.create_rooms(rooms=session['bnb_rooms'])
            
            #assign amenities
            bnb.assign_ameneities(selected=session['bnb_amenites'])

            #append images
            bnb.assign_images(image_id=session['bnb_img_session'])

            #clear sessions
            bnb.clear_session()

            return redirect('bnb:bnb-detail', instance)
    except:
        # return redirect('bnb:error-page')
        return redirect('bnb:bnb-details-create')


    

