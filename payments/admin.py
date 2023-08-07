from django.contrib import admin

from .models import *

class PropertyChargeModelAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    # fields = ('price',)
    fieldsets = (
        (
            'Charge Price For All Property Listings',
            {'fields': ('price', 'date')}
        ),
    )

admin.site.register(QRCode)
admin.site.register(PaymentOption)
admin.site.register(PropertyPayment)
admin.site.register(LodgeBookingPayment)
admin.site.register(BnbBookingPayment)
admin.site.register(PropertyCharge, PropertyChargeModelAdmin)
