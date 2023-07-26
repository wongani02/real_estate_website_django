import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.db.models import Q 
from django.core.paginator import Paginator
from django.core.mail import EmailMessage

from payments.models import LodgeBookingPayment, PaymentOption
from verifications.views import create_lodge_listing
from bnb.forms import ReviewForm
from payments.utils import EmailThread
from users.custom_middleware import process_lodge_request

from .create_lodge import LodgeCreation as LodgeCreationClass
from .models import Amenity, LodgeImage, Lodge, Image, LodgesViews, Booking
from .forms import *
from .email_context import *
from .utils import (
    check_room_availability, 
    format_dates, 
    process_data, 
    calc_number_of_nights,
    check_user_eligibility,
    )


# Create your views here.


def lodgeListingView(request):
    lodges = Lodge.objects.prefetch_related("pictures").filter(is_active=True)
    context = {
        'lodges': lodges,
    }
    return render(request, 'lodges/lodge-listing.html', context)


def lodgeDetailView(request, pk):
    lodge = get_object_or_404(Lodge, pk=pk)

    # track user that viewed the lodge
    process_lodge_request(request, pk)

    # get user eligibility to make a review
    user = request.user
    review_form = None
    eligibility = None
    if user.is_authenticated:
        eligibility = check_user_eligibility(user, lodge)
        if eligibility:
            review_form = ReviewForm()

    # Update the number of views
    update_views(lodge)

    # get reviews
    reviews = LodgeReview.objects.filter(lodge=lodge).order_by('-created')
    review_paginator = Paginator(reviews, 2)
    review_page_number = request.GET.get('page', 1)
    review_obj = review_paginator.get_page(review_page_number)

    context = {
        'lodge': lodge,
        'reviews': review_obj,
        'review_form': review_form,
        'eligibility':eligibility,
    }

    if request.htmx:
        return render(request, 'lodges/partials/review-partial.html', context)
    
    return render(request, 'lodges/lodge-detail.html', context)


def update_views(_property):
    from datetime import datetime

    date = datetime.now().strftime('%Y-%m-%d')
    property_view, created = LodgesViews.objects.get_or_create(property=_property, date=date)

    # Update entry
    property_view.views += 1
    property_view.save()


@login_required
def createLodgeView(request):
    session =request.session
    amenities = Amenity.objects.all()
    room_form = RoomFormset()
    if 'lodge_details' in request.session:
        lodge_form = LodgeCreationForm(
            initial={
                'property_name': session['lodge_details']['property_name'],
                'role': session['lodge_details']['role'],
                'description': session['lodge_details']['description'],
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
                'role': form.cleaned_data['role'],
                'description': form.cleaned_data['description'],
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
            for form in room_form:

                room_detials = {
                    'room_type': form.cleaned_data['room_type'],
                    'max_guests': form.cleaned_data['max_guests'],
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
                'max_guests':x['max_guests'],
                'beds': x['beds'],
                'price': x['price'],
                'quantity': x['quantity'],
                } for x in session['lodge_rooms']]) 
            
        else:
            room_form = RoomCreationFormSet()

        return render(request, 'lodges/create-lodge-rooms.html', {'room_form': room_form})


@login_required
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

            return redirect('lodges:lodge-restrictions')
        else:
            print(ameneity_form.errors)
        
    else:
        ameneity_form = LodgeAmenities(request.GET)
    context = {
        'ameneity_form': ameneity_form,
    }
    return render(request, 'lodges/create-lodge-amenities.html', context) 


@login_required
def lodgeRestrictions(request):
    session = request.session
    if 'lodge_amenites' not in session:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    
    restriction_list = []
    if request.method == 'POST':
        form = LodgeRestrictionsForm(request.POST)
        if form.is_valid():
            for restriction in form.cleaned_data['restriction']:
                restriction_list.append({
                    'id': restriction.id,
                    'name': restriction.restriction
                })
            
            session['lodge_restriction'] = restriction_list
            print(session['lodge_restriction'])

            return redirect('lodges:lodge-policies')    
    else:
        form = LodgeRestrictionsForm()

    context = {
        'form':form,
    }
    return render(request, 'lodges/create-lodge-restrictions.html', context)


