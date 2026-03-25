from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'landing/home.html')

def about(request):
    return render(request, 'landing/about.html')

def services(request):
    return render(request, 'landing/services.html')

def contact(request):
    return render(request, 'landing/contact.html')

def tracking_page(request):
    return render(request, 'landing/tracking.html')

def rates(request):
    return render(request, 'landing/rates.html')