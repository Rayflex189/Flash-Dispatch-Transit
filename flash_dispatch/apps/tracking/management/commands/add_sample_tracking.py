from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.tracking.models import Shipment, TrackingUpdate
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Add sample tracking data for testing'

    def handle(self, *args, **options):
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('test123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user: test_user / test123'))

        # Sample tracking numbers
        sample_trackings = [
            {
                'tracking': 'FD1234567890',
                'recipient': 'Alice Johnson',
                'address': '456 Oak Street, Los Angeles, CA 90001',
                'status': 'delivered'
            },
            {
                'tracking': 'FD1234567891',
                'recipient': 'Bob Smith',
                'address': '789 Pine Road, Chicago, IL 60601',
                'status': 'in_transit'
            },
            {
                'tracking': 'FD1234567892',
                'recipient': 'Carol White',
                'address': '321 Elm Street, Houston, TX 77001',
                'status': 'out_for_delivery'
            },
            {
                'tracking': 'FD1234567893',
                'recipient': 'David Brown',
                'address': '654 Maple Ave, Phoenix, AZ 85001',
                'status': 'picked_up'
            },
            {
                'tracking': 'FD1234567894',
                'recipient': 'Emma Davis',
                'address': '987 Cedar Ln, Philadelphia, PA 19101',
                'status': 'pending'
            }
        ]

        for sample in sample_trackings:
            shipment, created = Shipment.objects.get_or_create(
                tracking_number=sample['tracking'],
                defaults={
                    'user': user,
                    'sender_name': 'Flash Dispatch',
                    'sender_address': '123 Business Ave, New York, NY 10001',
                    'sender_phone': '+18001234567',
                    'sender_email': 'shipping@flashdispatch.com',
                    'recipient_name': sample['recipient'],
                    'recipient_address': sample['address'],
                    'recipient_phone': '+1987654321',
                    'recipient_email': f"{sample['recipient'].lower().replace(' ', '.')}@example.com",
                    'weight': round(random.uniform(1.0, 10.0), 2),
                    'dimensions': f"{random.randint(10, 40)}x{random.randint(10, 40)}x{random.randint(10, 40)}",
                    'description': 'Package shipment',
                    'service_type': random.choice(['standard', 'express', 'overnight']),
                    'status': sample['status'],
                    'estimated_delivery': datetime.now().date() + timedelta(days=random.randint(1, 7)),
                }
            )
            
            if created:
                # Create tracking updates
                updates = [
                    {'status': 'Order Received', 'location': 'Online', 'desc': 'Shipment information received', 'days': 5},
                    {'status': 'Picked Up', 'location': 'New York', 'desc': 'Package picked up by courier', 'days': 4},
                    {'status': 'In Transit', 'location': 'Distribution Center', 'desc': 'Package in transit to destination', 'days': 3},
                ]
                
                if sample['status'] == 'in_transit':
                    updates.append({'status': 'Arrived at Facility', 'location': 'Chicago', 'desc': 'Package arrived at regional facility', 'days': 2})
                elif sample['status'] == 'out_for_delivery':
                    updates.append({'status': 'Out for Delivery', 'location': 'Los Angeles', 'desc': 'Package out for delivery', 'days': 1})
                elif sample['status'] == 'delivered':
                    updates.append({'status': 'Delivered', 'location': sample['address'].split(',')[0], 'desc': 'Package delivered successfully', 'days': 0})
                
                for update in updates:
                    TrackingUpdate.objects.create(
                        shipment=shipment,
                        status=update['status'],
                        location=update['location'],
                        description=update['desc'],
                        timestamp=datetime.now() - timedelta(days=update['days'])
                    )
                
                self.stdout.write(self.style.SUCCESS(f'Added sample tracking: {sample["tracking"]}'))

        self.stdout.write(self.style.SUCCESS('Sample tracking data added successfully!'))