@login_required
def lodgePoliciesView(request):
    session = request.session
    
    if 'lodge_restriction' not in session:
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    if request.method == 'POST':
        form = LodgePolicyForm(request.POST)
        if form.is_valid():    
            print(form.cleaned_data['policy'])
            session['lodge_policies'] = form.cleaned_data['policy'].id

            return redirect('lodges:lodge-documents')    
    else:
        form = LodgePolicyForm()

    context = {
        'form': form,
    }
    return render(request, 'lodges/create-lodge-policies.html', context)


@login_required
def uploadLodgeDocumnetAndImages(request):
    session = request.session
    if 'lodge_policies' not in session:
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
            print(lodge)
            
            #create room categories
            lodge_instance.create_room_categories(rooms=session['lodge_rooms'])

            #create lodge rooms
            lodge_instance.create_rooms()

            #create lodge ameneities
            lodge_instance.assign_amenities(selected=session['lodge_amenites'])

            #create lodge restrisctions
            lodge_instance.assign_restrictions(selected=session['lodge_restriction'])

            #create lodge policy
            lodge_instance.create_cancellation_policy(policy_id=session['lodge_policies'])

            #assign images
            lodge_instance.add_images(image_id=session['img_session'])

            #delete session variables after lodge is created
            lodge_instance.clear_session()

            # create a lodge verification pending instance and send an email to the user
            create_lodge_listing(request, lodge)

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


def editLodgeRooms(request, pk):
    lodge = Lodge.objects.get(id=pk)
    room_cats = RoomCategory.objects.filter(lodge_id=lodge.id)

    context = {
        'room_cats': room_cats,
        'lodge': lodge,
    }
    return render(request, 'lodges/edit/rooms.html', context)


def editRoomCatDetails(request, room_cat):
    room = RoomCategory.objects.get(id=room_cat)
    if request.method == 'POST':
        form = LodgeRoomsEditForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('lodges:edit-rooms', room.lodge.id)
    else:
        form = LodgeRoomsEditForm(instance=room)
    context = {
        'form': form,
        'pk':room_cat
    }
    return render(request, 'lodges/edit/room-details.html', context)


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


def deleteLodgeImages(request, pk, image):

    image = Image.objects.filter(id=image).delete()

    images = images = LodgeImage.objects.filter(lodge_id=pk)


    context = {
        'images':images,
        'pk':pk,
    }
    return render(request, 'lodges/partials/lodge-images.html', context)


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

    policy = LodgeCancellationPolicy.objects.get(lodge_id=pk)

    if request.method == 'POST':
        form = LodgePolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
    else:
        form = LodgePolicyForm(instance=policy)
    context = {
        'form': form,
        'pk':pk,
    }
    return render(request, 'lodges/edit/policies.html', context)


def addLodgeRoomImages(request, room_cat, lodge):

    images = RoomCategoryImage.objects.filter(room_cat_id=room_cat)

    context = {
        'images': images,
        'pk':room_cat,
        'lodge': lodge,
    }
    return render(request, 'lodges/edit/lodge-room-images.html', context)


def handleRoomImages(request, room_cat):
    if request.method == 'POST':
        image = request.FILES.get('file')
        print(image)
        RoomCategoryImage.objects.create(
            room_cat_id=room_cat,
            image=image
        )
    
    return HttpResponse('uploaded')

def handleDeleteRoomImages(request, image_id, room_cat):

    RoomCategoryImage.objects.filter(id=image_id).delete()

    images = RoomCategoryImage.objects.filter(room_cat_id=room_cat)

    context = {
        'images':images,
        'pk':room_cat
    }
    return render(request, 'lodges/partials/room-image-list.html', context)



