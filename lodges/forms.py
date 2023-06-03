from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from .models import Amenity, LodgeAmenity


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