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


    def create_lodge(self, lodge={}, location={}):
        self.lodge_instance = Lodge.objects.create(
            name=lodge['property_name'],
            address=lodge['address'],
            city=location['map_location'],
            state=lodge['location'],
            country='Malawi',
            description=lodge['description'],
            lat=location['lat'],
            long=location['long'],
            # cover_img=,
        )
        return self.lodge_instance.id


    def create_rooms(self, rooms=[]):
        self.room_ids = []
        for item in rooms:
            self.lodge_room = Room.objects.create(
                lodge_id=self.lodge_instance.id,
                room_type=item['room_type'],
                adults=item['adults'],
                children=item['children'],
                beds=item['beds'],
                price_per_night=item['price'],
            )
            self.room_ids.append(self.lodge_room.id)

        return self.room_ids


    def assign_amenities(self, selected=[]):
        amenity_instance = LodgeAmenity.objects.create(
            lodge_id=self.lodge_instance.id,
        )

        for item in selected:
            amenity_instance.amenity.add(item['id'])


    @transaction.atomic
    def save_image(self, image):
        #save image method
        instance=Image.objects.create(img=image)

        self.session['img_session'].append(instance.id)
        self.session.modified = True
        print(self.session['img_session'])


    def add_images(self, image_id=[]):
        image_instance = LodgeImage.objects.create(
            lodge_id=self.lodge_instance.id,
        )

        for item in image_id:
            image_instance.img.add(item)


    def clear_session(self):
        del self.session['img_session']
        del self.session['lodge_details']
        del self.session['lodge_location_details']
        del self.session['lodge_rooms']
        del self.session['lodge_amenites']

    

