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
            'no_rooms', 'no_baths', 'no_garages',
            'property_type', 'district', 'price', 'compound_area',
            'amenities',
        ] 
        widgets = {
            'property_type': forms.Select(choices=Property.PROPERTY_TYPE, attrs={
                'class': 'selectpicker custom-select-lg mb20', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Type',
            }),
            'district': forms.Select(choices=Districts.objects.all(), attrs={
                'class': 'selectpicker custom-select-lg mb20', 'data-width': '100%', 'data-live-search': 'true',
                'title': 'Village'
            }),
        }

class PropertyInfoCreationForm(forms.ModelForm):
    desc = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form_control form-control','placeholder': 'Tell us about your Property...', 'rows':3})
    )
    property_cat = forms.ModelChoiceField(queryset=PropertyCategory.objects.all(), empty_label="Property", widget=forms.Select(attrs={
        'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'placeholder': 'Property Category',
    }))

    def __init__(self, *args, **kwargs):
        super(PropertyInfoCreationForm, self).__init__(*args, **kwargs)

        self.fields['property_cat'].empty_label = None

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.NumberInput):
                field.initial = None
    

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
                'class': 'form_control form-control', 'placeholder': 'Garages'
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

class PropertyCategoryCreationForm(forms.ModelForm):
    class Meta:
        model = PropertyCategory 
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'name': 'cat_name'})
        }


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
