from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
import datetime

# Login Form
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

# Registration Form
class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    is_manager = forms.BooleanField(required=False, initial=False, label='Register as Manager')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_manager']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))  # Added placeholder

    class Meta:
        model = UserProfile
        fields = ['phone']  # Include fields to update
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'})
        }

        help_texts = {
            'phone': 'Enter your phone number.',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone