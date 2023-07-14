from django.contrib import admin

from .models import *

# Register your models here.


admin.site.register(PaymentOption)
admin.site.register(LodgeBookingPayment)
admin.site.register(BnbBookingPayment)
admin.site.register(PropertyCharge)
