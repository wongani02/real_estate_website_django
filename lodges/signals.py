from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import *


@receiver(post_save, sender=RoomCategory)
def post_save_create_rooms(sender, instance, created, *args, **kwargs):
    if created:
        print('here')
        # num = 0
        # while num < instance.quantity:
        #     Room.objects.create(
        #         room_category_id=instance.id,
        #     )
        #     num += 1

