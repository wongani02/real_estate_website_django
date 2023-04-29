import django_filters

from properties.models import Property, Districts, Amenities


class AdvancedSearchFilter(django_filters.FilterSet):
    beds = django_filters.NumberFilter(field_name='no_rooms', lookup_expr='iexact')
    baths = django_filters.NumberFilter(field_name='no_baths', lookup_expr='iexact')
    garages = django_filters.NumberFilter(field_name='no_garages', lookup_expr='iexact')
    property_status = django_filters.ChoiceFilter(Property.STATUS)
    property_type = django_filters.ChoiceFilter(Property.PROPERTY_TYPE)
    location = django_filters.ModelChoiceFilter(queryset=Districts.objects.all())
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    area__gt = django_filters.NumberFilter(field_name='area', lookup_expr='gt')
    area__lt = django_filters.NumberFilter(field_name='area', lookup_expr='lt')
    amenities = django_filters.ModelMultipleChoiceFilter(queryset=Amenities.objects.all())

    class Meta:
        model = Property
        fields = [
            'no_rooms', 'no_baths', 'no_garages', 'status',
            'property_type', 'district', 'price', 'compound_area',
            'amenities',
        ] 

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(is_active=True)
    