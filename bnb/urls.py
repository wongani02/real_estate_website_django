from django.urls import path

from bnb import views


app_name = 'bnb'


urlpatterns = [
    path('listing/', views.BnbList.as_view(), name='bnb-list'),
    path('bnb/<uuid:pk>/', views.BnbDetail.as_view(), name='bnb-detail'),
    path('search/simple/', views.SimpleSearch.as_view(), name='simple-search'),
]