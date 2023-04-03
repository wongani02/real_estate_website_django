from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail

from ckeditor.fields import RichTextField

import uuid


class User(AbstractUser, PermissionsMixin):

    id = models.UUIDField(
        _("Client ID"), 
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    username = models.CharField(
        _("Client Username"), 
        max_length=30, 
        unique=True, 
        null=False)
    email = models.EmailField(_("CLient Email Address"), unique=True, null=False)
    name = models.CharField(_("Client Full Name"), max_length=40, blank=True)
    is_realtor = models.BooleanField(_("If user is a realtor set it to True"), default=False)
    is_customer = models.BooleanField(_("If user is a customer set it to True"), default=False)
    # is_active = models.BooleanField(_("If user is active set it to True"), default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name',]

    objects = UserManager()

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return '{} - {}'.format(self.username, self.email)
     

class UserType(models.Model):
    CHOICES = (
        ('Realtor', 'Realtor'),
        ('Customer', 'Customer'),
    )
    type = models.CharField(_("Type of user"), max_length=200, choices=CHOICES)

    def __str__(self):
        return self.type
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = RichTextField(null=True)
    profile_img = models.ImageField(
        help_text=_('Profile image'),
        upload_to='profile_imgs',
        null=True,
        blank=True
    ) 
    phone_number = models.CharField(
        help_text=_('phone number'), 
        max_length=10,
        null=True, 
        blank=True
    )
    other_email = models.EmailField(_("other email address"), unique=True, null=True)
    phone_number_2 = models.CharField(
        help_text=_('phone number'), 
        max_length=10,
        null=True, 
        blank=True
    )
    agency_certificate = models.FileField(
        help_text=_('agency certificates'), 
        null=True, 
        blank=True,
        upload_to='agency_certificates'
    )
    realtor_cretificate = models.FileField(
        help_text=_('realtor certificates'),
        upload_to='realtor_certificates', 
        null=True, 
        blank=True,
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}- {}'.format(self.user.username, self.user.email)
