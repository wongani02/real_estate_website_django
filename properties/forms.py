from django import forms
from django.utils.translation import gettext_lazy as _

from properties.models import * 
from bnb.models import PropertyType as BnbType



class SearchForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenities.objects.all(), 
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'custom-control custom-checkbox'
        }),
    )
    bnb_type = forms.ModelChoiceField(
        queryset=BnbType.objects.all(), widget=forms.Select(attrs={
            'class': 'selectpicker custom-select-lg mb20', 'data-width': '100%', 'data-live-search': 'true',
        })
    )

    class Meta:
        model = Property
        fields = [
            'no_rooms', 'no_baths', 'no_garages', 'status',
            'property_type', 'district', 'price', 'compound_area',
            'amenities',
        ] 
        widgets = {
            'property_type': forms.Select(choices=Property.PROPERTY_TYPE, attrs={
                'class': 'selectpicker custom-select-lg mb20', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Type',
            }),
            'status': forms.Select(choices=Property.STATUS, attrs={
                'class': 'selectpicker custom-select-lg mb20', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Status', 
            }),
            'district': forms.Select(choices=Districts.objects.all(), attrs={
                'class': 'selectpicker custom-select-lg mb20', 'data-width': '100%', 'data-live-search': 'true',
                'title': 'Village'
            }),
            # )'bnb_type': forms.Select(choices=BnbType.objects.all(), attrs={
            #     'class': 'selectpicker custom-select-lg mb20', 'data-width': '100%', 'data-live-search': 'true',
            # }
        }

class PropertyInfoCreationForm(forms.ModelForm):
    desc = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form_control form-control','placeholder': 'Tell us about your lodge', 'rows':3})
    )

    class Meta:
        model = Property
        fields = ['name', 'desc', 'property_area', 'compound_area', 'year_built', 'price',
                  'property_type', 'property_status', 'property_cat', 'no_garages','no_rooms', 'no_baths',
        ]
        required = "__all__"
        widgets = {
            'property_type': forms.Select(choices=Property.PROPERTY_TYPE, attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true',
                'title': 'Property Listing Type'
            }),
            'property_status': forms.Select(choices=Property.STATUS, attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Status', 
            }),
            'property_cat': forms.Select(choices=PropertyCategory.objects.all(), attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Category',
            }),
            'year_built': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control form_control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Name of Property'
            }),
            'no_rooms': forms.NumberInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Rooms'
            }),
            'no_baths': forms.NumberInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Baths'
            }),
            'no_garages': forms.NumberInput(attrs={
                'class': 'form_control form-control', 'label': 'Garages'
            }),
            'compound_area': forms.NumberInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Compound Area (metres)'
            }),
            'property_area': forms.NumberInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Property Area (meters)'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Price'
            }),
        }


class PropertyLocationCreationForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenities.objects.all(), 
        widget=forms.CheckboxSelectMultiple(),
    )
    class Meta:
        model = Property
        fields = [
            'location_area', 'district', 
            'amenities', 'lat', 'lon',
        ]
        widgets = {
            'district': forms.Select(choices=Districts.objects.all(), attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true',
                'title': 'Village'
            }),
        }




class PropertyEditForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenities.objects.all(), 
        widget=forms.CheckboxSelectMultiple(),
    )
    desc = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form_control form-control','placeholder': 'Tell us about your lodge', 'rows':3})
    )
    class Meta:
        model = Property
        fields = [
            'name', 'desc', 'property_area', 'compound_area', 'year_built', 'price',
            'property_type', 'property_status', 'property_cat', 'no_garages','no_rooms', 'no_baths',
            'location_area', 'district', 'amenities', 'lat', 'lon',
        ]
        widgets = {
            'property_type': forms.Select(choices=Property.PROPERTY_TYPE, attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true',
                'title': 'Property Listing Type'
            }),
            'property_status': forms.Select(choices=Property.STATUS, attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Status', 
            }),
            'property_cat': forms.Select(choices=PropertyCategory.objects.all(), attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Category',
            }),
            'year_built': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control form_control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Name of Property'
            }),
            'no_rooms': forms.NumberInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Rooms'
            }),
            'no_baths': forms.NumberInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Baths'
            }),
            'no_garages': forms.NumberInput(attrs={
                'class': 'form_control form-control', 'label': 'Garages'
            }),
            'compound_area': forms.NumberInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Compound Area (metres)'
            }),
            'property_area': forms.NumberInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Property Area (meters)'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form_control form-control', 'placeholder': 'Price'
            }),
            'district': forms.Select(choices=Districts.objects.all(), attrs={
                'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true',
                'title': 'Village'
            }),
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
        fields = ['name_of_place', ]


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
        fields = ['file',]


class VideosCreationForm(forms.ModelForm):
    video = forms.FileField(help_text="Select a single video for your property.", 
        widget=forms.ClearableFileInput(attrs={
            'multiple': False, 'class': 'form-control', 'label': 'Property Video'
        })
    )
    class Meta:
        model = Videos
        fields = ['video', 'link',]
        widgets = {
            'link': forms.URLInput(attrs={
                'class': 'form-control form_control', 'placeholder': 'Video Link'
            })
        }
