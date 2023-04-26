from django import template

from bnb.models import *

register = template.Library()

@register.simple_tag
def property_images(arg):
    # 
    return PropertyImage.objects.filter(property=arg)[:1].values('image')