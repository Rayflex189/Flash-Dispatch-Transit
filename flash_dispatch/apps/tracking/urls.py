from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.track_shipment, name='track'),
    path('api/track/<str:tracking_number>/', views.api_track_shipment, name='api_track'),
]