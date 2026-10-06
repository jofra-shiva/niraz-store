from django import forms
from django.contrib import admin

from .models import Category, Product, ProductImage
from .imgbb import upload_to_imgbb


# =========================================================
# PRODUCT IMAGE FORM
# =========================================================

class ProductImageForm(forms.ModelForm):

    # This is the actual file upload field
    upload_image = forms.ImageField(
        required=False,
        label="Image"
    )

    class Meta:
        model = ProductImage

        # Don't show the URLField to the admin
        fields = [
            "upload_image",
            "display_order",
        ]

    def save(self, commit=True):

        product_image = super().save(
            commit=False
        )

        uploaded_file = self.cleaned_data.get(
            "upload_image"
        )

        # Upload selected file to ImgBB
        if uploaded_file:

            image_url = upload_to_imgbb(
                uploaded_file
            )

            # Save ImgBB URL
            product_image.image = image_url

        if commit:
            product_image.save()

        return product_image


# =========================================================
# PRODUCT IMAGE INLINE
# =========================================================

class ProductImageInline(admin.TabularInline):

    model = ProductImage

    form = ProductImageForm

    extra = 1

    fields = (
        "upload_image",
        "display_order",
    )


# =========================================================
# CATEGORY ADMIN
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "created_at",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


# =========================================================
# PRODUCT ADMIN
# =========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "discount_percent",
        "stock",
        "available",
        "featured",
        "is_new",
    )

    list_filter = (
        "category",
        "available",
        "featured",
        "is_new",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [
        ProductImageInline
    ]