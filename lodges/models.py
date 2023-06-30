import uuid
import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.http import HttpResponseRedirect


class ActiveLodgeManager(models.Manager):

    def get_queryset(self):
        return super(ActiveLodgeManager, self).get_queryset().filter(is_active=True)


class Lodge(models.Model):
    VERIFIED = 'VERIFIED'
    PENDING = 'PENDING'
    DECLINED = 'DECLINED'
    
    VERIFICATION = [
        (VERIFIED, _("Verified")),
        (PENDING, _("Pending")),
        (DECLINED, _("Declined"))
    ]

    class Meta:
        verbose_name = 'Lodge'
        verbose_name_plural = 'Lodges'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    contact_email = models.EmailField(_('contact email'), null=True)
    contact_phone = models.CharField(_('contact phone number'), max_length=13, null=True)
    street_name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    map_location = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, default='Malawi')
    description = RichTextField(null=True)
    number_of_room_types = models.PositiveSmallIntegerField(null=True, default=2)
    lat = models.CharField(max_length=255, null=True)
    long = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, null=True)
    verification = models.CharField(_("Verification Status"), choices=VERIFICATION, default=PENDING, max_length=10)

    objects = models.Manager()
    active_lodges = ActiveLodgeManager()


    class Meta:
        verbose_name = 'Lodge'
        verbose_name_plural = 'Lodges'
        ordering = ['-created_at',]
    
    def __str__(self):
        return self.name


class RoomCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=255, null=True)
    adults = models.PositiveSmallIntegerField(default=2, null=True)
    children = models.PositiveSmallIntegerField(default=1, null=True)
    beds = models.PositiveSmallIntegerField(default=1, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(
        default=True, 
        null=True, 
        help_text='How many of these rooms are there?'
    )

    class Meta:
        verbose_name = 'Room Categry'
        verbose_name_plural = 'Rooms Categories'
    
    def __str__(self):
        return f"{self.lodge.name} - Room {self.room_type}"


'''custom room manager to return available rooms only'''
class AvailableRoomManager(models.Manager):

    def get_queryset(self):
        return super(AvailableRoomManager, self).get_queryset().filter(is_booked=False)


class Room(models.Model):
    room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, null=True, related_name='room_s')
    is_booked = models.BooleanField(null=True, default=False)

    objects = models.Manager()
    available = AvailableRoomManager()

    def __str__(self):
        return f'{self.id} Lodge: {self.room_category.lodge.name} - Room Category: {self.room_category.room_type} - Booked: {self.is_booked} '


class Restrictions(models.Model):
    restriction = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.restriction}'
    
    class Meta:
        verbose_name = 'Restrictions'
        verbose_name_plural = 'Restrictions'


class LodgeRestrictions(models.Model):
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, null=True, related_name='lodge_restriction')
    restriction = models.ManyToManyField(Restrictions, related_name='lodge_restr')

    class Meta:
        verbose_name = 'Lodge Restrictions'
        verbose_name_plural = 'Lodge Restrictions' 

    def __str__(self):
        return f'{self.lodge.name}'


class Amenity(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'

    def __str__(self):
        return self.name


class LodgeAmenity(models.Model):
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, null=True, related_name='amenities')
    amenity = models.ManyToManyField(Amenity, related_name='lodge_amenities')

    class Meta: 
        verbose_name = 'Lodge Amenity'
        verbose_name_plural = 'Lodge Amenities'

    def __str__(self):
        return f"{self.amenity.name} ({self.lodge.name} - Room {self.lodge.city})"
    

class ActivePolicyManager(models.Manager):

    def get_queryset(self):
        return super(ActivePolicyManager, self).get_queryset().filter(is_active=True)
    

class Policy(models.Model):
    policy_title = models.CharField(max_length=500,null=True)
    policy_description = RichTextField(null=True)
    number_of_days = models.PositiveSmallIntegerField(
        help_text='number of days before check in acceptable for booking cancellation',
        default=1,
        )
    is_active = models.BooleanField(default=True)

    active_policy_manager  = ActivePolicyManager()

    def __str__(self):
        return f'{self.policy_title} \n {self.policy_description}'


class LodgeCancellationPolicy(models.Model):
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, null=True, related_name='lodge_policies')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.lodge.name}'


class LodgeReview(models.Model):
    lodge = models.ForeignKey(Lodge, null=True, on_delete=models.CASCADE, related_name='lodge_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='user_reviews')
    review = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username}\'s review for - {self.lodge.name}'


class Image(models.Model):
    img =  models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a lodge image"),
        upload_to="lodge_images/",
        default="images/default.png",
    )

    def __str__(self):
        return f'{self.id}'


