from django.urls import path

from bnb import views


app_name = 'bnb'


urlpatterns = [
    path('listing/', views.BnbList.as_view(), name='bnb-list'),
    path('bnb/<uuid:pk>/', views.BnbDetail.as_view(), name='bnb-detail'),
    path('search/simple/', views.SimpleSearch.as_view(), name='simple-search'),

    #create bnb
    path('create/step-1/', views.bnbDetailsView, name='bnb-details-create'),
    path('create/step-2/', views.bnbLocationView, name='bnb-location'),
    path('create/step-3/', views.bnbRoomCreateView, name='bnb-room'),
    path('create/step-4/', views.bnbAmenitiesView, name='bnb-amenities-add'),
    path('create/step-5/', views.bnbImagesView, name='bnb-images-add'),

    #handler
    path('bnb-images/upload', views.bnbImageHandler, name='bnb-image-handler'),
    path('create-bnb-instance/', views.createBNBInstance, name='bnb-create-instance'),
]