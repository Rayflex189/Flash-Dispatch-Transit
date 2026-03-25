from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Shipment

def track_shipment(request):
    return render(request, 'tracking/track.html')

def shipment_detail(request, tracking_number):
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)
    return render(request, 'tracking/shipment_detail.html', {'shipment': shipment})