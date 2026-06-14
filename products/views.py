from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    
    # Check filter param
    current_filter = request.GET.get('filter', 'all')
    
    if current_filter == 'new':
        products = products.filter(is_new=True)
    elif current_filter == 'price-asc':
        # Sort by calculated sale price, or we can approximate with standard DB order by price
        products = products.order_by('price')
    elif current_filter == 'price-desc':
        products = products.order_by('-price')
    elif current_filter == 'discount':
        products = products.order_by('-discount_percent')
        
    context = {
        'category': category,
        'products': products,
        'current_filter': current_filter,
        'products_count': products.count(),
    }
    return render(request, 'products/category.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # Fetch 4 related products for standard recommendations section
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    
    # Sizing parsing (e.g. standard sizes values or default sizes S, M, L, XL, XXL)
    sizes = ["S", "M", "L", "XL", "XXL"]
    # If the product belongs to combo list or has specialized sizes
    if product.category.slug in ['classic', 'combo']:
        sizes = ["M", "L", "XL", "XXL"]
        
    context = {
        'product': product,
        'related_products': related_products,
        'sizes': sizes,
    }
    return render(request, 'products/detail.html', context)
