from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'address', 'city', 'pincode', 'state']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+91 98765 43210', 'pattern': '[0-9]{10}'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Flat/House No., Street, Area, Landmark', 'rows': '3'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'pincode': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '6-digit PIN', 'pattern': '[0-9]{6}', 'maxlength': '6'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State'}),
        }
