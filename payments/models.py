import uuid, qrcode

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.staticfiles.storage import staticfiles_storage

from properties.models import Property
from bnb.models import Property as BNB
from lodges.models import Lodge
from .utils import generate_ref_code
from io import BytesIO

from PIL import Image

class QRCode(models.Model):
    class Meta:
        verbose_name = 'QR Code'
        verbose_name_plural = 'QR Codes'

    id = models.UUIDField(_("QR Code ID"), primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(_("Created On"), auto_now=True)
    image = models.ImageField(upload_to='qr_codes/')


class PaymentOption(models.Model):
    payment_option = models.CharField(help_text=_('payment option name'), max_length=200, null=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.payment_option


class Payment(models.Model):
    id = models.UUIDField(
        _('payment ID'), 
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        on_delete=models.RESTRICT)
    full_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=10, null=True,  decimal_places=1)
    order_key = models.CharField(max_length=200, null=True)
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.CASCADE, null=True)
    billing_status = models.BooleanField(default=False, null=True)
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE, null=True)
    
    def generate_qr_code(content_dict):
        qr_content = ""

        for key, value in content_dict.items():
            qr_content += f"{key}: {value}\n"

        # Generate qr code image
        qr_code = qrcode.make(qr_content)
        
        # Create a file name for the qr code
        file_name = f"qr_code_{uuid.uuid4().hex}.png"

        # Create a file path for the qr code image
        file_path = f"qrcodes/{file_name}"

        # Save the qr code image to the media storage
        file_stream = BytesIO()
        qr_code.save(file_stream, format='PNG')
        file_stream.seek(0)
        file_content = ContentFile(file_stream.read())
        file_path = default_storage.save(file_path, file_content)

        # Create and return QRCode object
        obj = QRCode.objects.create(image=file_path)

        return obj

    def __str__(self):
        return self.full_name
    
    class Meta:
        abstract = True
    

class PropertyPayment(Payment):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, related_name="property_payment")


class BnbPayment(Payment):
    bnb = models.ForeignKey(BNB, on_delete=models.CASCADE, null=True)


class LodgePayment(Payment):
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, null=True)


class Invoice(models.Model):
    # payment = models.ForeignKey(Payment, on_delete=models.RESTRICT, null=True, related_name='payment_invoice')
    ref_num = models.CharField(max_length=12, null=True,default=generate_ref_code())
    invoice = models.FileField(null=True, upload_to='invoices/')

    def __str__(self):
        return ' {}'.format(self.ref_num)
    
    class Meta:
        abstract = True         


#will work on these letter

# class PropertyPayment(Invoice):
#     property = models.ForeignKey(PropertyPayment, on_delete=models.CASCADE, null=True)


# class BnbPayment(Payment):
#     bnb = models.ForeignKey(BnbPayment, on_delete=models.CASCADE, null=True)


# class LodgePayment(Payment):
#     lodge = models.ForeignKey(LodgePayment, on_delete=models.CASCADE, null=True)

