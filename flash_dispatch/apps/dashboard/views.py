from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from apps.tracking.models import Shipment

@login_required
def home(request):
    # Get user's shipments
    shipments = Shipment.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Statistics
    total_shipments = Shipment.objects.filter(user=request.user).count()
    delivered_shipments = Shipment.objects.filter(user=request.user, status='delivered').count()
    in_transit = Shipment.objects.filter(user=request.user, status='in_transit').count()
    
    # Recent activity
    recent_activity = []
    for shipment in shipments:
        recent_activity.append({
            'shipment': shipment,
            'latest_update': shipment.updates.first()
        })
    
    context = {
        'shipments': shipments,
        'total_shipments': total_shipments,
        'delivered_shipments': delivered_shipments,
        'in_transit': in_transit,
        'recent_activity': recent_activity,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def create_shipment(request):
    if request.method == 'POST':
        # Handle shipment creation
        pass
    return render(request, 'dashboard/create_shipment.html')

@login_required
def shipment_detail(request, tracking_number):
    shipment = Shipment.objects.get(tracking_number=tracking_number, user=request.user)
    tracking_updates = shipment.updates.all()
    return render(request, 'dashboard/shipment_detail.html', {
        'shipment': shipment,
        'tracking_updates': tracking_updates
    })


@login_required
def shipment_list(request):
    shipments = Shipment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/shipments.html', {'shipments': shipments})