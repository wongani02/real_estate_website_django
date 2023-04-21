from django.db import models
from django.utils import timezone
from django.conf import settings
from ckeditor.fields import RichTextField


class Lodge(models.Model):
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, default='Malawi')
    description = RichTextField(null=True)
    lat = models.CharField(max_length=255, null=True)
    long = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Lodge'
        verbose_name_plural = 'Lodges'
    
    def __str__(self):
        return self.name


class Room(models.Model):
    ROOMTYPE = (
        ('Executive', 'Executive'),
        ('Duluxe', 'Duluxe'),
        ('Standard', 'Standard'),
        ('Economy', 'Economy'),
    )
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, related_name='rooms')
    type = models.CharField(max_length=255, choices=ROOMTYPE)
    adults = models.PositiveSmallIntegerField(default=2, null=True)
    children = models.PositiveSmallIntegerField(default=1, null=True)
    beds = models.PositiveSmallIntegerField(default=1, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    
    def __str__(self):
        return f"{self.lodge.name} - Room {self.type}"


class Amenity(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'

    def __str__(self):
        return self.name


class RoomAmenity(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='amenities')
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Room Amenity'
        verbose_name_plural = 'Room Amenities'

    def __str__(self):
        return f"{self.amenity.name} ({self.room.lodge.name} - Room {self.room.type})"


class Picture(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='pictures')
    img = models.ImageField(null=True, upload_to='lodge_images/')

    class Meta:
        verbose_name = 'Picture'
        verbose_name_plural = 'Pictures'

    def __str__(self):
        return f"{self.room.lodge.name} - Room {self.room.type} Picture"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    num_guests = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"{self.user.username} - {self.room.lodge.name} - Room {self.room.type}"
