from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('track/<str:tracking_number>/', views.track_shipment, name='track'),
]