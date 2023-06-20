from django.urls import path

from properties import views

app_name = 'properties'


urlpatterns = [
    path('', views.PropertiesHome.as_view(), name='home'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('about/', views.AboutUs.as_view(), name='about'),
    path('properties/grid/single/<uuid:pk>/', views.PropertyDetail.as_view(), name='property-single'),
    path('properties/list/', views.PropertyListingList.as_view(), name='all-property-list'),
    path('properties/map/', views.PropertyListingMap.as_view(), name='property-map'),
    path('properties/pricing/', views.PropertyPricing.as_view(), name='property-pricing'),

    # Urls for creating a property listing
    path('create/property/step/1/', views.CreatePropertyListing.as_view(), name='create-listing'),
    path('create/property/step/2/', views.CreatePropertyLocationListing.as_view(), name='create-listing-location'),
    path('create/property/step/3/', views.CreatePropertyMediaListing.as_view(), name='create-media-location'),
    path('redirect/dashboard', views.redirectUser, name='redirect-user'),


    path('listing/edit/<uuid:pk>/', views.EditPropertyListing.as_view(), name='edit-listing'),
    path('listing/delete/<uuid:pk>/', views.DeletePropertyListing.as_view(), name='delete-listing'),
    path('listing/amenity/create/', views.create_amenities, name='create-amenity'),
    path('blog/list/', views.BlogList.as_view(), name='blog-list'),
    path('blog/grid/', views.BlogGrid.as_view(), name='blog-grid'),
    path('blog/blog-detail/<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('agency/list/', views.AgencyList.as_view(), name='agency-list'),
    path('agent/list/', views.AgentList.as_view(), name='agent-list'),
    path('search/simple/', views.SimpleSearch.as_view(), name='simple-search'),
    path('search/advanced/', views.AdvancedSearch.as_view(), name='advanced-search'),
]
