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
    path('onboarding/properties/', views.get_onbording, name='property-onboarding'),
    path('create/property/step/1/choice/<str:choice>/', views.CreatePropertyListing.as_view(), name='create-listing'),
    path('create/property/step/2/', views.CreatePropertyLocationListing.as_view(), name='create-listing-location'),
    path('create/property/step/3/', views.CreatePropertyMediaListing.as_view(), name='create-media-location'),
    path('create/property/step/4/', views.CreatePropertyDocuments.as_view(), name='create-documents'),
    path('create/property/step/5/', views.CreatePropertyPolicy.as_view(), name='create-policy'),
    path('redirect/dashboard/ ', views.redirectUser, name='redirect-user'),

    #payment offers
    path('payments/offer/', views.OfferPackage.as_view(), name='offers'),
    path('payment/options/', views.PaymentOptions.as_view(), name='payment-options'),

    # discover
    path('discover/', views.discover, name='discover'),

    # Edit 
    path('listing/edit/<uuid:pk>/', views.editPropertyOptions, name='edit-listing-options'),
    path('listing/edit/<uuid:pk>/details/', views.EditPropertyDetails.as_view(), name='edit-listing-details'),
    path('listing/edit/<uuid:pk>/media/', views.EditPropertyMedia.as_view(), name='edit-listing-media'),
    path('listing/edit/<uuid:pk>/others/', views.EditPropertyLocationAmenities.as_view(), name='edit-listing-others'),
    path('listing/edit/<uuid:pk>/policies/', views.EditPropertyPolicies.as_view(), name='edit-listing-policies'),
    path('listing/edit/<uuid:pk>/documents/', views.EditPropertyDocuments.as_view(), name='edit-listing-documents'),
    
    path('listing/delete/<uuid:pk>/', views.DeletePropertyListing.as_view(), name='delete-listing'),
    path('listing/amenity/create/', views.create_amenities, name='create-amenity'),
    path('blog/list/', views.BlogList.as_view(), name='blog-list'),
    path('blog/grid/', views.BlogGrid.as_view(), name='blog-grid'),
    path('blog/blog-detail/<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('agency/list/', views.AgencyList.as_view(), name='agency-list'),
    path('agent/list/', views.AgentList.as_view(), name='agent-list'),
    path('search/simple/', views.SimpleSearch.as_view(), name='simple-search'),
    path('search/advanced/', views.AdvancedSearch.as_view(), name='advanced-search'),

    #HTMX urls
    path('lodge-list/', views.LodgesHTMXView.as_view(), name='lodges-htmx'),
    path('bnb-list-htmx/', views.BnbHTMXView.as_view(), name='bnb-htmx'),

    # download document
    path('download/document/<int:pk>/', views.download_doc, name='download-doc'),
]
