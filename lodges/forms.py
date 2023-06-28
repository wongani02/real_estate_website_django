from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from .models import Amenity, LodgeAmenity, Lodge, RoomCategory


class LodgeCreationForm(forms.Form):
    property_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'Name of Lodge'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'Address'})
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'City / District'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form_control form-control','placeholder': 'Tell us about your lodge', 'rows':3})
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form_control','placeholder': 'location area'})
    )
    number_of_room_types = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control form_control inp','min':0, 'placeholder': 'how many room categories do you have? '})
    )
    contact_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form_control form-control', 'placeholder':'Contact email'})
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control','placeholder': 'Contact Number'})
    )


class RoomCreationForm(forms.Form):
    ROOMTYPE = (
        ('Executive', 'Executive'),
        ('Duluxe', 'Duluxe'),
        ('Standard', 'Standard'),
        ('Economy', 'Economy'),
    )
    room_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': ' Room type eg. Duluxe, Presidential...'}),
    required=True
    )
    adults = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form_control form-control ', 'min': 0, 'placeholder': 'number of adults'}),required=True,
    )
    children = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form_control  form-control ', 'min': 0, 'placeholder': ' Number of children'}),required=True
    )
    beds = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form_control form-control ', 'min': 0, 'placeholder': 'Number of beds'}),required=True
    )
    price = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form_control form-control ', 'min': 0, 'placeholder': 'Price per night'}),required=True
    )
    quantity= forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form_control form-control ', 'min': 0, 'placeholder': 'How many of these rooms are availble?'}),required=True
    )


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


RoomFormset = formset_factory(
    form=RoomCreationForm,
    extra=4
)


class MapLocationDetails(forms.Form):
    map_location = lat = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control','id':'location_area', 'placeholder': 'type the location name'})
    )
    lat = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'id':'latitude', 'readonly':True, 'name':'form_name', 'placeholder': 'Latitude'})
    )
    long = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'id':'longitude', 'readonly':True,'name':'form_name', 'placeholder': 'Longitude'})
    )


class LodgeAmenities(forms.ModelForm):
    
    class Meta:
        model = LodgeAmenity
        fields = ['amenity']
        widgets = {
            'amenity': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amenity'].queryset = Amenity.objects.all()


#edit formscountry
class LodgeDetailsEditForm(forms.ModelForm):

    class Meta:
        model=Lodge
        fields = ['name', 'street_name', 'city', 'country', 'description', 'contact_phone', 'contact_email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'Name of Lodge'}),
            'street_name': forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'City / District'}),
            'country': forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'Country'}),
            'description': forms.Textarea(attrs={'class': 'form_control form-control','placeholder': 'Tell us about your lodge', 'rows':3}),
            'contact_email': forms.EmailInput(attrs={'class':'form_control form-control', 'placeholder':'Contact email'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form_control form-control','placeholder': 'Contact Number'})
        }


class LodgeLocationEditView(forms.ModelForm):

    class Meta:
        fields = ['long', 'lat', 'map_location']
        model= Lodge
        widgets = {
            'map_location': forms.TextInput(
                attrs={
                        'class': 'form_control form-control',
                        'id':'location_area',
                        'placeholder': 'Enter the location name'
                    }),

            'lat': forms.TextInput(
                attrs={
                        'class': 'form_control form-control',
                        'id':'latitude', 
                        'readonly':True, 
                        'name':'form_name', 
                        'placeholder': 'Latitude'
                    }) ,

            'long': forms.TextInput(
                attrs={
                        'class': 'form_control form-control',
                        'id':'longitude', 
                        'readonly':True,
                        'name':'form_name', 
                        'placeholder': 'Longitude'
                    }), 
        }


class LodgeRoomsEditForm(forms.ModelForm):

    class Meta:
        model = RoomCategory
        fields = ['room_type', 'adults', 'children', 'beds', 'price_per_night', 'quantity']
        widgets = {
            'room_type': forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': ' Room type eg. Duluxe, Presidential...'}),
            'adults': forms.NumberInput(attrs={'class': 'form_control form-control ', 'min': 0, 'placeholder': 'number of adults'}),
            'children': forms.NumberInput(attrs={'class': 'form_control  form-control ', 'min': 0, 'placeholder': ' Number of children'}),
            'beds': forms.NumberInput(attrs={'class': 'form_control form-control ', 'min': 0, 'placeholder': 'Number of beds'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form_control form-control ', 'min': 0, 'placeholder': 'Price per night'})
        }


#booking form 
class LodgeBookingForm(forms.Form):
    guest_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'Guest full Name'})
    )
    guest_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form_control form-control', 'placeholder':' (this email will be used for your reservation communication)'})
    )
    note = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form_control form-control','placeholder': 'Special requests (optional)', 'rows':3})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['note'].label = 'Special requests cannot be guaranteed – but the property will do its best to meet your needs. You can always make a special request after your booking is complete!'
        self.fields['note'].required = False