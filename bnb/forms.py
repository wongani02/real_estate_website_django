from django import forms
from .models import Amenity, PropertyAmenity, PropertyType, BNBRoom, BNBImage, Property


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


#edit forms
class BnbDetailsEditForm(forms.ModelForm):

    class Meta:
        fields = ['title', 'property_type', 'contact_email', 'contact_phone', 'description', 'street_name', 'city', 'num_bedrooms', 'price_per_night']
        exclude = ['country', 'long', 'lat', 'host', 'id', 'is_active', 'created_at']
        model=Property
        widgets = {
            'title': forms.TextInput(
                attrs={
                        'class': 'form_control form-control', 
                       'placeholder': 'Name of Bnb'
                    }),

            'property_type': forms.Select(
                attrs={
                        'class': 'form_control form-control', 
                       'placeholder': 'Bnb type'
                    }),

            'contact_email': forms.EmailInput(
                attrs={
                        'class':'form_control form-control', 
                       'placeholder':'Contact email'
                       }),

            'contact_phone': forms.TextInput(
                attrs={
                    'class': 'form_control form-control',
                    'placeholder': 'Contact Number'
                }),

            'description': forms.Textarea(
                attrs={
                    'class': 'form_control form-control', 
                    'placeholder': 'Tell us about your BNB', 'rows':3
                }),

            'street_name': forms.TextInput(
                attrs={
                    'class': 'form_control form-control', 
                    'placeholder': 'Street name'
                    }),

            'city': forms.TextInput(
                attrs={
                    'class': 'form_control form-control', 
                    'placeholder': 'City / District'
                    }),

            'num_bedrooms': forms.NumberInput(
                attrs={
                        'class': 'form-control form_control', 
                       'min': 0,
                       'placeholder': 'How many rooms do you have?'
                    }),

            'price_per_night': forms.NumberInput(
                attrs={
                        'class': 'form-control form_control', 
                       'min': 0,
                       'placeholder': 'Set your price per night'
                    })
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # self.fields['']
            pass


class BnbRoomEditForm(forms.ModelForm):

    class Meta:
        model = BNBRoom
        fields = ['num_adults', 'num_beds', 'num_baths']
        widgets = {
            'num_adults': forms.NumberInput(
                attrs={
                        'class': 'form_control form-control ',
                        'min': 0, 
                        'placeholder': 'Max number of guests'
                        }),

            'num_beds': forms.NumberInput(
                attrs={
                        'class': 'form_control form-control ',
                        'min': 0, 
                        'placeholder': 'Number of beds'
                    }),

            'num_baths': forms.NumberInput(
                attrs={
                        'class': 'form_control  form-control ',
                        'min': 0, 
                        'placeholder': ' Number of baths'
                    })
        }
