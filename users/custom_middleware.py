from django.middleware.common import CommonMiddleware
from django.shortcuts import redirect
from modified_tracking_analyzer.models import Tracker
from ipware import get_client_ip

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from django.middleware.common import MiddlewareMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_user_agents.utils import get_user_agent

from core import settings
from users.models import Visitor, User
from properties.models import Property
from bnb.models import Property as BnB
from lodges.models import Lodge, About

import requests
import json


class CustomUserVisitMiddleware(SessionMiddleware, MiddlewareMixin):

    def process_request(self, request):
        # track all users other than staff
        
        if not request.user.is_staff:
            # only track users who land on the home or discover page
            if request.META['PATH_INFO'] != reverse('properties:discover') and request.META['PATH_INFO'] != reverse('properties:home'):
                return None

            # get user model data for authenticated user
            if request.user.is_authenticated:
                user_model = User.objects.get(email=request.user.email)
                tracker = Tracker.objects.create_from_request(request, user_model)
            
            # create anonymouse user object for unathenticated users
            else:
                _model = Property.objects.first()

                if _model is None: 
                    # get about object
                    obj = About.object.first()

                    user_model = get_object_or_404(About, pk=obj.pk)
                    
                user_model =  get_object_or_404(Property, pk=_model.pk)

                # create tracker 
                # tracker = Trackevbj , a r.objects.create_from_request(request, user_model)

            # print("Tracker: ", tracker)

            return None


def process_bnb_request(request, pk):
    model_class = BnB

    if model_class is not None:
        model_instance = get_object_or_404(model_class, pk=pk)

        tracker = Tracker.objects.create_from_request(request, model_instance)

        return None

    return None

def process_property_request(request, pk):
    model_class = Property

    if model_class is not None:
        model_instance = get_object_or_404(model_class, pk=pk)

        tracker = Tracker.objects.create_from_request(request, model_instance)

        return None

    return None

def process_lodge_request(request, pk):
    model_class = Lodge

    if model_class is not None:
        model_instance = get_object_or_404(model_class, pk=pk)

        tracker = Tracker.objects.create_from_request(request, model_instance)

        return None

    return None
