from django.urls import path

from bnb import views


app_name = 'bnb'


urlpatterns = [
    path('listing/', views.BnbList.as_view(), name='bnb-list'),
    path('bnb/<uuid:pk>/', views.BnbDetail.as_view(), name='bnb-detail'),
    path('search/simple/', views.SimpleSearch.as_view(), name='search'),

    #create bnb
    path('create/step-1/', views.bnbDetailsView, name='bnb-details-create'),
    path('create/step-2/', views.bnbLocationView, name='bnb-location'),
    path('create/step-3/', views.bnbRoomCreateView, name='bnb-room'),
    path('create/step-4/', views.bnbAmenitiesView, name='bnb-amenities-add'),
    path('create/step-5/', views.bnbImagesView, name='bnb-images-add'),

    #handler
    path('bnb-images/upload', views.bnbImageHandler, name='bnb-image-handler'),
    path('create-bnb-instance/', views.createBNBInstance, name='bnb-create-instance'),

    #edit 
    path('bnb/edit/<uuid:pk>/', views.editOptionsview, name='edit-options'),
    path('bnb/edit/<uuid:pk>/edit-details/', views.editDetailsView, name='edit-details'),
    path('bnb/edit/<uuid:pk>/location/', views.editLocationView, name='edit-location'),
    path('bnb/edit/<uuid:pk>/images/', views.editImagesView, name='edit-images'),
    path('bnb/edit/<uuid:pk>/rooms/', views.editRoomsView, name='edit-rooms'),
    path('edit/<uuid:pk>/amenities/', views.editAmenitiesView, name='edit-amenities'),
    path('edit/<uuid:pk>/policies/', views.editPoliciesView, name='edit-policies'),
]