from django.urls import path

from properties import views

app_name = 'properties'


urlpatterns = [
    path('', views.PropertiesHome.as_view(), name='home'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('about/', views.AboutUs.as_view(), name='about'),
    path('properties/', views.PropertyListingGrid.as_view(), name='all-property-grid'),
    path('properties/', views.PropertyListingList.as_view(), name='all-property-list'),
    path('listing/create/', views.CreatePropertyListing.as_view(), name='create-listing'),
    path('blog/list/', views.BlogList.as_view(), name='blog-list'),
    path('blog/grid/', views.BlogGrid.as_view(), name='blog-grid'),
    path('agency/list/', views.AgencyList.as_view(), name='agency-list'),
    path('agent/list/', views.AgentList.as_view(), name='agent-list'),
]
