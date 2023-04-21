from django.urls import path

from . import views


app_name = 'lodges'

urlpatterns = [
    path('create-lodge/', views.createLodgeView, name='create-lodge'),

    #handlers
    path('upload-images/', views.fileUploadView, name='file_upload'),
    path('amenties-handler/', views.handleAmenities, name='amenties-handler'),
    path('room-form-handler/', views.handleRoomForm, name='room-form-handler'),
    path('lodge-info-handler/', views.handleLodge, name='lodge-info-handler'),
]