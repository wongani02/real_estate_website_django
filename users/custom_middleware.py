from django.middleware.common import CommonMiddleware
from django.shortcuts import redirect
from tracking_analyzer.models import Tracker
from ipware import get_client_ip

from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.common import MiddlewareMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse

from core import settings
from users.models import Visitor

import requests
import json


class CustomUserVisitMiddleware(SessionMiddleware, MiddlewareMixin):

    def process_request(self, request):
        # track all users other than staff
        if request.user.is_staff:
            if request.path == reverse('properties:discover') or request.path == reverse('properties:home'):
                return None

            model_class = None

            if 'Property' in request.path:
                model_class = Property
            elif 'BnB' in request.path:
                model_class = BnB
            elif 'Lodge' in request.path:
                model_instance = Lodge

            if model_class is not None:
                link_url = request.META['HTTP_REFERER']
                model_instance = get_object_or_404(model_class, pk=link_url.split('/')[-2])

                tracker = Tracker.objects.create_from_request(request, model_instance)

                return None

            print("Tracker: ", tracker)

            return None