from django.http import JsonResponse
from django.views.decorators.http import require_GET
from apps.tracking.models import Shipment

@require_GET
def track_shipment(request, tracking_number):
    try:
        shipment = Shipment.objects.get(tracking_number=tracking_number)
        updates = shipment.updates.all().values('status', 'location', 'description', 'timestamp')
        
        data = {
            'tracking_number': shipment.tracking_number,
            'status': shipment.status,
            'sender_name': shipment.sender_name,
            'sender_address': shipment.sender_address,
            'recipient_name': shipment.recipient_name,
            'recipient_address': shipment.recipient_address,
            'estimated_delivery': shipment.estimated_delivery,
            'updates': list(updates)
        }
        return JsonResponse(data)
    except Shipment.DoesNotExist:
        return JsonResponse({'error': 'Shipment not found'}, status=404)