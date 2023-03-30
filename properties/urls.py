from django.urls import path

from properties import views

app_name = 'properties'


urlpatterns = [
    path('', views.PropertiesHome.as_view(), name='home'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('about/', views.AboutUs.as_view(), name='about'),
    path('properties/grid/', views.PropertyListingGrid.as_view(), name='all-property-grid'),
    path('properties/list/', views.PropertyListingList.as_view(), name='all-property-list'),
    path('properties/map/', views.PropertyListingMap.as_view(), name='property-map'),
    path('listing/create/dud/', views.dud_func, name='create-dud'),
    path('listing/create/', views.CreatePropertyListing.as_view(), name='create-listing'),
    path('listing/category/create/', views.create_property_category, name='create-category'),
    path('listing/district/create/', views.create_district, name='create-district'),
    path('blog/list/', views.BlogList.as_view(), name='blog-list'),
    path('blog/grid/', views.BlogGrid.as_view(), name='blog-grid'),
    path('agency/list/', views.AgencyList.as_view(), name='agency-list'),
    path('agent/list/', views.AgentList.as_view(), name='agent-list'),
]
