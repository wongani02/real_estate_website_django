from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage

from users.models import User
from payments.models import PropertyPayment, BnbPayment, LodgePayment, PaymentOption, QRCode
from properties.models import Property
from bnb.models import Property as BnB
from lodges.models import Lodge
from core import settings

from io import BytesIO

import qrcode


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
    qr = LodgePayment.generate_qr_code(content)

    # Create payments object
    payment = LodgePayment.objects.create(
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
    send_mail(read, filename, name.name, client.email)

    return response


"""
Function sends qr code to email recepient
"""
def send_mail(buffer, filename, property_name, client):
    subject = "QR Code for " + property_name
    body = 'Please find the QR Code attached.'
    from_email = settings.EMAIL_HOST_USER
    to_email = client

    # Create email object
    email = EmailMessage(subject, body, from_email, [to_email])

    # Attach qr code image to email
    email.attach(filename, buffer, 'image/png')

    # Send email
    email.send()