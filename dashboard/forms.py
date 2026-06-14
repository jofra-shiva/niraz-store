from django import forms
from products.models import Product, Category


class ProductForm(forms.ModelForm):
    # Field to support direct manual upload of an main product image
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'discount_percent', 'stock', 'available', 'featured', 'is_new', 'emoji']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Vintage Denim Shirt'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': '4', 'placeholder': 'Detailed item description...'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'max': '100'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-checkbox', 'style': 'width: auto; margin-right: 10px;'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-checkbox', 'style': 'width: auto; margin-right: 10px;'}),
            'is_new': forms.CheckboxInput(attrs={'class': 'form-checkbox', 'style': 'width: auto; margin-right: 10px;'}),
            'emoji': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 👔'}),
        }
