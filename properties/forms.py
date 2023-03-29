from django import forms
from django.utils.translation import gettext_lazy as _

from properties.models import * 


class PropertyCreationForm(forms.ModelForm):
    f=PropertyCategory.objects.all()
    class Meta:
        model = Property
        fields = ['property_type', 'name', 'status', 'property_cat', 'no_garages','no_rooms', 'no_baths',
            'year_built', 'property_area', 'price', 'addr', 
        ]
        widgets = {
            'property_type': forms.Select(choices=Property.PROPERTY_TYPE, attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Type',
            }),
            'status': forms.Select(choices=Property.STATUS, attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Status', 
            }),
            # 'property_cat': forms.ModelChoiceField(queryset=PropertyCategory.objects.all()),
            'property_cat': forms.Select(choices=PropertyCategory.objects.all(), attrs={
                'class': 'selectpicker', 'data-width': '80%', 'data-live-search': 'true', 'title': 'Property Category',
            }),
            'year_built': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form_control'})
        }


class DistrictCreationForm(forms.ModelForm):
    class Meta:
        model = Districts
        fields = ['district_name',]
        required = '__all__'


class NearbyPlacesCreationForm(forms.ModelForm):
    class Meta:
        model = NearbyPlaces
        fields = ['name', 'location',]


class PropertyCategoryCreationForm(forms.ModelForm):
    class Meta:
        model = PropertyCategory 
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class PropertyTypesCreationForm(forms.ModelForm):
    class Meta:
        model = PropertyType
        fields = ['_type', 'slug',]


class AmenitiesCreationForm(forms.ModelForm):
    class Meta:
        model = Amenities 
        fields = '__all__'
