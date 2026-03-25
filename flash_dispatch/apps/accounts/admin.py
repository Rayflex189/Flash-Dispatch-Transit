from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'user_type', 'phone_number', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'address', 
                                       'profile_picture', 'date_of_birth', 'company_name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'address', 
                                       'profile_picture', 'date_of_birth', 'company_name')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Address)