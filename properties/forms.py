from django import forms
from django.utils.translation import gettext_lazy as _

from properties.models import Property


class PropertyCreationForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'price', 'location_area', 'lat', 'lon',
                  'property_type', 'status', 'year_built', 'compound_area', 'no_garages',
                  'no_rooms', 'no_baths', 'desc', 'status', 'district', 'agent',]
        required = '__all__'
