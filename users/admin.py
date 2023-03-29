from django.contrib import admin
from .models import *

# Testing property categories
from properties.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(PropertyCategory)
