from django.db import models
from django.utils import timezone


#still working on them 
class Lodge(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Lodge'
        verbose_name_plural = 'Lodges'
    
    def __str__(self):
        return self.name


class Room(models.Model):
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, related_name='rooms')
    number = models.IntegerField()
    type = models.CharField(max_length=255)
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    
    def __str__(self):
        return f"{self.lodge.name} - Room {self.number}"


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
        return f"{self.amenity.name} ({self.room.lodge.name} - Room {self.room.number})"


class Picture(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='pictures')
    url = models.URLField()

    class Meta:
        verbose_name = 'Picture'
        verbose_name_plural = 'Pictures'

    def __str__(self):
        return f"{self.room.lodge.name} - Room {self.room.number} Picture"


class Booking(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    num_guests = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"{self.user.username} - {self.room.lodge.name} - Room {self.room.number}"