class LodgeImage(models.Model):
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, null=True, related_name='pictures')
    img = models.ForeignKey(Image, related_name='image', on_delete=models.CASCADE, null=True)
    is_feature = models.BooleanField(_("Featured"), default=False, null=True)

    class Meta:
        verbose_name = 'Picture'
        verbose_name_plural = 'Pictures'

    def __str__(self):
        return f"{self.lodge.name} - Room {self.lodge.city} Picture"


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    # lodge = models.ForeignKey(Lodge, null=True, on_delete=models.CASCADE, related_name='lodge_bookings')
    email = models.EmailField(null=True)
    full_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_bookings', null=True)
    check_in = models.DateField(null=True)
    check_out = models.DateField(null=True)
    num_guests = models.IntegerField(null=True, blank=True, default=1)
    number_of_nights = models.PositiveSmallIntegerField(default=1, null=True)
    number_of_rooms = models.PositiveSmallIntegerField(default=1, null=True)
    note = models.TextField(null=True, blank=True, help_text='leave a special note, eg we might arrive late')
    is_active = models.BooleanField(null=True, default=True)
    checked_in = models.BooleanField(null=True, default=False)
    cancelled = models.BooleanField(null=True, default=False)
    qr_code = models.ImageField(upload_to='bnb_qr_codes/', null=True, blank=True)
    ref_code = models.CharField(max_length=10, null=True, blank=True)
    is_paid = models.BooleanField(default=False, null=True)
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, editable=False)

    objects = models.Manager()
    active_bookings = ActiveBookingsManager()
    cancelled_bookings = CancelledBookingsManager()
    check_in_bookings = CheckedInBookingsManager()
   
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'


    def __str__(self):
        return f"{self.user.username} -  - Room "
    

    def save(self, *args, **kwargs):
        
        # check room availability
        availability = self.check_booking_availability()

        # return value error if the room is already booked
        if not availability:
            return ValueError("The room is already booked for the selected dates.")
        
        # update room status when room has been booked
        # self.update_availablity()
        super().save(*args, **kwargs)
    

    def check_booking_availability(self):
        availability_list = []
        booking_list = Booking.objects.filter(room=self.room.id)
        for booking in booking_list:
            if booking.check_in >self.check_out or booking.check_out <self.check_in:
                availability_list.append(True)
            else:
                availability_list.append(False)

        return all(availability_list)
    

    # method to update room availability
    def update_availablity(self):
        Room.available.filter(id=self.room.id).update(is_booked=True)

    
class Guests(models.Model):
    booking = models.ForeignKey(Booking, null=True, on_delete=models.CASCADE, related_name='lodge_guests')
    full_name = models.CharField(null=True, max_length=300)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=14, null=True)

    def __str__(self):
        return f'{self.full_name} - {self.phone_number}'


#blog tables
class BlogCategory(models.Model):
    name = models.CharField(max_length=300, null=True)
    slug = models.SlugField(unique=True, null=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        pass
        # return reverse('', args=[self.slug])


class BlogPost(models.Model):
    title = models.CharField(max_length=500, null=True)
    sub_title = models.CharField(max_length=10000, null=True, blank=True)
    category = models.ManyToManyField(BlogCategory, related_name='blog_cats')
    content = RichTextField(null=True)
    cover_img = models.ImageField(upload_to='blog_cover_img/', null=True)
    author = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(
        verbose_name=_("blog visibility"),
        help_text=_("Change blog visibility"),
        default=True,
    )
    slug = models.SlugField(unique=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class BlogImage(models.Model):
    """
    blog Image table.
    """

    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="blog_images")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a blog image"),
        upload_to="blog_images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


#contact table
class About(models.Model):
    company_name = models.CharField(max_length=600, null=True, help_text="Name of your company")
    logo = models.ImageField(null=True, blank=True, upload_to='logo/')
    instagram_link = models.URLField(null=True, blank=True, help_text="link to your instagram")
    twitter_link = models.URLField(null=True, blank=True, help_text="link to your twitter")
    facebook_link = models.URLField(null=True, blank=True, help_text="link to your facebook")
    whatsapp_link = models.URLField(null=True, blank=True, help_text="link to your what's app")
    about_text = RichTextField(null=True, help_text="what is your company like? mission, values etc..")
    phone_number = models.CharField(max_length=10, null=True, blank=True, help_text="your phone number")
    other_number = models.CharField(max_length=10, null=True, blank=True, help_text="other phone number")
    email = models.EmailField(null=True, blank=True, help_text="your email")
    address = models.CharField(max_length=300, blank=True, null=True)
    district = models.CharField(null=True, max_length=300, help_text="where are you based?")
    location = models.CharField(max_length=300, null=True, help_text="eg area 18")

    class Meta:
        verbose_name = _("About  Us")
        verbose_name_plural = _("About Us")

    def __str__(self):
        return 'do not add, just edit this one'


class LodgesViews(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Lodge, on_delete=models.CASCADE, related_name='lodges_views')
    date = models.DateField(auto_now=True)
    views = models.PositiveIntegerField(default=0)