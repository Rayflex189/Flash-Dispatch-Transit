from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

def home(request):
    return render(request, 'landing/home.html')

def about(request):
    return render(request, 'landing/about.html')

def services(request):
    return render(request, 'landing/services.html')

def contact(request):
    return render(request, 'landing/contact.html')

def rates(request):
    """Rates and pricing page"""
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
    
    # Rate calculation (same logic as in template)
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