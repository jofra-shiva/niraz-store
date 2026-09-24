from django.shortcuts import render
from products.models import Product, Category


def index(request):
    # Fetch categories
    categories = Category.objects.all()
    # Fetch featured products
    featured_products = Product.objects.filter(available=True, featured=True)[:8]
    if not featured_products.exists():
        # Fallback to standard products if no products are marked as featured yet
        featured_products = Product.objects.filter(available=True)[:20]
        
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'index.html', context)

#contact
def contact(request):
    return render(request, 'contact.html')