from django.utils import timezone

from properties.models import TempImageStore, TempDocumentStore
from properties.utils import verification_status
from bnb.models import Booking as BnbBooking
from lodges.models import Booking as LodgeBooking
from datetime import datetime, timedelta

import os

def delete_temp_media():
    # calculate the threshold (7 days ago)
    threshold_date = datetime.now() - timedelta(days=7)

    # make the time aware of the current timezone
    threshold_date = timezone.make_aware(threshold_date, timezone.get_current_timezone())

    # get the old images from the database
    old_images = TempImageStore.objects.filter(date__lt=threshold_date)

    # get the old documnets from the database
    old_docs = TempDocumentStore.objects.filter(date__lt=threshold_date)

    # delete old images from the database and file system
    for media in [old_images, old_docs]:
        # call delete function of the model and file
        media.delete()


def ticket_expiry_notification():
    # create a tickets object
    tickets = []

    # get all tickets that are active, have not been cancelled, and have not been checked in
    # and users that have not been notified of the ticket status
    for ticket in [BnbBooking, LodgeBooking]:
        tickets.extend(
            ticket.objects.filter(is_active=True, cancelled=False, checked_in=False, is_notified=False)
        )

    # get tickets and send users an email
    for obj in tickets:
        # send email to user
        verification_status(
            to_email=obj.user.email, p_name=obj.property, client=obj.user, ticket=obj
        )
        print("eamil sent")
