from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Retrieve form variables (size, quantity)
    size = request.POST.get('size', 'M')
    try:
        qty = int(request.POST.get('quantity', 1))
    except ValueError:
        qty = 1
        
    cart.add(product=product, size=size, quantity=qty)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id, size):
    cart = Cart(request)
    cart.remove(product_id, size)
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request):
    cart = Cart(request)
    # Loop through post elements to update quantities of existing keys
    for key, value in request.POST.items():
        if key.startswith('qty_'):
            # Key form is qty_{product_id}_{size}
            parts = key.split('_')
            if len(parts) >= 3:
                product_id = parts[1]
                size = parts[2]
                try:
                    qty = int(value)
                    if qty <= 0:
                        cart.remove(product_id, size)
                    else:
                        # Fetch product directly
                        product = get_object_or_404(Product, id=product_id)
                        cart.add(product=product, size=size, quantity=qty, override_quantity=True)
                except (ValueError, Product.DoesNotExist):
                    pass
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})
