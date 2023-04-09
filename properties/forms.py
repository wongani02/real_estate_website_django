from django import forms
from django.utils.translation import gettext_lazy as _

from properties.models import * 


class PropertyCreationForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name',
                  'property_type', 'status', 'property_cat', 'no_garages','no_rooms', 'no_baths',
            'year_built', 'location_area', 'price', 'district', 
            # 'amenities', 
        ]
        widgets = {
            'property_type': forms.Select(choices=Property.PROPERTY_TYPE, attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Type',
            }),
            'status': forms.Select(choices=Property.STATUS, attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Status', 
            }),
            'property_cat': forms.Select(choices=PropertyCategory.objects.all(), attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Category',
            }),
            'year_built': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control form_control'
            }),
            'district': forms.Select(choices=Districts.objects.all(), attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true',
                'title': 'Village'
            }),
            # 'amenities': forms.CheckboxSelectMultiple(choices=Amenities.objects.all(), attrs={})
        }



class DistrictCreationForm(forms.ModelForm):
    class Meta:
        model = Districts
        fields = ['district_name',]
        widgets ={
            'district_name': forms.TextInput(attrs={
                'class': 'form-control', 'name': 'district_name', 'id': 'district_name',
            }),
        }


class NearbyPlacesCreationForm(forms.ModelForm):
    class Meta:
        model = NearbyPlaces
        fields = ['name_of_place', 'location',]


class PropertyCategoryCreationForm(forms.ModelForm):
    class Meta:
        model = PropertyCategory 
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'name': 'cat_name'})
        }


class PropertyTypesCreationForm(forms.ModelForm):
    class Meta:
        model = PropertyType
        fields = ['_type', 'slug',]


class AmenitiesCreationForm(forms.ModelForm):
    class Meta:
        model = Amenities 
        fields = ['name', 'desc',]
        widgets = {
            'name': forms.TextInput(attrs={
                'name': 'amenity_name', 'id': 'amenity_name', 'class': 'form-control',
            }),
            'desc': forms.TextInput(attrs={
                'name': 'amenity_desc', 'id': 'amenity_desc', 'class': 'form-control',
            })
        }


class ImagesCreationForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image',]
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'multiple': True, 'class': 'input-img',
            }),
        }
