from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from users.models import User
from payments.models import PropertyPayment, PaymentOption, QRCode
from properties.models import Property

def generate_properties_code(request):
    # Create a user object
    user = User.objects.get(username=request.user.username)

    # Create a property object
    _property_ = Property.objects.first()

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
    payment.save()
    
    print("Content: ", payment)
    
    return render(request, 'payments/page-coming-soon.html', {'qr': qr})


def download_qr_code(request, **kwargs):
    # Retrieve QRCode object
    qr = QRCode.objects.get(id=kwargs.get('pk'))

    response = HttpResponse(content_type="image/png")

    response["Content-Disposition"] = f"attachment; filename={request.user.name}_qr_code_{qr.id}.png"

    return response