from django.db.models.query import QuerySet
import qrcode
import uuid
import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files import File
from django.core.files.base import ContentFile

from io import BytesIO
from PIL import Image, ImageDraw

from properties.models import Districts


User = settings.AUTH_USER_MODEL


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
    

class ActiveBNBManager(models.Manager):

    def get_queryset(self):
        return super(ActiveBNBManager, self).get_queryset().filter(is_active=True)


class Property(models.Model):
    id=models.UUIDField(_("BNB ID"), primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_("BnB Name"), max_length=255)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    contact_email = models.EmailField(_('contact email'), null=True)
    contact_phone = models.CharField(_('contact phone number'), max_length=12, null=True)
    description = models.TextField(_("BnB Description"), )
    street_name = models.CharField(_("Address"), max_length=255)
    max_num_of_guests = models.PositiveSmallIntegerField(default=2, null=True)
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

    objects = models.Manager()
    active_bnb = ActiveBNBManager()

    def __str__(self):
        return self.title
    

class BNBRoom(models.Model):
    bnb = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, related_name='bnb_rooms')
    num_adults = models.PositiveIntegerField(_("Number of Adults"), null=True)
    num_beds = models.PositiveIntegerField(_("Number of Beds"), null=True)
    num_baths = models.DecimalField(_("Number of Bathrooms"), max_digits=3, decimal_places=1, null=True)

    def __str__(self):
        return f'{self.bnb.title} hosted by {self.bnb.host}'
    

class Restrictions(models.Model):
    restriction = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.restriction}'
    
    class Meta:
        verbose_name = 'Restrictions'
        verbose_name_plural = 'Restrictions'


class BNBRestrictions(models.Model):
    bnb = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, related_name='bnb_restriction')
    restriction = models.ManyToManyField(Restrictions, related_name='bnb_restr')

    class Meta:
        verbose_name = 'BNB Restrictions'
        verbose_name_plural = 'BNB Restrictions' 

    def __str__(self):
        return f'{self.bnb.title}'


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ManyToManyField(Amenity, related_name='bnb_amenities')


class BNBImage(models.Model):
    image =  models.ImageField(upload_to='property_images/')


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bnb_image')
    image = models.ForeignKey(BNBImage, on_delete=models.CASCADE, null=True, blank=True, )
    is_feature = models.BooleanField(_("Featured"), default=False)

    def __str__(self):
        return f"{self.property} - {self.id}"
    

class Policy(models.Model):
    policy = models.TextField(null=True)

    def __str__(self):
        return f'policy {self.id}'


class BNBCancellationPolicy(models.Model):
    bnb = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, related_name='bnb_policies')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.bnb.title}'


class LodgeReview(models.Model):
    bnb = models.ForeignKey(Property, null=True, on_delete=models.CASCADE, related_name='user_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='bnb_user_reviews')
    review = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username}\'s review for - {self.bnb.title}'


class ActiveBookingsManager(models.Manager):

    def get_queryset(self):
        super(ActiveBookingsManager, self).get_queryset().filter(is_active=True)


class CancelledBookingsManager(models.Manager):

    def get_queryset(self):
        return super(CancelledBookingsManager, self).get_queryset().filter(cancelled=True)
    

class CheckedInBookingsManager(models.Manager):

    def get_queryset(self):
        return super(CheckedInBookingsManager, self).get_queryset().filter(checked_in=True)


class Booking(models.Model):
    id=models.UUIDField(_("BNB BOOKING ID"), primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='user_bnb_booking')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, related_name='bnb_bookings')
    email = models.EmailField(null=True)
    full_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    check_in = models.DateField(null=True)
    check_out = models.DateField(null=True)
    num_guests = models.PositiveIntegerField(_("Number of Guests"), null=True)
    number_of_nights = models.PositiveSmallIntegerField(default=1, null=True)
    note = models.TextField(null=True, help_text='leave a special note, eg we might arrive late')
    is_active = models.BooleanField(null=True, default=True)
    checked_in = models.BooleanField(null=True, default=False)
    cancelled = models.BooleanField(null=True, default=False)
    qr_code = models.ImageField(upload_to='bnb_qr_codes/', null=True, blank=True)
    ref_code = models.CharField(max_length=10, null=True, blank=True)
    is_paid = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=True, null=True)

    #model managers
    objects = models.Manager()
    active_bookings = ActiveBookingsManager()
    cancelled_bookings = CancelledBookingsManager()
    checked_in_bookings = CheckedInBookingsManager()

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"
    

    def save(self, *args, **kwargs):

        #QR code
        # qr_code_img = self.generate_qr_code()
        # frame = f'qr_code-{self.user.name}'+'.png'
        # self.qr_code.save(frame, File(qr_code_img), save=False)

        #validate booking
        self.validate_booking()

        super().save(*args, **kwargs)
    

    def generate_qr_code(self):
        # taking the logo image 
        Logo_link = staticfiles_storage.path('images/header-logo3.png')
        logo = Image.open(Logo_link)
        # taking base width
        basewidth = 100
        # adjust image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        # taking data
        data = f'{self.user.name}'
        # adding data to QRcode
        QRcode.add_data(data)
        # generating QR code
        QRcode.make()
        # taking color 
        QRcolor = 'Blue'
        # adding color to QR code
        QRimg = QRcode.make_image(
            fill_color=QRcolor, back_color="white").convert('RGB')
        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
            (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)
        # save the QR code generated
        file_stream = BytesIO()
        QRimg.save(file_stream, 'PNG')
        file_stream.seek(0)
        return file_stream
    
    def validate_booking(self):
        availability_list = []
        booking_list = Booking.objects.filter(property=self.property.id)
        for booking in booking_list:
            if booking.check_in >self.check_out or booking.check_out <self.check_in:
                availability_list.append(True)
            else:
                availability_list.append(False)

        return all(availability_list)
        

