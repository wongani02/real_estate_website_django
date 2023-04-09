from django.contrib import admin
from .models import PropertyType, Amenity, RoomType, Property, PropertyAmenity, PropertyImage, Booking


class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage


class BookingInline(admin.TabularInline):
    model = Booking


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
    inlines = [PropertyAmenityInline, PropertyImageInline]
    list_display = ('title', 'owner', 'property_type', 'room_type', 'city', 'state', 'country', 'is_available', 'created_at')
    list_filter = ('property_type', 'room_type', 'city', 'state', 'country', 'is_available')
    search_fields = ('title', 'description', 'address', 'city', 'state', 'country', 'zipcode')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'check_in', 'check_out', 'num_guests', 'is_paid')
    list_filter = ('user', 'property', 'check_in', 'check_out', 'is_paid')
    search_fields = ('user__username', 'property__title', 'property__address', 'property__city', 'property__state', 'property__country')


