from django.contrib import admin
from .models import Lodge, Room, Amenity, RoomAmenity, Picture, Booking


class RoomAmenityInline(admin.TabularInline):
    model = RoomAmenity
    extra = 0


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 2


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0


@admin.register(Lodge)
class LodgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state', 'country')
    inlines = [RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('lodge', 'number', 'type', 'capacity', 'price_per_night')
    inlines = [RoomAmenityInline, PictureInline]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'num_guests', 'created_at')
