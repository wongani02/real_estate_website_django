from django.urls import path
from payments import views

app_name = 'payments'

urlpatterns = [
    path('qr-code/properties/', views.generate_properties_code, name='create-qr-code'),
    path('download/<uuid:pk>/', views.download_qr_code, name='download'),

    # path('test-mail/', views.test_mail, name='test-mail'),
]