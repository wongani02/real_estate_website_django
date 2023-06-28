from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site

from users.models import User
from payments.models import PropertyPayment, BnbPayment, LodgeBookingPayment, PaymentOption, QRCode
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
def generate_properties_code(request):
    # Create a user object
    user = User.objects.get(username=request.user.username)

    # Create a property object
    # modify this object
    _property_ = Property.objects.first()

    # Get relavant qr data
    content = {
        'property_name': _property_.name, 'property_location': _property_.location_area,
        'price': _property_.price, 'username': user.username 
    }

    # Get returned QRCode object
    qr = PropertyPayment.generate_qr_code(content)

    # Create payments object
    payment = PropertyPayment.objects.create(
        user=user, email=user.email, full_name=user.name,
        payment_option=PaymentOption.objects.first(),
        property=_property_, qr_code=qr
    )

    # Save model instance
    payment.save()
    
    # Add qr data to session
    qr_content(request, content)
    
    return render(request, 'payments/page-coming-soon.html', {'qr': qr, 'property': _property_})



"""
Function creates and returns a qr code to template for the properties model
"""
def generate_lodges_code(request):
    # Create a user object
    user = User.objects.get(username=request.user.username)

    # Create a property object
    # modify this object
    _property_ = BnB.objects.first()

    # Get relavant qr data
    content = {
        'property_name': _property_.title, 'owner': _property_.host, 'property_location': _property_.street_name,
        'price': _property_.price_per_night,
    }

    # Get returned QRCode object
    qr = BnbPayment.generate_qr_code(content)

    # Create payments object
    payment = BnbPayment.objects.create(
        user=user, email=user.email, full_name=user.name,
        payment_option=PaymentOption.objects.first(),
        property=_property_, qr_code=qr
    )

    # Save model instance
    payment.save()
    
    # Add qr data to session
    qr_content(request, content)
    
    return render(request, 'payments/page-coming-soon.html', {'qr': qr, 'property': _property_})



"""
Function creates and returns a qr code to template for the properties model
"""
def generate_bnbs_code(request):
    # Create a user object
    user = User.objects.get(username=request.user.username)

    # Create a property object
    # modify this object
    _property_ = Lodge.objects.first()

    # Get relavant qr data
    content = {
        'property_name': _property_.name, 'property_location': _property_.map_location,
        'username': user.username 
    }

    # Get returned QRCode object
    qr = LodgeBookingPayment.generate_qr_code(content)

    # Create payments object
    payment = LodgeBookingPayment.objects.create(
        user=user, email=user.email, full_name=user.name,
        payment_option=PaymentOption.objects.first(),
        property=_property_, qr_code=qr
    )

    # Save model instance
    payment.save()
    
    # Add qr data to session
    qr_content(request, content)

    return render(request, 'payments/page-coming-soon.html', {'qr': qr, 'property': _property_})



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
    name = Property.objects.get(id=kwargs.get('pk'))
    
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
    to_email = client.email

    # Create email object
    email = EmailMultiAlternatives(subject, plain_text, from_email, [to_email])
    # email = send_mail(subject, email_body, from_email, [to_email], html_message=email_body)
    
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