from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_percent', 'stock', 'available', 'featured', 'is_new']
    list_filter = ['available', 'featured', 'is_new', 'category']
    list_editable = ['price', 'discount_percent', 'stock', 'available', 'featured', 'is_new']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
