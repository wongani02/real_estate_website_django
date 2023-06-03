from django.contrib import admin
from .models import Lodge, Room, Amenity, LodgeAmenity, LodgeImage, Booking, BlogPost, BlogImage, BlogCategory, About, Image


class LodgeAmenityInline(admin.TabularInline):
    model = LodgeAmenity
    extra = 0


class PictureInline(admin.TabularInline):
    model = LodgeImage
    extra = 0


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0


@admin.register(Lodge)
class LodgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'state', 'country',)
    inlines = [RoomInline, LodgeAmenityInline, PictureInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('lodge', 'room_type', 'adults', 'price_per_night',)
    # inlines = [ PictureInline]


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


admin.site.register(Image)