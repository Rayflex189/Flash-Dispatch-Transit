from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        newsletter = request.POST.get('newsletter')
        
        try:
            # Prepare email content
            email_subject = f"Contact Form: {subject} - from {name}"
            
            # HTML email template
            html_message = render_to_string('emails/contact_notification.html', {
                'name': name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
                'newsletter': newsletter,
                'date': datetime.now()
            })
            
            # Plain text version (fallback)
            plain_message = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            Subject: {subject}
            
            Message:
            {message}
            
            Newsletter Subscription: {'Yes' if newsletter else 'No'}
            Submitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            # Send to admin/contact email
            admin_email = EmailMessage(
                email_subject,
                html_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                reply_to=[email]
            )
            admin_email.content_subtype = "html"
            admin_email.send(fail_silently=False)
            
            # Auto-respond to user
            if email:
                user_html_message = render_to_string('emails/auto_response.html', {
                    'name': name,
                    'subject': subject,
                    'date': datetime.now()
                })
                
                user_email = EmailMessage(
                    "Thank you for contacting Flash Dispatch",
                    user_html_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                )
                user_email.content_subtype = "html"
                user_email.send(fail_silently=False)
            
            messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
            
        except Exception as e:
            # Log the error
            print(f"Email error: {e}")
            messages.error(request, 'There was an error sending your message. Please try again or call us directly.')
        
        return redirect('landing:contact')
    
    return render(request, 'landing/contact.html')

def home(request):
    return render(request, 'landing/home.html')

def about(request):
    return render(request, 'landing/about.html')

def services(request):
    return render(request, 'landing/services.html')

def rates(request):
    return render(request, 'landing/rates.html')

@require_http_methods(["POST"])
def calculate_shipping_rate(request):
    """API endpoint for calculating shipping rates"""
    import json
    data = json.loads(request.body)
    
    # Rate calculation logic
    service = data.get('service', 'standard')
    weight = float(data.get('weight', 1))
    from_location = data.get('from_location', 'ny')
    to_location = data.get('to_location', 'ny')
    
    # Rate calculation
    rates = {
        'standard': {'base': 8, 'per_kg': 1.2, 'per_km': 0.05},
        'express': {'base': 15, 'per_kg': 2.0, 'per_km': 0.08},
        'overnight': {'base': 25, 'per_kg': 3.0, 'per_km': 0.12},
        'international': {'base': 35, 'per_kg': 4.5, 'per_km': 0.15}
    }
    
    distances = {
        'ny': {'ny': 0, 'la': 2800, 'ch': 800, 'tx': 1600, 'ph': 2100},
        'la': {'ny': 2800, 'la': 0, 'ch': 1700, 'tx': 1500, 'ph': 350},
        'ch': {'ny': 800, 'la': 1700, 'ch': 0, 'tx': 900, 'ph': 1450},
        'tx': {'ny': 1600, 'la': 1500, 'ch': 900, 'tx': 0, 'ph': 1000},
        'ph': {'ny': 2100, 'la': 350, 'ch': 1450, 'tx': 1000, 'ph': 0}
    }
    
    selected_rates = rates.get(service, rates['standard'])
    distance = distances.get(from_location, {}).get(to_location, 0)
    
    base_price = selected_rates['base']
    weight_surcharge = weight * selected_rates['per_kg']
    distance_fee = distance * selected_rates['per_km']
    total = base_price + weight_surcharge + distance_fee
    
    return JsonResponse({
        'success': True,
        'total': round(total, 2),
        'breakdown': {
            'base_price': base_price,
            'weight_surcharge': round(weight_surcharge, 2),
            'distance_fee': round(distance_fee, 2)
        }
    })