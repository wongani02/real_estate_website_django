from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', user_views.loginView, name='login'),
]