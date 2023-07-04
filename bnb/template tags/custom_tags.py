from django import template

from bnb.models import *
from properties.models import Images

register = template.Library()

@register.simple_tag
def property_images(arg):
    img = None
    # 
    images = Images.objects.filter(property=arg).values('file')
    
    for image in images:
        img = image
    return img


"""
Function returns the verbose name of a model
"""
@register.simple_tag
def verbose_name(arg):
    return arg._meta.verbose_name

"""
Function returns the listing name
"""
@register.simple_tag
def get_listing_name(arg):
    if hasattr(arg, 'title'):
        return arg.title
    elif hasattr(arg, 'name'):
        return arg.name

@register.simple_tag
def model_name(arg):
    return arg.__class.__name__