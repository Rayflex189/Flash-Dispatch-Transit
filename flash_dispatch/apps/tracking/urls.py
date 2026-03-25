from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.track_shipment, name='track'),
    path('shipment/<str:tracking_number>/', views.shipment_detail, name='shipment_detail'),
    path('api/track/<str:tracking_number>/', views.api_track_shipment, name='api_track'),
]