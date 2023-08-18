from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    #auth views
    path('login/', user_views.loginView, name='login'),
    path('logout/', user_views.logoutView, name='logout'),
    path('register/', user_views.RegisterView, name='register'),

    #dashboard views
    path('dashboard/my-properties/', user_views.myPropertiesView, name='my-properties'),
    path('dashboard/dashboard/', user_views.dashboardView, name='dashboard'),
    path('dashboard/bookmarks/', user_views.bookmarksView, name='bookmarks'),
    path('dashboard/profile/', user_views.profileView, name='profile'),
    path('dashboard/notifications/', user_views.notificationsView, name='notifications'),
    path('payments/bookings/select/choice=<str:booking>/', user_views.bookingsView, name='bookings-choice'),
    path('payments/bookings/select/', user_views.direct_bookings, name='select-bookings'),
    path('payments/finances/select/choice=<str:finances>/', user_views.financesView, name='finances-choice'),
    path('payments/finances/select/', user_views.direct_finances, name='select-finances'),
    path('payments/bank-details/', user_views.user_bank_details_view, name='bank-details'),

    #onbordingviews
    path('create-property/onbording-xhtl1/', user_views.typeOfPropertyView, name='onbording-1'),
    path('create-property/onbording-gksk2/<str:p_type>/', user_views.postPropertyAsView, name='onbording-2'),

    # Ajax
    path('bnb/booking-details/', user_views.get_bnb_booking_details, name='bnb-booking-details'),
    path('lodge/booking-details/', user_views.get_lodge_booking_details, name='lodge-booking-details'),
    path('bnb/payment-details/', user_views.get_bnb_payment_details, name='bnb-payment-details'),
    path('lodge/payment-details/', user_views.get_lodge_payment_details, name='lodge-payment-details'),
    path('property/payment-details/', user_views.get_property_payment_details, name='property-payment-details'),

    # qr images
    path('download/payment/property/', user_views.download_property_qr, name='payment-property-qr'),
    path('download/payment/bnb/', user_views.download_bnb_qr, name='payment-bnb-qr'),
    path('download/payment/lodge/', user_views.download_lodge_qr, name='payment-lodge-qr'),
]