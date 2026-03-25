from django.shortcuts import render

def home(request):
    return render(request, 'landing/home.html')

def about(request):
    return render(request, 'landing/about.html')

def contact(request):
    return render(request, 'landing/contact.html')

def services(request):
    return render(request, 'landing/services.html')