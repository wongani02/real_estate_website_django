from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import RoomCategory, Booking


# @receiver(post_save, sender=RoomCategory)
# def post_save_create_rooms(sender, instance, created, *args, **kwargs):
#     if created:
#         print('here')
        # num = 0
        # while num < instance.quantity:
        #     Room.objects.create(
        #         room_category_id=instance.id,
        #     )
        #     num += 1


# @receiver(post_save, sender=Booking)
# def validate_booking_availability(sender, instance, created, *args, **kwargs):
#     if created:
#         availability = instance.check_booking_availability()
#         print('checking')
#         print(availability)
#         if not availability:
#             booking = Booking.objects.filter(id=instance.id)
#             booking.update(is_active=False)
#             raise ValueError("The room is already booked for the selected dates.")

