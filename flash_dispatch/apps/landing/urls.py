from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('rates/', views.rates, name='rates'),
    path('api/calculate-rate/', views.calculate_shipping_rate, name='calculate_rate'),
]