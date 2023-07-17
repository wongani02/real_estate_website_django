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
    path('payments/bookings/<str:booking>/choice/', user_views.bookingsView, name='bookings'),
    path('payments/bookings/select/', user_views.direct_bookings, name='select-bookings'),
    path('payments/bookings/select/<str:booking>/', user_views.direct_bookings_choice, name='bookings-choice'),
    path('payments/finances/<str:finances>/choice/', user_views.financesView, name='finances'),
    path('payments/finances/select/', user_views.direct_finances, name='select-finances'),
    path('payments/finances/select/<str:finances>/', user_views.direct_finances_choice, name='finances-choice'),
    

    #onbordingviews
    path('create-property/onbording-xhtl1/', user_views.typeOfPropertyView, name='onbording-1'),
    path('create-property/onbording-gksk2/<str:p_type>/', user_views.postPropertyAsView, name='onbording-2'),
]