from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from apps.tracking.models import Shipment, TrackingUpdate
from apps.accounts.models import User
from django.core.exceptions import PermissionDenied
import random
import string
from datetime import datetime

def generate_tracking_number():
    """Generate a unique tracking number"""
    while True:
        tracking_number = 'FD' + ''.join(random.choices(string.digits, k=10))
        if not Shipment.objects.filter(tracking_number=tracking_number).exists():
            return tracking_number

def is_admin_or_staff(user):
    """Check if user is admin or staff"""
    return user.is_staff or user.is_superuser

@login_required
def home(request):
    """Dashboard home page"""
    # Get user's shipments
    shipments = Shipment.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Statistics
    total_shipments = Shipment.objects.filter(user=request.user).count()
    delivered_shipments = Shipment.objects.filter(user=request.user, status='delivered').count()
    in_transit = Shipment.objects.filter(user=request.user, status='in_transit').count()
    pending = Shipment.objects.filter(user=request.user, status='pending').count()
    
    # Recent activity
    recent_activity = []
    for shipment in shipments:
        latest_update = shipment.updates.first()
        recent_activity.append({
            'shipment': shipment,
            'status': shipment.status,
            'description': latest_update.description if latest_update else 'Shipment created',
            'timestamp': latest_update.timestamp if latest_update else shipment.created_at
        })
    
    context = {
        'shipments': shipments,
        'total_shipments': total_shipments,
        'delivered_shipments': delivered_shipments,
        'in_transit': in_transit,
        'pending_shipments': pending,
        'recent_activity': recent_activity,
        'now': timezone.now()
    }
    return render(request, 'dashboard/home.html', context)

@login_required
@user_passes_test(is_admin_or_staff, login_url='dashboard:home')
def create_shipment(request):
    """Create a new shipment - Staff only"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Get form data
                package_type = request.POST.get('package_type')
                weight = float(request.POST.get('weight', 0))
                length = float(request.POST.get('length', 0))
                width = float(request.POST.get('width', 0))
                height = float(request.POST.get('height', 0))
                service_type = request.POST.get('service_type')
                
                # Sender information
                sender_name = request.POST.get('sender_name')
                sender_address = request.POST.get('sender_address')
                sender_phone = request.POST.get('sender_phone')
                sender_email = request.POST.get('sender_email')
                
                # Recipient information
                recipient_name = request.POST.get('recipient_name')
                recipient_address = request.POST.get('recipient_address')
                recipient_phone = request.POST.get('recipient_phone')
                recipient_email = request.POST.get('recipient_email')
                
                # Additional options
                insurance = request.POST.get('insurance') == 'on'
                signature = request.POST.get('signature') == 'on'
                fragile = request.POST.get('fragile') == 'on'
                
                # Validate required fields
                if not all([sender_name, sender_address, sender_phone, sender_email,
                           recipient_name, recipient_address, recipient_phone, recipient_email]):
                    messages.error(request, 'Please fill in all required fields.')
                    return render(request, 'dashboard/create_shipment.html')
                
                # Calculate estimated delivery date
                from datetime import datetime, timedelta
                if service_type == 'overnight':
                    estimated_delivery = datetime.now().date() + timedelta(days=1)
                elif service_type == 'express':
                    estimated_delivery = datetime.now().date() + timedelta(days=2)
                elif service_type == 'international':
                    estimated_delivery = datetime.now().date() + timedelta(days=7)
                else:
                    estimated_delivery = datetime.now().date() + timedelta(days=5)
                
                # Create shipment
                shipment = Shipment.objects.create(
                    tracking_number=generate_tracking_number(),
                    user=request.user,
                    sender_name=sender_name,
                    sender_address=sender_address,
                    sender_phone=sender_phone,
                    sender_email=sender_email,
                    recipient_name=recipient_name,
                    recipient_address=recipient_address,
                    recipient_phone=recipient_phone,
                    recipient_email=recipient_email,
                    weight=weight,
                    dimensions=f"{length}x{width}x{height}",
                    description=f"Package Type: {package_type}",
                    service_type=service_type,
                    status='pending',
                    estimated_delivery=estimated_delivery,
                    current_location='Processing Center'
                )
                
                # Create initial tracking update
                TrackingUpdate.objects.create(
                    shipment=shipment,
                    status='Order Received',
                    location='Flash Dispatch Hub',
                    description='Shipment information received. Your package is being processed.',
                    timestamp=timezone.now()
                )
                
                messages.success(request, f'Shipment created successfully! Tracking number: {shipment.tracking_number}')
                return redirect('dashboard:shipment_detail', tracking_number=shipment.tracking_number)
                
        except Exception as e:
            messages.error(request, f'Error creating shipment: {str(e)}')
            return render(request, 'dashboard/create_shipment.html')
    
    return render(request, 'dashboard/create_shipment.html')

@login_required
def shipment_detail(request, tracking_number):
    """View shipment details"""
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)
    
    # Check if user has permission (owner or staff)
    if shipment.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this shipment.')
        return redirect('dashboard:home')
    
    tracking_updates = shipment.updates.all().order_by('-timestamp')
    
    # Calculate status percentage for progress bar
    status_percentage = {
        'pending': 20,
        'picked_up': 40,
        'in_transit': 60,
        'out_for_delivery': 80,
        'delivered': 100
    }.get(shipment.status, 0)
    
    context = {
        'shipment': shipment,
        'tracking_updates': tracking_updates,
        'status_percentage': status_percentage,
        'now': timezone.now()
    }
    return render(request, 'dashboard/shipment_detail.html', context)

@login_required
def shipment_list(request):
    """List all shipments for the user"""
    if request.user.is_staff:
        # Staff can see all shipments
        shipments = Shipment.objects.all().order_by('-created_at')
    else:
        # Regular users see only their shipments
        shipments = Shipment.objects.filter(user=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        shipments = shipments.filter(status=status_filter)
    
    # Calculate counts for stats
    total_count = shipments.count()
    
    context = {
        'shipments': shipments,
        'total_count': total_count,
        'status_filter': status_filter,
        'status_choices': Shipment.STATUS_CHOICES,
        'now': timezone.now()
    }
    return render(request, 'dashboard/shipments.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def update_shipment_status(request, tracking_number):
    """Update shipment status - Staff only"""
    if request.method == 'POST':
        shipment = get_object_or_404(Shipment, tracking_number=tracking_number)
        new_status = request.POST.get('status')
        location = request.POST.get('location')
        description = request.POST.get('description')
        
        if new_status in dict(Shipment.STATUS_CHOICES):
            shipment.status = new_status
            shipment.save()
            
            # Create tracking update
            TrackingUpdate.objects.create(
                shipment=shipment,
                status=new_status,
                location=location or 'In transit',
                description=description or f'Shipment status updated to {dict(Shipment.STATUS_CHOICES)[new_status]}',
                timestamp=timezone.now()
            )
            
            messages.success(request, f'Shipment {shipment.tracking_number} status updated successfully!')
        else:
            messages.error(request, 'Invalid status selected.')
        
        return redirect('dashboard:shipment_detail', tracking_number=tracking_number)
    
    return redirect('dashboard:shipment_detail', tracking_number=tracking_number)