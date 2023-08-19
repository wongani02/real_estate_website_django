from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

from users.models import User
from payments.models import BnbBookingPayment, LodgeBookingPayment, PaymentOption, QRCode, Payment, PropertyPayment, PropertyCharge
from properties.models import Property, Receipt
from bnb.models import Property as BnB, Booking as BNBBooking
from lodges.models import Lodge, About, Booking as LodgeBooking
from core import settings
from payments.utils import EmailThread
from io import BytesIO
from datetime import datetime

import datetime as d
import qrcode, pytz
import uuid
import qrcode, pytz, json


"""
Function creates and returns a qr code to template for the properties model
"""
def generate_code(request):
    try:
        # Create a user object
        user = User.objects.get(username=request.user.username)

        # Get data from booking session
        if 'lodge_booking' in request.session:
            payment_key = request.session['lodge_booking']

            payment = LodgeBookingPayment.objects.get(order_key=payment_key)

            # create a booking email session
            request.session['booking_email'] = payment.email

            booking = payment.booking.all()
            
            # variable to hold the number of booking instances
            no_bookings = 0

            for a in booking:
                no_bookings += 1

                # ignored existence of any other booking data as the relevant data is 
                # contained in the payments row. However, multiple bookings can still
                # be accessed for other purposes other than the creation of a qr code
                booking = LodgeBooking.objects.get(id=a.id)

            # Get booking content
            booking_content = get_lodge_booking_content(booking, no_bookings, request)  

            # save booking content to session incase the page is refreshed
            # request.session['booking_content'] = json.dumps(booking_content)

            # Get returned QRCode object
            qr = LodgeBookingPayment.generate_qr_code(booking_content)

            # assign qr code to bnb booking payment object
            payment.qr_code = qr

            payment.save()

            _property_ = payment.lodge

        elif 'bnb_booking' in request.session:
            booking_id = request.session['bnb_booking']

            payment = BnbBookingPayment.objects.get(order_key=booking_id)

            # create a booking email session
            request.session['booking_email'] = payment.email

            # Get data from booking table
            booking = payment.booking.id

            booking = BNBBooking.objects.get(id=booking)

            # Get booking content
            booking_content = get_bnb_booking_content(booking, request)

            # save booking content to session incase the page is refreshed
            # request.session['booking_content'] = json.dumps(booking_content)

            # Get returned QRCode object
            qr = BnbBookingPayment.generate_qr_code(booking_content)

            # assign qr code to bnb booking payment object
            payment.qr_code = qr
            booking.qr_code = qr

            payment.save()
            
            _property_ = payment.bnb

        elif 'property_payment' in request.session:
            payment_id = request.session['property_payment']

            payment = PropertyPayment.objects.get(order_key=payment_id)

            # create a booking email session
            request.session['booking_email'] = payment.email

            # Get data from receipt table
            receipt_id = payment.receipt.id

            booking = Receipt.objects.get(id=receipt_id)

            # Get receipt content
            booking_content = get_property_payment_content(payment)

            # save booking content to session incase the page is refreshed
            # request.session['booking_content'] = json.dumps(booking_content)

            # Get returned QRCode object
            qr = PropertyPayment.generate_qr_code(booking_content)

            # assign qr code to property payment object
            payment.qr_code = qr
            booking.qr_code = qr

            payment.save()
            
            _property_ = payment.property

        # Save model instance
        # payment.save()
        
        # Add qr data to session to be used on download
        # if booking_content is None:
        #     qr_content(request, json.loads(request.session['booking_content']))
        # else:    
        qr_content(request, booking_content)

        # return to qr page if this request is from a property payment and not lodge or bnb
        if 'property_payment' in request.session:
            # Delete session
            del request.session['property_payment']

            return render(
                request, 
                'payments/page-coming-soon.html', 
                {
                    'qr': qr, 'property': _property_, 'booking': booking,
                    'time': None
                }
            )

        # else take normal route
        return render(
            request, 'payments/page-coming-soon.html', 
            {
                'qr': qr, 'property': _property_, 'booking': booking,
                'time': booking.check_in
            }
        )
    except: 
        return render(request, 'payments/page-error.html')

def get_lodge_booking_content(booking, no_bookings, request):
    # get current site 
    site = get_current_site(request)

    # get the url for the page
    page_link = str(site) + str(reverse('lodges:lodge-detail', args=[booking.lodge.id]))

    content = {
        'Property Name': booking.room.room_category.lodge.name, 'Property Location': booking.room.room_category.lodge.map_location,
        'Reference Code': booking.ref_code, 'Username': booking.full_name, 'Email': booking.email, 'Check In': booking.check_in, 
        'Check Out': booking.check_out, 'Created On': booking.created_at, 'Number of Rooms': no_bookings,
        'Number of Nights': booking.number_of_nights, 'Number of Guests': booking.num_guests, "Url": page_link
    }

    return content


def get_bnb_booking_content(booking, request):
    # get current site 
    site = get_current_site(request)

    # get the url for the page
    page_link = str(site) + str(reverse('lodges:lodge-detail', args=[booking.lodge.id]))

    content = {
        'Property Name': booking.property.title, 'Property Location': booking.property.street_name,
        'Reference Code': booking.ref_code, 'Username': booking.full_name, 'Email': booking.email, 'Check In': booking.check_in, 
        'Check Out': booking.check_out, 'Created On': booking.created_at,
        'Number of Nights': booking.number_of_nights, 'Number of Guests': booking.num_guests, "Url": page_link,
    }

    return content

