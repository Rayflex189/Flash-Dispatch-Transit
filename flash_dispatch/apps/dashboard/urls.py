from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_shipment, name='create_shipment'),
    path('shipments/', views.shipment_list, name='shipments'),
    path('shipment/<str:tracking_number>/', views.shipment_detail, name='shipment_detail'),
    path('shipment/<str:tracking_number>/update-status/', views.update_shipment_status, name='update_status'),
]