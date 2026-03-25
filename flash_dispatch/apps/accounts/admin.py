from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Address

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'user_type', 'phone_number', 'profile_picture_preview', 'is_staff', 'is_active']
    list_filter = ['user_type', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'phone_number', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number', 
                'date_of_birth', 'company_name', 'address', 'profile_picture'
            )
        }),
        ('Account Type & Permissions', {
            'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Notification Preferences', {
            'fields': ('email_notifications', 'sms_notifications', 'push_notifications'),
            'classes': ('collapse',)
        }),
        ('User Preferences', {
            'fields': ('language', 'timezone'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'phone_number')
        }),
    )
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.profile_picture.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: #e2e8f0; border-radius: 50%; display: flex; align-items: center; justify-content: center;">'
            '<span style="font-size: 20px;">{}</span></div>',
            obj.username[0].upper()
        )
    profile_picture_preview.short_description = 'Profile Picture'
    
    actions = ['make_customer', 'make_dispatcher', 'make_admin', 'enable_notifications', 'disable_notifications']
    
    def make_customer(self, request, queryset):
        queryset.update(user_type='customer')
        self.message_user(request, f"{queryset.count()} users changed to Customer.")
    make_customer.short_description = "Change selected users to Customer"
    
    def make_dispatcher(self, request, queryset):
        queryset.update(user_type='dispatcher')
        self.message_user(request, f"{queryset.count()} users changed to Dispatcher.")
    make_dispatcher.short_description = "Change selected users to Dispatcher"
    
    def make_admin(self, request, queryset):
        queryset.update(user_type='admin')
        self.message_user(request, f"{queryset.count()} users changed to Admin.")
    make_admin.short_description = "Change selected users to Admin"
    
    def enable_notifications(self, request, queryset):
        queryset.update(email_notifications=True, sms_notifications=True, push_notifications=True)
        self.message_user(request, f"Enabled notifications for {queryset.count()} users.")
    enable_notifications.short_description = "Enable all notifications for selected users"
    
    def disable_notifications(self, request, queryset):
        queryset.update(email_notifications=False, sms_notifications=False, push_notifications=False)
        self.message_user(request, f"Disabled notifications for {queryset.count()} users.")
    disable_notifications.short_description = "Disable all notifications for selected users"

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address_line1', 'city', 'state', 'postal_code', 'country', 'is_default', 'created_at']
    list_filter = ['is_default', 'country', 'state', 'city']
    search_fields = ['address_line1', 'city', 'state', 'postal_code', 'user__username', 'user__email']
    list_editable = ['is_default']
    list_per_page = 20
    ordering = ['-is_default', '-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Address Details', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Address Settings', {
            'fields': ('is_default',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.is_default:
            # Set all other addresses of this user to non-default
            Address.objects.filter(user=obj.user).exclude(id=obj.id).update(is_default=False)
        super().save_model(request, obj, form, change)
    
    actions = ['mark_as_default', 'remove_default']
    
    def mark_as_default(self, request, queryset):
        for address in queryset:
            # Set this address as default and remove default from others
            Address.objects.filter(user=address.user).update(is_default=False)
            address.is_default = True
            address.save()
        self.message_user(request, f"{queryset.count()} addresses marked as default.")
    mark_as_default.short_description = "Mark selected addresses as default"
    
    def remove_default(self, request, queryset):
        queryset.update(is_default=False)
        self.message_user(request, f"Removed default status from {queryset.count()} addresses.")
    remove_default.short_description = "Remove default status from selected addresses"

# Register models with custom admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Address, AddressAdmin)

# Customize admin site header
admin.site.site_header = "Flash Dispatch Administration"
admin.site.site_title = "Flash Dispatch Admin Portal"
admin.site.index_title = "Welcome to Flash Dispatch Admin Dashboard"