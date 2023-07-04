from properties.models import TempImageStore
from datetime import datetime, timedelta

import os

def delete_temp_images():
    # calculate the threshold (7 days ago)
    threshold_date = datetime().now() - timedelta(days=7)

    # get the old images from the database
    old_images = TempImageStore.objects.filter(date__lt=threshold_date)

    # delete old images from the database and file system
    for image in old_images:
        # call delete function of the model
        image.delete()
