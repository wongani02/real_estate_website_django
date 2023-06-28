from django import template

from properties.models import PropetyViews
from bnb.models import BnbViews
from lodges.models import LodgesViews

register = template.Library()

# A function that returns the number of properties 
@register.simple_tag
def number_of_properties(arg):
    # Return number of properties from Location `arg`
    return PropetyViews.objects.filter(property__id=arg).count()

# A function that returns the number of properties 
@register.simple_tag
def number_of_lodges(arg):
    # Return number of properties from Location `arg`
    return LodgesViews.objects.filter(property__id=arg).count()

# A function that returns the number of properties 
@register.simple_tag
def number_of_bnbs(arg):
    # Return number of properties from Location `arg`
    return BnbViews.objects.filter(property__id=arg).count()
