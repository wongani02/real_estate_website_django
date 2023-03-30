from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Property, Amenities
from .forms import PropertyCreationForm


def create_amenities(*args, **kwargs):
    print("post_save")
    print("args: ", args)
    print("kwargs: ", kwargs)

    # Get amenity data from hightlights form
    # amenity_form = AmenitiesCreationForm(request.POST)

    # # Process amenities form before property creation form
    # # Inorder to obtain the amenity id required for properties
    # if amenity_form.is_valid():
    #     print("Valid")
    #     _id = amenity_form.custom_save()

# @receiver(post_save, user=Amenities)
# def create_property(user, instance, created, **kwargs):
#     if created:
#         print("instance: ", instance)
#         print("kwargs: ", kwargs)
#         # Process property creation form
        # Get data from property creation form
        # property_form = PropertyCreationForm(request.POST)
        # print("request: ", request.POS)

        # print("property_form: ", property_form)
        
        # if property_form.is_valid():
        #     property_form.custom_save(_id)