def get_property_payment_content(payment):

    # create content
    content = {
        'Property Name': payment.property.name, 'Property Location': payment.property.location_area,
        'Reference Code': payment.receipt.ref_code, 'Username': payment.full_name, 'Email': payment.email,
        'Created On': payment.receipt.created_at, 'Amount': payment.total_paid
    }

    return content


"""
Function adds qr code data to session variable
"""
def qr_content(request, content):
    qr_content = ""

    # Lop through content dict to string
    for key, value in content.items():
            qr_content += f"{key}: {value}\n"

    # Append string data to session
    request.session['qr_content'] = qr_content

"""
Function downloads and sends qr to user
"""
def download_qr_code(request, **kwargs):
    # Retrieve QRCode content from session
    if request.session['qr_content']:
        content = request.session['qr_content']

    qr_code = qrcode.make(content)

    buffer = BytesIO()
    qr_code.save(buffer, format="PNG")
    buffer.seek(0)

    # Get image data
    read = buffer.getvalue()

    response = HttpResponse(buffer, content_type="image/png")
    filename = str(request.user) + "_qr_code.png"
    response["Content-Disposition"] = f"attachment; filename={filename}"

    # Get name of property
    try:
        name = Property.objects.get(id=kwargs.get('pk'))
    except ObjectDoesNotExist:
        pass
    try:
        name = BnB.objects.get(id=kwargs.get('pk'))
    except ObjectDoesNotExist:
        pass
    try:
        name = Lodge.objects.get(id=kwargs.get('pk'))
    except ObjectDoesNotExist:
        pass
    
    # Get username - email of recepient
    client = User.objects.get(username=request.user.username)

    # Send email qr to user
    send_mail(request, read, filename, client, name)
 
    # Delete session
    # del request.session['bnb_booking']
    # del request.session['lodge_booking']

    return response


"""
Function sends qr code to email recepient
"""
def send_mail(request, buffer, filename, client, _property_):
    # Get company object
    company = About.objects.first()

    # Get current site
    current_site = get_current_site(request)

    # Get current date and time
    formatted_date, current_tz, time = get_current_time_data()

    # Create emails subject
    subject = "QR Code for " + client.username

    # Create context variables
    context = get_context(_property_, company, client, request, formatted_date, current_tz, time, buffer, current_site)

    # Create email body
    email_body = render_to_string('payments/booking-reservation.html', context)
    plain_text = strip_tags(email_body)

    # Create email sender
    from_email = settings.EMAIL_HOST_USER

    # Create email recepient
    to_email = request.session['booking_email']

    # delete session
    # del request.session['booking_email']

    # Create email object
    email = EmailMultiAlternatives(subject, plain_text, from_email, ["bau19-cnyemba@poly.ac.mw"])

    # Attach qr code and email html image to email
    email.attach(filename, buffer, 'image/png')
    email.attach_alternative(email_body, 'text/html')

    # Send email via thread
    EmailThread(email).start()


"""
Function returns current time data:
date, time and timezone
"""
def get_current_time_data():
    current_date = datetime.now()
    time = datetime.now().time()
    current_tz = current_date.now().astimezone().tzinfo
    current_time = time.strftime("%H:%M")
    formatted_date = current_date.strftime("%A, %d %B %Y")

    return formatted_date, current_tz, current_time

def get_context(property, company, client, request, formatted_date, current_tz, time, buffer, current_site):
    if property.meta_title == 'Lodge':
        # use order key to get payment object
        payment_key = request.session['lodge_booking']
        payment = LodgeBookingPayment.objects.get(order_key=payment_key)

        context = {
            'company_name': company.company_name, 'company_addr': company.address,
            'company_tel': company.phone_number, 'user': client, 'property': property,
            'date': formatted_date, 'zone': current_tz, 'time': time, 'qr': buffer,
            'current_site': current_site, 'payment': payment
        }

        return context

    elif property.meta_title == 'BnB':
        # use order key to get payment object
        booking_id = request.session['bnb_booking']
        payment = BnbBookingPayment.objects.get(order_key=booking_id)

        context = {
            'company_name': company.company_name, 'company_addr': company.address,
            'company_tel': company.phone_number, 'user': client, 'property': property,
            'date': formatted_date, 'zone': current_tz, 'time': time, 'qr': buffer,
            'current_site': current_site, 'payment': payment
        }

    elif property.meta_title == 'Property':
        # use key to get payment data
        payment_id = request.session['property_payment']
        payment = PropertyPayment.objects.get(order_key=payment_id)

        # get the charged rate
        charge = PropertyCharge.objects.first()

        context = {
            'company_name': company.company_name, 'company_addr': company.address,
            'company_tel': company.phone_number, 'user': client, 'property': property,
            'date': formatted_date, 'zone': current_tz, 'time': time, 'qr': buffer,
            'current_site': current_site, 'payment': payment, 'charge': charge
        }

        return context