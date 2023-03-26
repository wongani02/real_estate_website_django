from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    #auth views
    path('login/', user_views.loginView, name='login'),
    path('logout/', user_views.logoutView, name='logout'),

    #dashboard views
    path('dashboard/my-properties/', user_views.myPropertiesView, name='my-properties'),
    path('dashboard/dashboard/', user_views.dashboardView, name='dashboard'),
    path('dashboard/bookmarks/', user_views.bookmarksView, name='bookmarks'),
    path('dashboard/profile/', user_views.bookmarksView, name='profile'),
]