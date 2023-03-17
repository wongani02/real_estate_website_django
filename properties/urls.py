from django.urls import path

from properties import views

app_name = 'properties'


urlpatterns = [
    path('', views.get_home, name='home'),
]
