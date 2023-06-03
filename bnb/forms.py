from django import forms
from .models import Amenity, PropertyAmenity, PropertyType


class BNBDetailsForm(forms.Form):
    property_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'Name of Bnb'})
    )
    street_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'Street name'})
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'City / District'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form_control form-control', 'placeholder': 'Tell us about your BNB', 'rows':3})
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form_control', 'placeholder': 'Location area'})
    )
    number_of_rooms = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control form_control', 'min': 0,'placeholder': 'How many rooms do you have?'})
    )
    contact_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form_control form-control', 'placeholder':'Contact email'})
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control','placeholder': 'Contact Number'})
    )
    bnb_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form_control form-control', 'placeholder': 'Bnb type'}),
        queryset=PropertyType.objects.all()
    )
    price_per_night = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control form_control', 'min': 0,'placeholder': 'Set your price per night'})
    )


class BNBRoomCreationForm(forms.Form):
    
    adults = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form_control form-control ', 'min': 0, 'placeholder': 'Max number of guests'}),required=True,
    )
    baths = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form_control  form-control ', 'min': 0, 'placeholder': ' Number of baths'}),required=True
    )
    beds = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form_control form-control ', 'min': 0, 'placeholder': 'Number of beds'}),required=True
    )
    


class BNBLocationForm(forms.Form):
    map_location = lat = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control','id':'location_area', 'placeholder': 'Enter the location name'})
    )
    lat = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'id':'latitude', 'readonly':True, 'name':'form_name', 'placeholder': 'Latitude'})
    )
    long = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'id':'longitude', 'readonly':True,'name':'form_name', 'placeholder': 'Longitude'})
    )


class BnBAmenitiesForm(forms.ModelForm):
    
    class Meta:
        model = PropertyAmenity
        fields = ['amenity']
        widgets = {
            'amenity': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amenity'].queryset = Amenity.objects.all()