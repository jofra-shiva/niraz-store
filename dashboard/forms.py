from django import forms
from products.models import Product


class ProductForm(forms.ModelForm):

    # This is NOT stored directly on Product.
    # It is handled separately in views.py and saved to ProductImage.
    image = forms.ImageField(
        required=False,
        label="Product Image",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": "image/*",
                "class": "product-image-input",
            }
        ),
    )

    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "price",
            "discount_percent",
            "stock",
            "available",
            "featured",
            "is_new",
            "emoji",
        ]

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter product description",
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00",
                }
            ),

            "discount_percent": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "100",
                    "placeholder": "0",
                }
            ),

            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "placeholder": "10",
                }
            ),

            "emoji": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "👔",
                }
            ),

            "available": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "featured": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "is_new": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is not None and price < 0:
            raise forms.ValidationError(
                "Price cannot be negative."
            )

        return price

    def clean_discount_percent(self):
        discount = self.cleaned_data.get("discount_percent")

        if discount is not None and discount > 100:
            raise forms.ValidationError(
                "Discount cannot be greater than 100%."
            )

        return discount

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")

        if stock is not None and stock < 0:
            raise forms.ValidationError(
                "Stock cannot be negative."
            )

        return stock