from django.contrib import admin

from .models import PaymentOption, LodgeBookingPayment

# Register your models here.


admin.site.register(PaymentOption)
admin.site.register(LodgeBookingPayment)