from django.shortcuts import render

from .models import PropertyListing, BnBListing, LodgeListing
from properties.utils import verification_status


"""
Function craates a property listing object which enables backend users to be able to verify property that
has been recently created by the users.
This function must be run once the property object has been created
"""
def create_property_listing(request, property_):
    # get user
    user = None
    try:
        user = property_.agent
    except:
        pass
    try:
        user = property_.user
    except:
        pass
    try:
        user = property_.host
    except:
        pass

    # # create property listing object
    # listing = PropertyListing.objects.create(
    #     property=property_,
    # )
    # listing.save()

    # send user an email notifying them of the property awaiting verification
    verification_status(
        to_email=request.user.email, p_name=property_.name, p_status='pending', client=user, request=request
    )

"""
Function craates a bnb listing object which enables backend users to be able to verify bnbs that
has been recently created by the users.
This function must be run once the bnb object has been created
"""
def create_bnb_listing(request, property_):
    # get user
    user = None
    try:
        user = property_.agent
    except:
        pass
    try:
        user = property_.user
    except:
        pass
    try:
        user = property_.host
    except:
        pass

    # # create property listing object
    # listing = BnBListing.objects.create(
    #     property=property_,
    # )
    # listing.save()

    # send user an email notifying them of the property awaiting verification
    verification_status(
        to_email=request.user.email, p_name=property_.name, p_status='pending', client=user, request=request
    )

"""
Function craates a lodge listing object which enables backend users to be able to verify lodges that
has been recently created by the users.
This function must be run once the lodge object has been created
"""
def create_lodge_listing(request, property_):
    # get user
    user = None
    try:
        user = property_.agent
    except:
        pass
    try:
        user = property_.user
    except:
        pass
    try:
        user = property_.host
    except:
        pass

    # # create property listing object
    # listing = LodgeListing.objects.create(
    #     property=property_,
    # )
    # listing.save()

    # send user an email notifying them of the property awaiting verification
    verification_status(
        to_email=request.user.email, p_name=property_.name, p_status='pending', client=user, request=request
    )
