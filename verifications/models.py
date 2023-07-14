from django.db import models
from django.utils.translation import gettext_lazy as _

from properties.models import Property
from bnb.models import Property as BnB
from lodges.models import Lodge

from ckeditor.fields import RichTextField


class Listing(models.Model):
    class Meta:
        verbose_name = 'Do Not Edit This'
        verbose_name_plural = 'Do Not Edit This'

    VERIFIED = 'VERIFIED'
    PENDING = 'PENDING'
    DECLINED = 'DECLINED'

    VERIFICATION = [
        (VERIFIED, _("Verified")),
        (PENDING, _("Pending")),
        (DECLINED, _("Declined"))
    ]

    verification = models.CharField(
        _("Verification Status"), choices=VERIFICATION, default=PENDING, max_length=10,
        help_text="Please review property prior selection of this option."
    )
    reason = RichTextField(_("Reason for Verification Decline"))
    date_sub = models.DateTimeField(_("Date Submitted for Verification"), auto_now=True)
    date_ver = models.DateTimeField(_("Date Verified"),)

    def __str__(self):
        return 'Do not edit this.'


class PropertyListing(Listing):
    class Meta:
        verbose_name = 'Property Listing'
        verbose_name_plural = 'Property Listings'

    ver_id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.property.name, self.verification, self.date_sub, self.date_ver)


class BnBListing(Listing):
    class Meta:
        verbose_name = 'BnB Listing'
        verbose_name_plural = 'BnB Listings'

    ver_id = models.AutoField(primary_key=True)
    property = models.ForeignKey(BnB, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.property.title, self.verification, self.date_sub, self.date_ver)



class LodgeListing(Listing):
    class Meta:
        verbose_name = 'Lodge Listing'
        verbose_name_plural = 'Lodge Listings'

    ver_id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Lodge, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.property.name, self.verification, self.date_sub, self.date_ver)

