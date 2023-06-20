import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse

from core import settings

from ckeditor.fields import RichTextField


# Specify location to save images
def image_upload_path(instance, filename):
    return settings.MEDIA_ROOT + '/images/{0}/{1}'.format(instance.property.name, filename)

# Specify location to save images
def video_upload_path(instance, filename):
    return settings.MEDIA_ROOT + 'videos/{0}/{1}'.format(instance.property.name, filename)


# Amenities table
class Amenities(models.Model):
    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'

    name = models.CharField(_('Amenity Name'), unique=True, max_length=20, blank=True)
    desc = models.CharField(_("Amenity Description"), max_length=100, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

# Property Status table
class PropertyType(models.Model):
    class Meta:
        verbose_name = 'Property Type'
        verbose_name_plural = 'Property Types'

    _type = models.CharField(_("Property Type"), max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self._type
    
    def get_absolute_url(self):
        return reverse('', args=[self.slug])


# Property Type table
class PropertyCategory(models.Model):
    class Meta:
        verbose_name = 'Property Category'
        verbose_name_plural = 'Property Categories'

    name = models.CharField(_("Category Name"), max_length=50)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('', args=[self.slug])


# Districts table
class Districts(models.Model):
    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    district_name = models.CharField(_("District Name"), max_length=50)
    is_active = models.BooleanField(_("Active"))
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.district_name
    
    def get_absolute_url(self):
        return reverse('', args=[self.slug])


# Property table
class Property(models.Model):
    SALE = "SALE"
    RENT = "RENT"
    SOLD = "SOLD"
    AVAILABLE = "AVAILABLE"
    PENDING = 'PENDING'
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
        (PENDING, _("Pending")),
    ]

    id = models.UUIDField(_("Property ID"), primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name of Property"), max_length=100)
    price = models.PositiveIntegerField(_("Property Price"))
    prev_price = models.PositiveIntegerField(_("Previous Property Price"), null=True, blank=True)
    location_area = models.CharField(_("Property Location Area"), max_length=100)
    lat = models.CharField(_("Latitude"), max_length=999, blank=True)
    lon = models.CharField(_("Longitude"), max_length=999, blank=True)
    views = models.PositiveIntegerField(_("Number of Views"), blank=True, default=0)
    eng = models.PositiveIntegerField(_("Number of Engagements"), blank=True, default=0)
    is_paid = models.BooleanField(_("Paid"), default=False)
    is_active = models.BooleanField(_("Active"), default=True)
    property_cat = models.ForeignKey(PropertyCategory, on_delete=models.DO_NOTHING)
    property_type = models.CharField(_("Property Type"), choices=PROPERTY_TYPE, default=RENT, max_length=10)
    property_status = models.CharField(_("Available/Sold"), choices=STATUS, default=AVAILABLE, max_length=10)
    amenities = models.ManyToManyField(Amenities)
    year_built = models.DateField(_("Year Built"), blank=True)
    compound_area = models.PositiveIntegerField(_("Compound Area (metres)"), blank=True, default=0)
    property_area = models.PositiveIntegerField(_("Property Area (metres)"), blank=True, default=0)
    no_garages = models.PositiveIntegerField(_("Number of Garages"), default=0)
    no_rooms = models.PositiveIntegerField(_("Number of Rooms"), default=2)
    no_baths = models.PositiveIntegerField(_("Number of Baths"), default=1)
    desc = RichTextField(_("Description"))
    status = models.BooleanField(_("Property Status"), default=False)
    district = models.ForeignKey(Districts, on_delete=models.DO_NOTHING, related_name='property_district')
    created_at = models.DateTimeField(auto_now=True, null=True)
    is_featured = models.BooleanField(_("if Featured"), default=False, null=True)
    region = models.CharField(_("State/Region"), max_length=100, null=True)
    country = models.CharField(_("Country"), max_length=50, default='MALAWI')
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='agent_properties')
    user_bookmark = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_bookmark", blank=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.name, self.price, self.location_area)



class PropetyViews(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_views')
    date = models.DateField(auto_now=True)
    views = models.PositiveIntegerField(default=0)




# Nearby Places table
class NearbyPlaces(models.Model):
    class Meta:
        verbose_name = 'Nearby Place'
        verbose_name_plural = 'Nearby Places'

    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE, related_name='property_nearby')
    name_of_place = models.CharField(_("Name of Place"), max_length=100, null=True)
    desc = models.TextField(_("Description of place"), null=True)

    def __str__(self):
        return '{} - {}'.format(self.name_of_place, self.desc[:20])


# Images table


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
    date = models.DateTimeField(_("Date Liked"), auto_now=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    count = models.IntegerField(default=1, editable=False)

    def property_name(self):
        return self.property.name
    
    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.property, self.date)



class Images(models.Model):
    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE, related_name='property_images')
    file = models.ImageField(_("Property Image"), upload_to='property_images/', null=True)
    is_feature = models.BooleanField(_("Main image to display"), default=False, null=True)
    is_active = models.BooleanField(_("Is Active"), default=True, null=True)
    date = models.DateTimeField(_("Date Uploaded"), auto_now=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.property.name, self.date)


# Videos table
class Videos(models.Model):
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE, related_name='property_videos')
    is_feature = models.BooleanField(_("Main image to display"), default=False, null=True)
    video = models.FileField(_("Property Video"), upload_to=video_upload_path, null=True)
    link = models.URLField(_("Video URL Link"), null=True)
    date = models.DateTimeField(_("Date Uploaded"), auto_now=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.video, self.date)


class PropertyAmenityLink(models.Model):
    id = models.AutoField(primary_key=True)
    _property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenities, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '{} - {} - {}'.format(self.id, self._property, self.amenity)

