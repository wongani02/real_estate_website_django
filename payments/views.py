from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site

from users.models import User
from payments.models import BnbBookingPayment, LodgeBookingPayment, PaymentOption, QRCode, Payment
from properties.models import Property
from bnb.models import Property as BnB
from lodges.models import Lodge, About
from core import settings
from payments.utils import EmailThread
from io import BytesIO
from datetime import datetime

import datetime as d
import qrcode, pytz


"""
Function creates and returns a qr code to template for the properties model
"""
def generate_lodges_code(request):
    # Create a user object
    user = User.objects.get(username=request.user.username)

    # Get data from booking session
    if 'lodge_booking' in request.session:
        payment_id = request.session['lodge_booking']

        payment = LodgeBookingPayment.objects.get(pk=payment_id)

        booking = payment.booking.first()

    if 'bnb_booking' in request.session:
        booking_id = request.session['bnb_booking']

        payment = BnbBookingPayment.objects.get(pk=payment_id)

        # Get data from booking table
        booking = payment.booking.first()

    # Get relavant qr data
    content = {
        'Property Name': booking.room.room_category.lodge.name, 'Property Location': booking.room.room_category.lodge.map_location,
        'Reference Code': booking.ref_code, 'Username': booking.full_name, 'Email': booking.email, 'Check In': booking.check_in, 
        'Check Out': booking.check_out, 'Created On': booking.created_at, 'Number of Rooms': booking.number_of_rooms,
        'Number of Nights': booking.number_of_nights, 'Number of Guests': booking.num_guests
    }

    if 'lodge_booking' in request.session:

        # Get returned QRCode object
        qr = LodgeBookingPayment.generate_qr_code(content)

        _property_ = payment.lodge

        # delete session
        del request.session['lodge_booking']

    if 'bnb_booking' in request.session:
        # Get returned QRCode object
        qr = BnbBookingPayment.generate_qr_code(content)
        
        _property_ = payment.bnb

        # Delete session
        del request.session['bnb_booking']


    # Save model instance
    payment.save()

    # Get booking content
    booking_content = get_booking_content(booking)
    
    # Add qr data to session
    qr_content(request, booking_content)
    
    return render(request, 'payments/page-coming-soon.html', {'qr': qr, 'property': _property_})


def get_booking_content(booking):
    content = {
        'property_name': booking.room.room_category.lodge.name, 'property_location': booking.room.room_category.lodge.map_location,
        'ref_code': booking.ref_code, 'username': booking.full_name, 'email': booking.email, 'check_in': booking.check_in, 
        'check_out': booking.check_out, 'created_at': booking.created_at, 'no_rooms': booking.number_of_rooms,
        'no_nights': booking.number_of_nights, 'guests': booking.num_guests
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
    send_mail(request, read, filename, name, client)

    return response


"""
Function sends qr code to email recepient
"""
def send_mail(request, buffer, filename, _property_, client):
    # Get company object
    company = About.objects.first()

    # Get current site
    current_site = get_current_site(request)

    # Get current date and time
    formatted_date, current_tz, time = get_current_time_data()

    # Create emails subject
    subject = "QR Code for " + _property_.name

    # Create context variables
    context = {
         'company_name': company.company_name, 'company_addr': company.address,
         'company_tel': company.phone_number, 'user': client, 'property': _property_,
         'date': formatted_date, 'zone': current_tz, 'time': time, 'qr': buffer,
         'current_site': current_site
    }

    # Create email body
    email_body = render_to_string('payments/payment-email.html', context)
    plain_text = strip_tags(email_body)

    # Create email sender
    from_email = settings.EMAIL_HOST_USER

    # Create email recepient
    to_email = request.session['booking_email']

    # delete session
    del request.session['booking_email']

    # Create email object
    email = EmailMultiAlternatives(subject, plain_text, from_email, [to_email])

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


# qr id
# property url