#services
def searchView(request):

    if request.method == 'POST':
        q = request.POST['lodge_search']

        results = Lodge.active_lodges.filter(
            Q(name__icontains=q) | Q(street_name__icontains=q) | Q(city__icontains=q) | Q(map_location__icontains=q) | Q(country__icontains=q)
            ).order_by('?').distinct()
        
    context = {
        'lodges': results
    }

    if request.htmx:
        return render(request, 'lodges/partials/search-results.html', context)

    return render(request, 'lodges/search/lodge-results.html', context)


def handleReviews(request, pk):

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            LodgeReview.objects.create(
                user_id=request.user.id,
                lodge_id=pk,
                review=form.cleaned_data['review']
            )
            return render(request, 'lodges/partials/review-posted.html')

    return render(request, 'lodges/partials/review-posted.html')


def getAvailableRoomTypes(request, lodge):

    date_range = request.POST.get('daterange')
    quantity = request.POST.get('quantity')
    request.session['date_range'] = date_range

    start_date, end_date = format_dates(date_range)

    #get lodge to check availablilty
    lodge = Lodge.objects.get(id=lodge)

    #get all room types associated with the lodge
    lodge_room_types = lodge.rooms.all()

    #initialise an empty available rooms array
    avalable_rooms = []

    #get available rooms only from each room type
    for room_type in lodge_room_types:
        
        #check availability of each room 
        for room in room_type.room_s.all():

            availability = check_room_availability(room=room.id, check_in=start_date, check_out=end_date)
            print(availability, room.id)
            # if available create a dictionary with all data
            if availability:
                
                data = {
                    'room_type_id': room_type.id,
                    'room_id': room.id,
                    'availability': availability,
                }
                
                # append the data to the list on available rooms
                avalable_rooms.append(data)

    # processed data
    processed_data = process_data(avalable_rooms)
    print(processed_data)
                
    context = {
        'lodge': lodge,
        'data': processed_data,
        'qty': int(quantity),
        
    }
    return render(request, 'lodges/partials/available-roomtypes.html', context)


def bookingDetailsView(request, **kwargs):
    session = request.session
    rooms = kwargs.get('room_list')
    session['room_list'] = rooms
    
    if request.method == 'POST':
        form = LodgeBookingForm(request.POST)
        if form.is_valid():
            request.session['lodge_booking_data'] = {
                'name': form.cleaned_data['guest_name'],
                'email': form.cleaned_data['guest_email'],
                'note': form.cleaned_data['note'],
            }
            return redirect(
                'lodges:booking-step-2', 
                kwargs.get('lodge'), 
                kwargs.get('room'), 
                kwargs.get('qty'),
                kwargs.get('room_list')
                )
    
    else:
        if 'lodge_booking_data' in request.session:
            form = LodgeBookingForm(initial={
                'guest_name': session['lodge_booking_data']['name'],
                'guest_email': session['lodge_booking_data']['email'],
                'note': session['lodge_booking_data']['note']
            })
        else:
            form = LodgeBookingForm()

    context = {
        'form': form,
        'dates': request.session['date_range'],
        'qty': kwargs.get('qty')
    }
    return render(request, 'lodges/bookings/booking-step-1.html', context)


def bookingPaymentView(request, **kwargs):
    
    room_type = RoomCategory.objects.get(id=kwargs.get('room'))

    room_price = room_type.price_per_night

    date_range = request.session['date_range']

    check_in, check_out = format_dates(date_range)

    num_nights = calc_number_of_nights(check_in=check_in, check_out=check_out)

    qty = kwargs.get('qty')

    total_price = (room_price*num_nights)*qty

    context = {
        'guest': request.session['lodge_booking_data'],
        'total_price': total_price,
        'num_nights': num_nights,
        'check_in': check_in,
        'check_out': check_out,
        'num_rooms': qty,
        'room_type': room_type,
        'room_list': kwargs.get('room_list'),
    }
    return render(request, 'lodges/bookings/booking-step-2.html', context)


