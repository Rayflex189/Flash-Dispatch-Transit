from django.db import models
from django.contrib.auth import get_user_model
import random
import string
import cloudinary
import cloudinary.uploader

User = get_user_model()

def generate_tracking_number():
    """Generate a unique tracking number"""
    while True:
        tracking_number = 'FD' + ''.join(random.choices(string.digits, k=10))
        if not Shipment.objects.filter(tracking_number=tracking_number).exists():
            return tracking_number

class Shipment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    SERVICE_TYPES = (
        ('standard', 'Standard Delivery'),
        ('express', 'Express Delivery'),
        ('overnight', 'Overnight'),
        ('international', 'International'),
    )
    
    tracking_number = models.CharField(max_length=20, unique=True, default=generate_tracking_number)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipments')
    
    # Sender Information
    sender_name = models.CharField(max_length=255)
    sender_address = models.TextField()
    sender_phone = models.CharField(max_length=15)
    sender_email = models.EmailField()
    
    # Recipient Information
    recipient_name = models.CharField(max_length=255)
    recipient_address = models.TextField()
    recipient_phone = models.CharField(max_length=15)
    recipient_email = models.EmailField()
    
    # Package Details
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=50, help_text="LxWxH in cm")
    description = models.TextField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    
    # Document/Image Uploads (using Cloudinary)
    document = models.ImageField(
        upload_to='shipment_documents/',
        null=True,
        blank=True,
        help_text="Upload document or package image"
    )
    document_cloudinary_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateField()
    actual_delivery = models.DateField(null=True, blank=True)
    
    # Tracking
    current_location = models.CharField(max_length=255, blank=True)
    
    # Additional options
    insurance = models.BooleanField(default=False)
    signature_required = models.BooleanField(default=False)
    fragile_handling = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.tracking_number} - {self.recipient_name}"
    
    def save(self, *args, **kwargs):
        # Upload to Cloudinary if document is present
        if self.document and hasattr(self.document, 'file'):
            try:
                upload_result = cloudinary.uploader.upload(
                    self.document.file,
                    folder=f"shipments/{self.tracking_number}",
                    resource_type="auto"
                )
                self.document_cloudinary_url = upload_result['secure_url']
            except Exception as e:
                print(f"Cloudinary upload error: {e}")
        
        super().save(*args, **kwargs)

class TrackingUpdate(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='updates')
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.status} at {self.location}"