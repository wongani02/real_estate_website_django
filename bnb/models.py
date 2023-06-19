from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from properties.models import Districts

import uuid

User = settings.AUTH_USER_MODEL


#still working on the tables 
class PropertyType(models.Model):
    name = models.CharField(_("Property Type"), max_length=255)

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(_("Amenity Name"), max_length=255)

    class Meta:
        verbose_name = 'Ameneties'
        verbose_name_plural = 'Ameneties'

    def __str__(self):
        return self.name


class RoomType(models.Model):
    name = models.CharField(_("Room Type"), max_length=255)

    def __str__(self):
        return self.name
    

class Property(models.Model):
    id=models.UUIDField(_("BNB ID"), primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_("BnB Name"), max_length=255)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    contact_email = models.EmailField(_('contact email'), null=True)
    contact_phone = models.CharField(_('contact phone number'), max_length=12, null=True)
    description = models.TextField(_("BnB Description"), )
    street_name = models.CharField(_("Address"), max_length=255)
    # city = models.ForeignKey(Districts, on_delete=models.CASCADE, related_name='bnb_city')
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, blank=True)
    num_bedrooms = models.PositiveIntegerField(_("Number of Bed Rooms"), null=True)
    price_per_night = models.DecimalField(_("Price/Night"), max_digits=12, decimal_places=2)
    prev_price = models.DecimalField(_("Previous Price"), max_digits=8, decimal_places=2, blank=True, null=True)
    lat = models.CharField(max_length=255, null=True)
    long = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class BNBRoom(models.Model):
    bnb = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, related_name='bnb_rooms')
    num_adults = models.PositiveIntegerField(_("Number of Adults"), null=True)
    num_beds = models.PositiveIntegerField(_("Number of Beds"), null=True)
    num_baths = models.DecimalField(_("Number of Bathrooms"), max_digits=3, decimal_places=1, null=True)

    def __str__(self):
        return f'{self.bnb.title} hosted by {self.bnb.host}'


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ManyToManyField(Amenity, related_name='bnb_amenities')


class BNBImage(models.Model):
    image =  models.ImageField(upload_to='property_images/')


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bnb_image')
    image = models.ForeignKey(BNBImage, on_delete=models.CASCADE, null=True, blank=True)
    is_feature = models.BooleanField(_("Featured"), default=False)

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

