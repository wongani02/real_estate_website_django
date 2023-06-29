from django.urls import path

from . import views


app_name = 'lodges'

urlpatterns = [
    path('create-lodge/', views.createLodgeView, name='create-lodge'),
    path('lodge-listing/', views.lodgeListingView, name='lodge-listings'),
    path('lodge-detail/<uuid:pk>/', views.lodgeDetailView, name='lodge-detail'),

    #search
    path('search/', views.searchView, name='search'),

    #handlers
    path('create-location-location/', views.createLodgeLocation, name='lodge-location'),
    path('upload-images/', views.fileUploadView, name='file_upload'),
    path('amenties-handler/', views.handleAmenities, name='amenties-handler'),
    path('room-form-handler/', views.handleRoomForm, name='room-form-handler'),
    path('lodge-info-handler/', views.handleLodge, name='lodge-info-handler'),
    path('lodge-info-restrictions/', views.lodgeRestrictions, name='lodge-restrictions'),
    path('lodge-info-policies/', views.lodgePoliciesView, name='lodge-policies'),
    path('lodge-documents-and-images/', views.uploadLodgeDocumnetAndImages, name='lodge-documents'),
    

    #create lodge instance
    path('create-lodge-instance/', views.createLodgeInstanceView, name='create-lodge-instance'),

    #edit lodge
    path('edit/<uuid:pk>/', views.editLodgeOptions, name='edit-options'),
    path('edit/<uuid:pk>/details/', views.editLodgeDetails, name='edit-details'),
    path('edit/<uuid:pk>/rooms/', views.editLodgeRooms, name='edit-rooms'),
    path('edit/<uuid:pk>/location/', views.editLodgeLocation, name='edit-location'),
    path('edit/<uuid:pk>/amenities/', views.editLodgeAmenities, name='edit-amenities'),
    path('edit/<uuid:pk>/images/', views.editLodgeImages, name='edit-images'),
    path('edit/<uuid:pk>/policies/', views.editLodgePolicies, name='edit-policies'),

    #bookings
    path('lodge-detail/<uuid:lodge>/booking/<uuid:room>/<int:qty>/<int:room_list>/', views.bookingDetailsView, name='booking-step-1'),
    path('lodge-detail/<uuid:lodge>/booking/<uuid:room>/<int:qty>/<int:room_list>/payments/', views.bookingPaymentView, name='booking-step-2'),
    path('process-payment/<uuid:lodge>/booking/<uuid:room>/<int:qty>/<int:room_list>/', views.processPaymentView, name='process-payment'),

    #htmx urls
    path('search-rooms/<uuid:lodge>/', views.getAvailableRoomTypes, name='search-available-rooms'),
]