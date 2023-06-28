from django.contrib import admin
from .models import *


class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 0


class BNBRestrictionInline(admin.TabularInline):
    model = BNBRestrictions
    extra = 0


class ImageInline(admin.TabularInline):
    model = BNBImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0


class BNBPolicyInline(admin.StackedInline):
    model = BNBCancellationPolicy
    extra=0


class BookingInline(admin.TabularInline):
    model = Booking

class RoomInline(admin.TabularInline):
    model = BNBRoom
    extra=0

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyAmenityInline, BNBRestrictionInline, PropertyImageInline, RoomInline, BNBPolicyInline]
    list_display = ('title', 'host', 'property_type', 'city', 'country', 'is_active', 'created_at')
    list_filter = ('property_type', 'city','country', 'is_active')
    search_fields = ('title', 'description', 'street_name', 'city', 'country')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'check_in', 'check_out', 'num_guests', 'is_paid')
    list_filter = ('user', 'property', 'check_in', 'check_out', 'is_paid')
    search_fields = ('user__username', 'property__title', 'property__street_name', 'property__city', 'property__country')


admin.site.register(Policy)
admin.site.register(PropertyImage)
admin.site.register(BNBImage)
admin.site.register(Restrictions)

