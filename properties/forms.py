from django import forms
from django.utils.translation import gettext_lazy as _

from properties.models import * 


class PropertyCreationForm(forms.ModelForm):
    f=PropertyCategory.objects.all()
    class Meta:
        model = Property
        fields = ['name',
            #       'property_type', 'status', 'property_cat', 'no_garages','no_rooms', 'no_baths',
            # 'year_built', 'property_area', 'price', 'addr', 'district', 
            # 'amenities', 
        ]
        # widgets = {
        #     'property_type': forms.Select(choices=Property.PROPERTY_TYPE, attrs={
        #         'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Type',
        #     }),
        #     'status': forms.Select(choices=Property.STATUS, attrs={
        #         'class': 'selectpicker', 'data-width': '100%', 'data-live-search': 'true', 'title': 'Property Status', 
        #     }),
        #     'property_cat': forms.Select(choices=PropertyCategory.objects.all(), attrs={
        #         'class': 'selectpicker', 'data-width': '82%', 'data-live-search': 'true', 'title': 'Property Category',
        #     }),
        #     'year_built': forms.DateInput(attrs={
        #         'type': 'date', 'class': 'form-control form_control'
        #     }),
        #     'district': forms.Select(choices=Districts.objects.all(), attrs={
        #         'class': 'selectpicker', 'data-width': '85%', 'data-live-search': 'true',
        #         'title': 'Village'
        #     })
        # }

    def custom_save(self, _id):
        p = self.save(commit=False)
        p.amenities = _id.id
        p.save()


class DistrictCreationForm(forms.ModelForm):
    class Meta:
        model = Districts
        fields = ['district_name',]
        widgets ={
            'district_name': forms.TextInput(attrs={
                'class': 'form-control', 'name': 'district_name',
            }),
        }


class NearbyPlacesCreationForm(forms.ModelForm):
    class Meta:
        model = NearbyPlaces
        fields = ['name', 'location',]


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
        fields = '__all__'
        exclude = ['id',]

    def custom_save(self):
        s = self.save(commit=True)
        
        return s


class ImagesCreationForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image',]
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'multiple': True, 'class': 'input-img',
            }),
        }
