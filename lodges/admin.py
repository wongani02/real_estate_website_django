from django.contrib import admin
from .models import *


class LodgeAmenityInline(admin.TabularInline):
    model = LodgeAmenity
    extra = 0


class LodgePolicyInline(admin.StackedInline):
    model=LodgeCancellationPolicy
    extra = 0


class LodgeRestrictionsInline(admin.TabularInline):
    model = LodgeRestrictions
    extra = 0


class PictureInline(admin.TabularInline):
    model = LodgeImage
    extra = 0


class RoomCategoryInline(admin.StackedInline):
    model = RoomCategory
    extra = 0


@admin.register(Lodge)
class LodgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'street_name', 'city', 'map_location', 'country',)
    inlines = [
        RoomCategoryInline, 
        LodgeAmenityInline, 
        LodgeRestrictionsInline, 
        PictureInline, 
        LodgePolicyInline
    ]


# @admin.register(RoomCategory)
# class RoomAdmin(admin.ModelAdmin):
#     list_display = ('lodge', 'room_type', 'adults', 'price_per_night',)
    # inlines = [ PictureInline]

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ['policy']


@admin.register(Restrictions)
class RestrictionAdmin(admin.ModelAdmin):
    list_display = ['restriction']


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'num_guests', 'created_at',)


#blog admin
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'is_active',
    ]
    prepopulated_fields = {'slug': ('name',)}


class BlogImageInline(admin.StackedInline):
    model = BlogImage
    extra = 2


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogImageInline]


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'email', 'phone_number']


# @admin.register(Room)
# class LodgeRoomAdmin(admin.ModelAdmin):
#     list_display = ['is_booked']
    

# admin.site.register(Image)
admin.site.register(Room)