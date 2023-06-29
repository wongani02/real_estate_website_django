from .models import *
from django.db import transaction


class LodgeCreation():
    def __init__(self, request):
        self.session = request.session

        #initialize session for images
        image_ids = self.session.get('img_session') 
        if 'img_session' not in self.session:
            self.image_ids = self.session['img_session'] = []
        self.image_ids = image_ids


    def create_lodge(self, lodge={}, location={}, user_id=None):

        self.lodge_instance = Lodge.objects.create(
            user_id=user_id,
            name=lodge['property_name'],
            contact_email=lodge['contact_email'],
            contact_phone=lodge['contact_number'],
            street_name=lodge['address'],
            city=lodge['city'],
            number_of_room_types=lodge['number_of_room_types'],
            map_location=location['map_location'],
            country='Malawi',
            description=lodge['description'],
            lat=location['lat'],
            long=location['long'],
            # cover_img=,
        )
        return self.lodge_instance.id


    def create_room_categories(self, rooms=[]):
        self.room_ids = []
        for item in rooms:
            self.lodge_room = RoomCategory.objects.create(
                lodge_id=self.lodge_instance.id,
                room_type=item['room_type'],
                adults=item['adults'],
                children=item['children'],
                beds=item['beds'],
                price_per_night=item['price'],
                quantity=item['quantity']
            )
            self.room_ids.append(self.lodge_room.id)

        return self.room_ids
    
    
    def create_rooms(self):

        for room_type_id in self.room_ids:

            room_cat = RoomCategory.objects.get(id=room_type_id)

            num = 0
            while num < room_cat.quantity:
                Room.objects.create(
                    room_category_id=room_type_id,
                )
                num += 1


    def assign_amenities(self, selected=[]):
        amenity_instance = LodgeAmenity.objects.create(
            lodge_id=self.lodge_instance.id,
        )

        for item in selected:
            amenity_instance.amenity.add(item['id'])

    def assign_restrictions(self, selected=[]):
        restriction_instance = LodgeRestrictions.objects.create(
            lodge_id = self.lodge_instance.id
        )

        for item in selected:
            restriction_instance.restriction.add(item['id'])


    def create_cancellation_policy(self, policy_id):
        policy_instance = LodgeCancellationPolicy.objects.create(
            lodge_id=self.lodge_instance.id,
            policy_id=policy_id,
        )


    @transaction.atomic
    def save_image(self, image):
        #save image method
        instance=Image.objects.create(img=image)

        self.session['img_session'].append(instance.id)
        self.session.modified = True
        print(self.session['img_session'])


    def add_images(self, image_id=[]):
        num = 0
        for item in image_id:
            if num == 0:
                LodgeImage.objects.create(
                    lodge_id=self.lodge_instance.id,
                    img_id=item,
                    is_feature=True
                )
            else:
                LodgeImage.objects.create(
                    lodge_id=self.lodge_instance.id,
                    img_id=item,
                    is_feature=False
                )
            num += 1


    def clear_session(self):
        del self.session['img_session']
        del self.session['lodge_details']
        del self.session['lodge_location_details']
        del self.session['lodge_rooms']
        del self.session['lodge_amenites']
        del self.session['lodge_restriction']
        del self.session['lodge_policies']

    