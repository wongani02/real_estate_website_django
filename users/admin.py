from django.contrib import admin
from .models import *
from tracking_analyzer.models import Tracker

# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
# admin.site.register(UserVisitModel)