@login_required
def processPaymentView(request, **kwargs):
    lodge = Lodge.objects.get(id=kwargs.get('lodge'))
    date_range = request.session['date_range']
    check_in, check_out = format_dates(date_range)
    num_nights = calc_number_of_nights(check_in=check_in, check_out=check_out)
    booking_ids = []
    number_of_rooms = kwargs.get('qty')
    rooms_available = kwargs.get('room_list')
    print(type(rooms_available), rooms_available)
    
    number_of_bookings = 0
    if number_of_rooms > rooms_available:
        number_of_bookings = rooms_available
    else:
        number_of_bookings = number_of_rooms

    room_cat = RoomCategory.objects.get(id=kwargs.get('room'))
    rooms = room_cat.room_s.all()
    
    rooms_to_be_booked = []

    for room in rooms:
        availability = check_room_availability(room=room.id, check_in=check_in, check_out=check_out) 
        if availability:
            rooms_to_be_booked.append(room.id)
            print(rooms_to_be_booked)

    count = 0

    # Make sure to only delete your session variables at the end of the function
    # Im also using them for some of my code 
    while count < number_of_bookings:
        booking_instance = Booking.objects.create(
            user_id=request.user.id,
            room_id=rooms_to_be_booked[count],
            lodge=lodge,
            email=request.session['lodge_booking_data']['email'],
            full_name=request.session['lodge_booking_data']['name'],
            check_in=check_in, 
            check_out=check_out,
            number_of_nights=num_nights,
            number_of_rooms=number_of_rooms,
            note=request.session['lodge_booking_data']['note'],
        )
        booking_ids.append(booking_instance.id)
        print(count, number_of_bookings)
        count += 1

    body = json.loads(request.body)
    
    payment = LodgeBookingPayment.objects.create(
        user_id=request.user.id,
        lodge_id=lodge.id,
        full_name=body['fullname'],
        email=body['email'],
        total_paid=body['totalPaid'],
        order_key=body['orderId'],
        payment_option=PaymentOption.objects.first(),
        billing_status=True,
    )
    payment_id = payment.order_key

    for booking in booking_ids:
        payment.booking.add(booking)

    booking = Booking.objects.filter(id__in=booking_ids)
    booking.update(is_paid=True)

    # Add payment id to session variable "lodge_booking"
    request.session['lodge_booking'] = payment.order_key

    # Add email to session
    request.session['booking_email'] = request.session['lodge_booking_data']['email']

    return JsonResponse('payment complete', safe=False)


# bookmarks
def bookmarkLodge(request, pk):

    lodge = get_object_or_404(Lodge, pk=pk)

    if request.user.is_authenticated:
        lodge.user_bookmark.add(request.user)
        subject = 'Your Lodge Has Been Bookmarked!'
        message = bookmarked_lodge_email.format(
            lodge.user.username,
            lodge.name,
            lodge.map_location,
            lodge.id,
        )
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [lodge.user.email])

        EmailThread(email).start()
        messages.success(request, f'lodge "{lodge.name}" has been added bookmarks')
    else:
        messages.error(request, f'Please login to bookmark this property')
        return render(request, 'lodges/partials/bookmark-removed.html', {'lodge':lodge})

    return render(request, 'lodges/partials/lodge-bookmarked.html', {'lodge':lodge})


def removeBookmark(request, pk):

    lodge = get_object_or_404(Lodge, pk=pk)
    if request.user.is_authenticated:
        lodge.user_bookmark.remove(request.user)
        messages.info(request, f'lodge "{lodge.name}" has been removed bookmarks')
    else:
        messages.error(request, f'Please login to bookmark this property')

    return render(request, 'lodges/partials/bookmark-removed.html', {'lodge': lodge})


