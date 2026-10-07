from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

from .models import Category, Product, ProductImage


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = (
        Product.objects
        .filter(
            category=category,
            available=True
        )
        .prefetch_related(
            Prefetch(
                'images',
                queryset=ProductImage.objects.order_by('display_order', 'id')
            )
        )
    )

    # Filter products
    current_filter = request.GET.get('filter', 'all')

    if current_filter == 'new':
        products = products.filter(is_new=True)

    elif current_filter == 'price-asc':
        products = products.order_by('price')

    elif current_filter == 'price-desc':
        products = products.order_by('-price')

    elif current_filter == 'discount':
        products = products.order_by('-discount_percent')

    else:
        products = products.order_by('-created_at')

    context = {
        'category': category,
        'products': products,
        'current_filter': current_filter,
        'products_count': products.count(),
    }

    return render(
        request,
        'products/category.html',
        context
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related(
            Prefetch(
                'images',
                queryset=ProductImage.objects.order_by(
                    'display_order',
                    'id'
                )
            )
        ),
        slug=slug
    )

    related_products = (
        Product.objects
        .filter(
            category=product.category,
            available=True
        )
        .exclude(id=product.id)
        .prefetch_related(
            Prefetch(
                'images',
                queryset=ProductImage.objects.order_by(
                    'display_order',
                    'id'
                )
            )
        )[:4]
    )

    # Default sizes
    sizes = ["S", "M", "L", "XL", "XXL"]

    # Different sizes for classic/combo
    if product.category.slug in ['classic', 'combo']:
        sizes = ["M", "L", "XL", "XXL"]

    context = {
        'product': product,
        'related_products': related_products,
        'sizes': sizes,
    }

    return render(
        request,
        'products/detail.html',
        context
    )