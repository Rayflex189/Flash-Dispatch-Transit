from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, ProfileUpdateForm, AddressForm
from .models import Address, User
from apps.tracking.models import Shipment
from datetime import datetime, timedelta

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Flash Dispatch.')
            return redirect('dashboard:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    # Get user's shipment statistics
    total_shipments = Shipment.objects.filter(user=request.user).count()
    
    # Get shipments from this month
    first_day_of_month = datetime.now().replace(day=1)
    monthly_shipments = Shipment.objects.filter(
        user=request.user,
        created_at__gte=first_day_of_month
    ).count()
    
    # Calculate loyalty points (1 point per shipment)
    loyalty_points = total_shipments * 10
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    addresses = Address.objects.filter(user=request.user)
    
    # Get recent shipments for activity
    recent_shipments = Shipment.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'addresses': addresses,
        'total_shipments': total_shipments,
        'monthly_shipments': monthly_shipments,
        'loyalty_points': loyalty_points,
        'recent_shipments': recent_shipments,
        'address_form': AddressForm(),
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            
            # If this is the first address or user wants it as default
            if request.POST.get('is_default') or not Address.objects.filter(user=request.user).exists():
                address.is_default = True
                
            address.save()
            
            # If this address is default, remove default from others
            if address.is_default:
                Address.objects.filter(user=request.user).exclude(id=address.id).update(is_default=False)
                
            messages.success(request, 'Address added successfully!')
        else:
            messages.error(request, 'Please correct the errors below.')
    return redirect('accounts:profile')

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save()
            
            # If this address is set as default
            if request.POST.get('is_default'):
                Address.objects.filter(user=request.user).exclude(id=address.id).update(is_default=False)
                address.is_default = True
                address.save()
                
            messages.success(request, 'Address updated successfully!')
        else:
            messages.error(request, 'Please correct the errors below.')
        return redirect('accounts:profile')
    
    # Return address data as JSON for AJAX request
    from django.http import JsonResponse
    return JsonResponse({
        'id': address.id,
        'address_line1': address.address_line1,
        'address_line2': address.address_line2,
        'city': address.city,
        'state': address.state,
        'postal_code': address.postal_code,
        'country': address.country,
        'is_default': address.is_default
    })

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully!')
    return redirect('accounts:profile')

@login_required
def set_default_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    # Set this address as default
    Address.objects.filter(user=request.user).update(is_default=False)
    address.is_default = True
    address.save()
    
    messages.success(request, 'Default address updated successfully!')
    return redirect('accounts:profile')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def update_notifications(request):
    if request.method == 'POST':
        user = request.user
        user.email_notifications = request.POST.get('email_notifications') == 'on'
        user.sms_notifications = request.POST.get('sms_notifications') == 'on'
        user.push_notifications = request.POST.get('push_notifications') == 'on'
        user.save()
        messages.success(request, 'Notification preferences updated!')
    return redirect('accounts:profile')

@login_required
def update_preferences(request):
    if request.method == 'POST':
        user = request.user
        user.language = request.POST.get('language')
        user.timezone = request.POST.get('timezone')
        user.save()
        messages.success(request, 'Preferences updated successfully!')
    return redirect('accounts:profile')