from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('dispatcher', 'Dispatcher'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    
    # Preferences
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='America/New_York')
    
    class Meta:
        db_table = 'accounts_user'
        
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Made nullable for migration
    updated_at = models.DateTimeField(auto_now=True, null=True)  # Added updated_at field
    
    class Meta:
        ordering = ['-is_default', '-created_at']
        db_table = 'accounts_address'
    
    def __str__(self):
        return f"{self.address_line1}, {self.city}"
    
    def save(self, *args, **kwargs):
        # If this is the first address for the user, make it default
        if not self.pk and not Address.objects.filter(user=self.user).exists():
            self.is_default = True
        super().save(*args, **kwargs)