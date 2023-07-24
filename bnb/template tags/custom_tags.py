from django import template
from django.db.models import Min, Max

from bnb.models import *
from lodges.models import RoomCategory
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

@register.simple_tag
def get_room_price(arg):
    result = RoomCategory.objects.filter(lodge__id=arg).aggregate(
        lowest_price=Min('price_per_night'),
        highest_price=Max('price_per_night')
    )

    lowest_price = result['lowest_price']
    highest_price = result['highest_price']

    return '${} - ${}'.format(lowest_price, highest_price)