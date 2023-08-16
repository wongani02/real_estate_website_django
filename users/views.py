from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.utils.html import strip_tags
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse

from bnb.models import Property as BNBProperty, BnbViews, Booking as BnbBooking
from lodges.models import Lodge, About, LodgesViews, Booking as LodgeBooking
from properties.models import Property, PropetyViews, Receipt
from properties.charts import all_property_views_chart
from payments.utils import EmailThread
from payments.models import PropertyPayment, BnbBookingPayment, LodgeBookingPayment
from core import settings

from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, UserProfileForm
from .helpers import auth_user_should_not_access

import json

# Create your views here.

User = get_user_model()


def contextLoginForm(request):
    login_form = UserLoginForm()
    return {'login_form': login_form}

def contextRegisterForm(request):
    register_form = UserRegistrationForm()
    return {'register_form': register_form}


@auth_user_should_not_access
def loginView(request):
    login_form = UserLoginForm()
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                print(user)
                login(request, user)
                messages.info(request, 'Login successful')
                return redirect('accounts:dashboard')
            else:
                message = 'Invalid Credentials!'
                messages.error(request, message)
                return redirect('accounts:login')
    context = {
        'login_form': login_form
    }
    return render(request, 'users/auth-page.html', context)

@auth_user_should_not_access
def RegisterView(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            user = register_form.save(commit=False)
            user.email = email
            if register_form.cleaned_data['user_type'] == 'Realtor':
                user.is_realtor = True
            else:
                user.is_customer = True
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            auth = authenticate(email=email, password=register_form.cleaned_data['password'])
            if auth is not None:
                if regMail(request, email):
                    login(request, auth)
                    return redirect('accounts:dashboard')
                messages.success(request, 'Account created successfully')
            return redirect('accounts:login')
        else: 
            print(register_form.errors)
        
    else :
        register_form = UserRegistrationForm()
    
    context = {
        'register_form':register_form,
    }
    return render(request, 'users/auth-page.html', context)

def regMail(request, email):
    # Get company object
    company = About.objects.first()

    # Get current site
    current_site = get_current_site(request)

    # Create emails subject
    subject = "Welcome to " + company.company_name

    # Create context variables
    context = {
         'company': company.company_name, 'company_addr': company.address,
         'company_tel': company.phone_number, 'user': email, 'current_site': current_site,
         'support': 'support@afrihuts.com'
    }

    # Create email body
    email_body = render_to_string('users/users-email.html', context)
    plain_text = strip_tags(email_body)

    # Create email sender
    from_email = settings.EMAIL_HOST_USER

    # Create email recepient
    to_email = email

    # Create email object
    email = EmailMultiAlternatives(subject, plain_text, from_email, [to_email])

    # Attach email html image to email
    email.attach_alternative(email_body, 'text/html')

    # Send email via thread
    EmailThread(email).start()

    return True



def logoutView(request):
    logout(request)
    return redirect('properties:home')


def forgotPassword(request):
    context = {

    }
    return render(request, 'users/', context)


#dasboard views
@login_required(login_url='accounts:login')
def dashboardView(request):
    # Get total number of properties, bnbs and lodges owned by user
    no_properties = Property.objects.filter(agent__username=request.user.username).count()
    no_lodges = Lodge.objects.filter(user__username=request.user.username).count()
    no_bnbs = BNBProperty.objects.filter(host__username=request.user.username).count()

    # Get view data for all listings
    data, count = get_view_data(request)

    context = {
        'properties': no_properties, 'bnbs': no_bnbs, 'lodges': no_lodges,
        'views': json.dumps(data), 'listing_views': count
    }
    return render(request, 'users/page-dashboard.html', context)

def get_view_data(request):
    # Empty list to hold legends
    view_data = []

    # variable to hold count data
    count = []

    # get lodges, bnbs, and properties owned by user
    lodges = Lodge.objects.filter(user__username=request.user.username)
    bnbs = BNBProperty.objects.filter(host__username=request.user.username)
    properties = Property.objects.filter(agent__username=request.user.username)

    # append listing names to legend list
    listing_names = [lodge.name for lodge in lodges] + [bnb.title for bnb in bnbs] + [property.name for property in properties]

    # append names to nested list
    view_data.append(listing_names)

    # get count data
    lodge_count = [LodgesViews.objects.filter(property=lodge).aggregate(total_views=Sum('views'))['total_views'] for lodge in lodges]
    bnb_count = [BnbViews.objects.filter(property=bnb).aggregate(total_views=Sum('views'))['total_views'] for bnb in bnbs]
    property_count = [PropetyViews.objects.filter(property=_property).aggregate(total_views=Sum('views'))['total_views'] for _property in properties]

    # append count data to nested list in order of listing names
    view_data.append(lodge_count)
    view_data.append(bnb_count)
    view_data.append(property_count)

    # aggregate counts
    count = lodge_count + bnb_count + property_count

    # assign initial index value of zero to avoid an error
    if len(count) == 0:
        count.append("0")

    return view_data, count[0]



@login_required(login_url='accounts:login')
def profileView(request):

    if request.method == "POST":
        u_form = UserUpdateForm(instance=request.user, data=request.POST)
        p_form = UserProfileForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            print('valid')
        else:
            print('error updating form', u_form.errors, p_form.errors)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/page-dashboard-profile.html', context)


@login_required(login_url='accounts:login')
def bookmarksView(request):
    user = get_object_or_404(User, id=request.user.id)
    q = Property.objects.filter(user_bookmark=user)
    context = {
        'bookmarks': q
    }
    return render(request, 'users/page-dashboard-favorites.html', context)


@login_required(login_url='accounts:login')
def myPropertiesView(request):
    user_id = request.user.id
    #properties
    properties = Property.objects.filter(agent_id=user_id)

    #bnbs 
    bnb = BNBProperty.objects.filter(host_id=user_id)

    #lodges
    lodge = Lodge.objects.filter(user_id=user_id)

    context = {
        'properties': properties,
        'bnb': bnb,
        'lodges': lodge,
    }
    return render(request, 'users/page-dashboard-property.html', context)


@login_required(login_url='accounts:login')
def bookingsView(request, **kwargs):
    # get all booking data
    bnb_data, lodge_data = get_booking_data(request)
    bnb_bookings, lodge_bookings = get_booked_listings(request)

    context = {
        'bnb_data': bnb_data, 'lodge_data': lodge_data,
        'bnb_bookings': bnb_bookings, 'lodge_bookings': lodge_bookings,
        'choice': kwargs.get('booking')
    }
    # print(context)
    return render(request, 'users/page-dashboard-bookings.html', context)

@login_required(login_url='accounts:login')
def financesView(request, **kwargs):
    # get finances data
    finances = get_user_payments(request)

    # get receipts
    receipts = get_user_receipts(request)

    context = {
        'choice': kwargs.get('finances'),
        'finances': finances, 'receipts': receipts
    }

    # print(context)

    return render(request, 'users/page-dashboard-payments.html', context)


@login_required(login_url='accounts:login')
def addPropertyView(request):
    context = {

    }
    return render(request, 'users/', context)


@login_required(login_url='accounts:login')
def notificationsView(request):
    context = {

    }
    return render(request, 'users/page-dashboard-message.html', context)


#onbording views
def typeOfPropertyView(request):
    context = {

    }
    return render(request, 'users/onbording-1.html', context)


def postPropertyAsView(request, p_type):
    request.session['property_type'] = p_type

    if p_type == 'lodges_and_cottages':
        context = {
            ''
        }
    elif p_type =='property' :
        context
    else: 
        context = {}
    
    return render(request, 'users/onbording-2.html', context)

def direct_bookings(request, **kwargs):
    return render(request, 'users/onbording-4.html')

def direct_finances(request, **kwargs):
    return render(request, 'users/onbording-5.html')

def get_booked_listings(request):
    # get user object
    user = User.objects.get(email=request.user.email)

    # get all bookings made by the user
    bnbs = BnbBooking.objects.filter(user=user).order_by('-created_at')
    lodges = LodgeBooking.objects.filter(user=user).order_by('-created_at')

    return bnbs, lodges


def get_booking_data(request):
    # get user object
    user = User.objects.get(email=request.user.email)

    # create lists to hold booking data
    lodge_list = []
    bnb_list = []

    # get listings owned by user 
    bnbs = BNBProperty.objects.filter(host=user)
    lodges = Lodge.objects.filter(user=user)

    # get all bookings made on the users listings
    for bnb in bnbs:
        bnb_list.append(
            BnbBooking.objects.filter(property=bnb)
        )

    for lodge in lodges:
        lodge_list.append(
            LodgeBooking.objects.filter(room__room_category__lodge__id=lodge.id)
        )

    return bnb_list, lodge_list

"""
Function returns all the payments a particular user has made on the site
"""
def get_user_payments(request):
    # get user object
    user = User.objects.get(email=request.user.email)

    # create list to store data
    data = []

    for payment in [PropertyPayment, BnbBookingPayment, LodgeBookingPayment]:
        data.extend(
            list(
                payment.objects.filter(user=user)
            )
        )
    
    # sort list object based on date
    sorted_data = sorted(data, key=lambda payment: payment.created)

    return sorted_data

"""
Function gets all the payments made a specific users listings
"""
def get_user_receipts(request):
    # get user object
    user = User.objects.get(email=request.user.email)

    # create list to hold data
    data = []

    # get all listings owned by the user that have a payment made to them
    for receipt in [PropertyPayment, BnbBookingPayment, LodgeBookingPayment]:
        if receipt.meta_title == 'Property':
            data.extend(
            list(
                receipt.objects.filter(
                        property__agent=user
                    )
                )
            )
        elif receipt.meta_title == 'Lodge':
            data.extend(
            list(
                receipt.objects.filter(
                        lodge__user=user
                    )
                )
            )
        elif receipt.meta_title == 'BnB':
            data.extend(
                list(
                    receipt.objects.filter(
                            bnb__host=user
                        )
                    )
                )

    # sort the list based on the date
    sorted_data = sorted(data, key=lambda receipt: receipt.created)

    return sorted_data


"""
Function returns the details of a specific bnb booking object
"""
def get_bnb_booking_details(request):
    # get reference code from request
    ref_code = request.GET.get('ref_code')

    # query database
    booking = BnbBooking.objects.get(ref_code=ref_code)

    # convert booking details to a dictionary
    booking_details = {
        'email': booking.email,
        'num_guests': booking.num_guests,
        'num_nights': booking.number_of_nights,
        'checked_in': booking.checked_in,
        'note': booking.note,
        'ref_code': booking.ref_code
    }
    
    return JsonResponse(booking_details)


"""
Function returns the details of a specific lodge booking object
"""
def get_lodge_booking_details(request):
    # get reference code from request
    ref_code = request.GET.get('ref_code')

    # query database
    booking = LodgeBooking.objects.get(ref_code=ref_code)

    # convert booking details to a dictionary
    booking_details = {
        'email': booking.email,
        'num_guests': booking.num_guests,
        'num_nights': booking.number_of_nights,
        'checked_in': booking.checked_in,
        'note': booking.note,
        'ref_code': booking.ref_code
    }
    
    return JsonResponse(booking_details)


"""
Function returns the details of a specific bnb payment object
"""
def get_bnb_payment_details(request):
    # get order key from request
    order_key = request.GET.get('order_key')

    # query database
    payment = BnbBookingPayment.objects.get(order_key=order_key)

    # convert payment details to dictionary
    payment_details = {
        'billing_status': payment.billing_status,
        'qr_code': payment.qr_code.image.url,
        'order_key': payment.order_key,
    }

    return JsonResponse(payment_details)


"""
Function returns the details of a specific lodge payment object
"""
def get_lodge_payment_details(request):
    # get order key from request
    order_key = request.GET.get('order_key')

    # query database
    payment = LodgeBookingPayment.objects.get(order_key=order_key)

    # convert payment details to dictionary
    payment_details = {
        'billing_status': payment.billing_status,
        'qr_code': payment.qr_code.image.url,
        'order_key': payment.order_key,
    }

    return JsonResponse(payment_details)


"""
Function returns the details of a specific property payment object
"""
def get_property_payment_details(request):
    # get order key from request
    order_key = request.GET.get('order_key')

    # query database
    payment = PropertyPayment.objects.get(order_key=order_key)

    # convert payment details to dictionary
    payment_details = {
        'billing_status': payment.billing_status,
        'qr_code': payment.qr_code.image.url,
        'order_key': payment.order_key,
    }

    return JsonResponse(payment_details)

