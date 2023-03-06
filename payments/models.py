import uuid

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from properties.models import Property
from .utils import generate_ref_code

# Create your models here.

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
    property=models.ForeignKey(
        Property, 
        null=True,
        on_delete=models.RESTRICT,
        related_name='property_payment')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        on_delete=models.RESTRICT, 
        related_name='user_payment')
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=10, null=True,  decimal_places=1)
    order_key = models.CharField(max_length=200, null=True)
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.CASCADE, null=True)
    billing_status = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Invoice(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.RESTRICT, null=True, related_name='payment_invoice')
    ref_num = models.CharField(max_length=12, null=True,default=generate_ref_code())
    invoice = models.FileField(null=True, upload_to='invoices/')

    def __str__(self):
        return '{} - {}'.format(self.payment.full_name, self.ref_num)
