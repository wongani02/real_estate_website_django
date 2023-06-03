from django.urls import path

from . import views


app_name = 'lodges'

urlpatterns = [
    path('create-lodge/', views.createLodgeView, name='create-lodge'),
    path('lodge-listing/', views.lodgeListingView, name='lodge-listings'),
    path('lodge-detail/<int:pk>/', views.lodgeDetailView, name='lodge-detail'),

    #handlers
    path('create-location-location/', views.createLodgeLocation, name='lodge-location'),
    path('upload-images/', views.fileUploadView, name='file_upload'),
    path('amenties-handler/', views.handleAmenities, name='amenties-handler'),
    path('room-form-handler/', views.handleRoomForm, name='room-form-handler'),
    path('lodge-info-handler/', views.handleLodge, name='lodge-info-handler'),
    path('lodge-documents-and-images/', views.uploadLodgeDocumnetAndImages, name='lodge-documents'),

    #create lodge instance
    path('create-lodge-instance/', views.createLodgeInstanceView, name='create-lodge-instance'),
]