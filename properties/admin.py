from django.contrib import admin
from .models import *

from properties.models import *

# Register your models here.

admin.site.register(Amenities)


class VideoModelAdmin(admin.StackedInline):
    model = Videos
    extra = 1


class ImageModelAdmin(admin.StackedInline):
    model = Images


class NearbyPlacesModelAdmin(admin.StackedInline):
    model = NearbyPlaces
    extra = 2


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [NearbyPlacesModelAdmin, ImageModelAdmin , VideoModelAdmin]
    list_display = ['name', 'price', 'property_type']


@admin.register(PropertyCategory)
class PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Districts)
class DistrictPropertyAdmin(admin.ModelAdmin):
    list_display = ['district_name', 'slug']
    prepopulated_fields = {'slug': ('district_name',)}


admin.site.register(Images)
admin.site.register(PropetyViews)
admin.site.register(Likes)
admin.site.register(TempImageStore)