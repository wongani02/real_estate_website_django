from django.contrib import admin

from .models import *
from properties.models import Property as Property_
from properties.utils import verification_status


class ListingAdmin(admin.ModelAdmin):
    list_display = ('property', 'verification', 'date_sub', 'date_ver',)
    readonly_fields = ('date_sub',)
    list_filter = ('verification', 'date_sub', 'date_ver')
    fieldsets = (
        (
            'Listing Overview', 
            {'fields': ('property',)}
        ),
        (
            'Verification Status',
            {'fields': ('verification', 'reason',)}
        ),
        (
            'Verification Date',
            {'fields': ('date_ver',)}
        )
    )

    def save_model(self, request, obj, form, change):
        print("contents: ", obj)
        # call the parents save_model method to save the object
        super().save_model(request, obj, form, change)
        user = None
        try:
            user = obj.property.agent
        except:
            pass
        try:
            user = obj.property.user
        except:
            pass
        try:
            user = obj.property.host
        except:
            pass

        if obj.verification == 'VERIFIED' or obj.verification == 'Verified':
            verification_status(user.email, obj.property, client=user, obj=obj, request=request)

        elif obj.verification == 'DECLINED' or obj.verification == 'Declined':
            verification_status(user.email, obj.property, client=user, obj=obj, issues=obj.reason, request=request)


admin.site.register(PropertyListing, ListingAdmin)
admin.site.register(BnBListing, ListingAdmin)
admin.site.register(LodgeListing, ListingAdmin)
admin.site.register(Listing)

