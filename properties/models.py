import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core import settings


# Specify location to save images
def image_upload_path(instance, filename):
    return settings.MEDIA_ROOT + '/images/{0}/{1}'.format(instance.property.name, filename)

# Specify location to save images
def video_upload_path(instance, filename):
    return settings.MEDIA_ROOT + 'videos/{0}/{1}'.format(instance.property.name, filename)


# Images table
class Images(models.Model):
    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    image = models.ImageField(_("Property Image"), upload_to=image_upload_path)
    is_active = models.BooleanField(_("Is Active"), default=True)
    date = models.DateTimeField(_("Date Uploaded"), auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.image, self.date)


# Videos table
class Videos(models.Model):
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    video = models.FileField(_("Property Video"), upload_to=video_upload_path)
    date = models.DateTimeField(_("Date Uploaded"), auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.video, self.date)


# Amenities table
class Amenities(models.Model):
    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'

    s_pool = models.BooleanField(_("Swimming Pool"), default=False)
    a_conditioning = models.BooleanField(_("Air Conditioning"), default=False)
    dining_room = models.BooleanField(_("Dining Room"), default=False)
    laundry = models.BooleanField(_("Laundry"), default=False)
    wifi = models.BooleanField(_("Wi-Fi"), default=False)
    neighbourhood_w = models.BooleanField(_("Neighborhood Watch"), default=False)
    gym = models.BooleanField(_("Gym"), default=False)
    living_room = models.BooleanField(_("Living Room"), default=False)


# Property Status table
class PropertyStatus(models.Model):
    class Meta:
        verbose_name = 'Property Status'
        verbose_name_plural = 'Property Statuses'

    _type = models.CharField(_("Property Type"), max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return self._type


# Property Type table
class PropertyCategory(models.Model):
    class Meta:
        verbose_name = 'Property Category'
        verbose_name_plural = 'Property Categories'

    name = models.CharField(_("Category Name"), max_length=50)

    def __str__(self):
        return self.name


# Districts table
class Districts(models.Model):
    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    district_name = models.CharField(_("District Name"), max_length=50)
    is_active = models.BooleanField(_("Active"))

    def __str__(self):
        return self.district_name


# Nearby Places table
class NearbyPlaces(models.Model):
    class Meta:
        verbose_name = 'Nearby Place'
        verbose_name_plural = 'Nearby Places'

    name_of_place = models.CharField(_("Name of Place"), max_length=100)
    location = models.CharField(_("Location"), max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.name_of_place, self.location)


# Likes table
class Likes(models.Model):
    class Meta:
        verbose_name = 'Likes'
        verbose_name_plural = 'Likes'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='user_likes')
    date = models.DateTimeField(_("Date Liked"), auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.property, self.date)

# Property table
class Property(models.Model):
    SALE = "SALE"
    RENT = "RENT"
    SOLD = "SOLD"
    AVAILABLE = "AVAILABLE"
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    PROPERTY_TYPE = [
        (SALE, _("Sale")),
        (RENT, _("Rent")),
    ]

    STATUS = [
        (SOLD, _("Sold")),
        (AVAILABLE, _("Available")),
    ]

    id = models.UUIDField(_("Property ID"), primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name of Property"), max_length=100)
    price = models.PositiveIntegerField(_("Property Price"))
    location_area = models.CharField(_("Property Location Area"), max_length=100)
    lat = models.CharField(_("Latitude"), max_length=999)
    lon = models.CharField(_("Longitude"), max_length=999)
    images = models.ForeignKey(Images, on_delete=models.CASCADE)
    videos = models.ForeignKey(Videos, on_delete=models.CASCADE)
    likes = models.ForeignKey(Likes, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(_("Number of Views"))
    is_paid = models.BooleanField(_("Paid"), default=False)
    is_active = models.BooleanField(_("Active"), default=True)
    property_cat = models.ForeignKey(PropertyCategory, on_delete=models.DO_NOTHING)
    property_type = models.CharField(_("Property Type"), choices=PROPERTY_TYPE, default=RENT, max_length=7)
    status = models.CharField(_("Available/Sold"), choices=STATUS, default=AVAILABLE)
    amenities = models.ForeignKey(Amenities, on_delete=models.DO_NOTHING)
    year_built = models.DateField(_("Year Built"),)
    compound_area = models.PositiveIntegerField(_("Property Compound Area (metres)"))
    no_garages = models.PositiveIntegerField(_("Number of Garages"))
    no_rooms = models.PositiveIntegerField(_("Number of Rooms"))
    no_baths = models.PositiveIntegerField(_("Number of Baths"))
    desc = models.TextField(_("Description"))
    nearby_places = models.ForeignKey(NearbyPlaces, on_delete=models.DO_NOTHING)
    status = models.BooleanField(_("Property Status"),)
    district = models.ForeignKey(Districts, on_delete=models.DO_NOTHING)
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='agent_properties')

    def __str__(self):
        return '{} - {} - {}'.format(self.name, self.price, self.location_area)


