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
    list_display = ['name', 'price', 'status', 'property_type']


@admin.register(PropertyCategory)
class PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


# @admin.register(PropertyStatus)
# class PropertyStatusAdmin(admin.ModelAdmin):
#     list_display = ['_type', 'slug']
#     prepopulated_fields = {'slug': ('_type',)}


@admin.register(Districts)
class DistrictPropertyAdmin(admin.ModelAdmin):
    list_display = ['district_name', 'slug']
    prepopulated_fields = {'slug': ('district_name',)}
