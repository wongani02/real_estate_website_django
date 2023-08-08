"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from core import settings

admin.site.site_header = 'Afrihuts Administration'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Properties url
    path('', include('properties.urls')),

    # bnb url
    path('bnb/', include('bnb.urls', namespace='bnb')),

    # accounts url
    path('accounts/', include('users.urls', namespace='accounts')),

    # lodges url
    path('lodges/', include('lodges.urls', namespace='lodges')),

    # payments url
    path('payments/', include('payments.urls')),

    # verifications url
    path('verifications/', include('verifications.urls')),

    # modified tracking library
    path('tracker/', include('modified_tracking_analyzer.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
