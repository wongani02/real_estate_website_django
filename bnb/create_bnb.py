from django.db import transaction

from .models import *


class BNB:
    def __init__(self, request):
        self.session = request.session

        #initialize session for images
        image_ids = self.session.get('bnb_img_session') 
        if 'bnb_img_session' not in self.session:
            self.image_ids = self.session['bnb_img_session'] = []
        self.image_ids = image_ids


    def create_bnb(self, user, bnb={}, location={}):
        self.bnb_instance = Property.objects.create(
            host_id=user,
            title=bnb['property_name'],
            property_type_id=bnb['bnb_type'],
            description=bnb['description'],
            street_name=bnb['street_name'],
            city=bnb['city'],
            country=location['map_location'],
            price_per_night=bnb['price_per_night'],
            contact_phone=bnb['contact_number'],
            contact_email=bnb['contact_email'],
            lat=location['lat'],
            long=location['long']
        )

        return self.bnb_instance.id
    

    def create_rooms(self, rooms=[]):
        for item in rooms:
            room = BNBRoom.objects.create(
                bnb_id=self.bnb_instance.id,
                num_adults=item['adults'],
                num_beds=item['beds'],
                num_baths=item['baths'],
            )
        

    def assign_ameneities(self, selected=[]):
        amenity_instance = PropertyAmenity.objects.create(
            property_id=self.bnb_instance.id,
        )

        for amenity in selected:
            amenity_instance.amenity.add(amenity['id'])


    def assign_restrictions(self, selected=[]):
        restriction_instance = BNBRestrictions.objects.create(
            bnb_id = self.bnb_instance.id
        )

        for item in selected:
            restriction_instance.restriction.add(item['id'])


    def create_cancellation_policy(self, policy_id):
        policy_instance = BNBCancellationPolicy.objects.create(
            bnb_id=self.bnb_instance.id,
            policy_id=policy_id,
        )


    @transaction.atomic
    def save_images(self, image):
        #save image method
        instance=BNBImage.objects.create(image=image)

        self.session['bnb_img_session'].append(instance.id)
        self.session.modified = True
        print(self.session['bnb_img_session'])


    def assign_images(self, image_id=[]):
        num = 0
        for item in image_id:
            if num == 0:
                PropertyImage.objects.create(
                    property_id=self.bnb_instance.id,
                    image_id=item,
                    is_feature=True
                )
            else:
                PropertyImage.objects.create(
                    property_id=self.bnb_instance.id,
                    image_id=item,
                    is_feature=False
                )
            num += 1


    def clear_session(self):
        del self.session['bnb_img_session']
        del self.session['bnb_details']
        del self.session['bnb_location_details']
        del self.session['bnb_amenites']
        del self.session['bnb_rooms']
        del self.session['bnb_policies']
        del self.session['bnb_restriction_details']
        
