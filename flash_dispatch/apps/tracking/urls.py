from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.track_shipment, name='track'),
    path('<str:tracking_number>/', views.shipment_detail, name='detail'),
]