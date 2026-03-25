from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Address

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'address', 'profile_picture', 
                 'date_of_birth', 'company_name')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'address', 'profile_picture',
                 'date_of_birth', 'company_name')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']