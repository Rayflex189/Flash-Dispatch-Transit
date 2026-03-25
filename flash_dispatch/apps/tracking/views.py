from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Shipment, TrackingUpdate

def track_shipment(request):
    """Main tracking page view"""
    tracking_number = request.GET.get('tracking', None)
    shipment = None
    error = None
    
    if tracking_number:
        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number.upper())
            # Get all tracking updates
            tracking_updates = shipment.updates.all().order_by('-timestamp')
        except Shipment.DoesNotExist:
            error = "No shipment found with this tracking number. Please check and try again."
    
    context = {
        'shipment': shipment,
        'error': error,
        'tracking_number': tracking_number,
        'tracking_updates': shipment.updates.all().order_by('-timestamp') if shipment else []
    }
    return render(request, 'tracking/track.html', context)

def shipment_detail(request, tracking_number):
    """Detailed view for a specific shipment"""
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number.upper())
    tracking_updates = shipment.updates.all().order_by('-timestamp')
    
    context = {
        'shipment': shipment,
        'tracking_updates': tracking_updates,
        'status_percentage': get_status_percentage(shipment.status),
        'estimated_delivery_days': get_estimated_days(shipment.estimated_delivery),
    }
    return render(request, 'tracking/shipment_detail.html', context)

@require_http_methods(["GET"])
def api_track_shipment(request, tracking_number):
    """API endpoint for AJAX tracking"""
    try:
        shipment = Shipment.objects.get(tracking_number=tracking_number.upper())
        updates = shipment.updates.all().values('status', 'location', 'description', 'timestamp')
        
        data = {
            'success': True,
            'tracking_number': shipment.tracking_number,
            'status': shipment.get_status_display(),
            'status_code': shipment.status,
            'sender_name': shipment.sender_name,
            'sender_address': shipment.sender_address,
            'recipient_name': shipment.recipient_name,
            'recipient_address': shipment.recipient_address,
            'weight': str(shipment.weight),
            'service_type': shipment.get_service_type_display(),
            'created_at': shipment.created_at.strftime('%Y-%m-%d %H:%M'),
            'estimated_delivery': shipment.estimated_delivery.strftime('%Y-%m-%d'),
            'current_location': shipment.current_location or 'In transit',
            'updates': list(updates),
            'status_percentage': get_status_percentage(shipment.status)
        }
        return JsonResponse(data)
    except Shipment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'No shipment found with this tracking number'
        }, status=404)

def get_status_percentage(status):
    """Calculate progress percentage based on status"""
    status_map = {
        'pending': 20,
        'picked_up': 40,
        'in_transit': 60,
        'out_for_delivery': 80,
        'delivered': 100
    }
    return status_map.get(status, 0)

def get_estimated_days(estimated_date):
    """Calculate estimated delivery days from now"""
    from datetime import date
    days = (estimated_date - date.today()).days
    if days < 0:
        return "Delivered"
    elif days == 0:
        return "Today"
    elif days == 1:
        return "Tomorrow"
    else:
        return f"{days} days"