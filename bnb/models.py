from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


#still workinf on the tables 
class PropertyType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    num_guests = models.IntegerField()
    num_bedrooms = models.IntegerField()
    num_beds = models.IntegerField()
    num_baths = models.DecimalField(max_digits=3, decimal_places=1)
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
    num_guests = models.IntegerField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"

