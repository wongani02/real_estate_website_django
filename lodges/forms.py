from django import forms
from django.forms.formsets import formset_factory


class LodgeCreationForm(forms.Form):
    property_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'Name of Lodge'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'Address'})
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'city'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form_control form-control','placeholder': 'Tell us about your lodge', 'rows':3})
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form_control','placeholder': 'location'})
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
    room_type = forms.CharField(widget=forms.Select(
        attrs={'class': 'selectpicker'},
        choices=ROOMTYPE,
    ))
    adults = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': 'number of adults'})
    )
    children = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form_control form-control', 'placeholder': ' Number of children'})
    )
    beds = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form_control form-control', 'placeholder': 'Number of beds'})
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form_control form-control', 'placeholder': 'Price per night'})
    )


RoomFormset = formset_factory(
    form=RoomCreationForm,
    extra=4
)