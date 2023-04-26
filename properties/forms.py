from django import forms
from django.utils.translation import gettext_lazy as _

from properties.models import * 



class SearchForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenities.objects.all(), 
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'custom-control custom-checkbox'
        }),
    )

    class Meta:
        model = Property
        fields = [
            'no_rooms', 'no_baths', 'no_garages', 'status',
            'property_type', 'district', 'price', 'compound_area',
            'amenities',
        ] 
        # widgets = {
        #     'property_type': forms.Select(choices=Property.PROPERTY_TYPE, attrs={
        #         'class': 'selectpicker custom-select-lg mb20', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Type',
        #     }),
        #     'status': forms.Select(choices=Property.STATUS, attrs={
        #         'class': 'selectpicker custom-select-lg mb20', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Status', 
        #     }),
        #     'district': forms.Select(choices=Districts.objects.all(), attrs={
        #         'class': 'selectpicker custom-select-lg mb20', 'data-width': '100%', 'data-live-search': 'true',
        #         'title': 'Village'
        #     }),
        # }

class PropertyCreationForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenities.objects.all(), 
        widget=forms.CheckboxSelectMultiple(),
    )
    class Meta:
        model = Property
        fields = ['name',
                  'property_type', 'status', 'property_cat', 'no_garages','no_rooms', 'no_baths',
            'year_built', 'location_area', 'price', 'district', 
            'amenities', 'lat', 'lon',
        ]
        # widgets = {
        #     'property_type': forms.Select(choices=Property.PROPERTY_TYPE, attrs={
        #         'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Type',
        #     }),
        #     'status': forms.Select(choices=Property.STATUS, attrs={
        #         'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Status', 
        #     }),
        #     'property_cat': forms.Select(choices=PropertyCategory.objects.all(), attrs={
        #         'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Category',
        #     }),
        #     'year_built': forms.DateInput(attrs={
        #         'type': 'date', 'class': 'form-control form_control'
        #     }),
        #     'district': forms.Select(choices=Districts.objects.all(), attrs={
        #         'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true',
        #         'title': 'Village'
        #     }),
        # }



class PropertyEditForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenities.objects.all(), 
        widget=forms.CheckboxSelectMultiple(),
    )
    class Meta:
        model = Property
        fields = ['name',
                  'property_type', 'status', 'property_cat', 'no_garages','no_rooms', 'no_baths',
            'year_built', 'location_area', 'price', 'district', 
            'amenities', 'lat', 'lon',
        ]
        # widgets = {
        #     'property_type': forms.Select(choices=Property.PROPERTY_TYPE, attrs={
        #         'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Type',
        #     }),
        #     'status': forms.Select(choices=Property.STATUS, attrs={
        #         'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Status', 
        #     }),
        #     'property_cat': forms.Select(choices=PropertyCategory.objects.all(), attrs={
        #         'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Category',
        #     }),
        #     'year_built': forms.DateInput(attrs={
        #         'type': 'date', 'class': 'form-control form_control'
        #     }),
        #     'district': forms.Select(choices=Districts.objects.all(), attrs={
        #         'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true',
        #         'title': 'Village'
        #     }),
        # }



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
    image = forms.ImageField(help_text="You can select and add multiple images to this field.", 
        widget=forms.ClearableFileInput(attrs={
            'multiple': True, 'class': 'img-fluid', 'label': ''
    }))
    class Meta:
        model = Images
        fields = ['image',]


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
