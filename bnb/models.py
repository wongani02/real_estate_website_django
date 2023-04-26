from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

import uuid

User = settings.AUTH_USER_MODEL


#still workinf on the tables 
class PropertyType(models.Model):
    name = models.CharField(_("Property Type"), max_length=255)

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(_("Amenity Name"), max_length=255)

    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(_("Room Type"), max_length=255)

    def __str__(self):
        return self.name

class Property(models.Model):
    id=models.UUIDField(_("BNB ID"), primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_("BnB Name"), max_length=255)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    description = models.TextField(_("BnB Description"), )
    address = models.CharField(_("Address"), max_length=255)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    price_per_night = models.DecimalField(_("Price/Night"), max_digits=8, decimal_places=2)
    prev_price = models.DecimalField(_("Previous Price"), max_digits=8, decimal_places=2, null=True)
    num_guests = models.PositiveIntegerField(_("Number of Guests"), )
    num_bedrooms = models.PositiveIntegerField(_("Number of Bed Rooms"), )
    num_beds = models.PositiveIntegerField(_("Number of Beds"), )
    num_baths = models.DecimalField(_("Number of Bathrooms"), max_digits=3, decimal_places=1)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"{self.property} - {self.id}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.PositiveIntegerField(_("Number of Guests"))
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"

