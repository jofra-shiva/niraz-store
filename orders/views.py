from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm
import razorpay
import traceback

def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:cart_detail')
        
    form = OrderCreateForm()
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Create Order instance without saving to DB yet
            order = form.save(commit=False)
            order.subtotal = cart.get_subtotal()
            order.discount = cart.get_discount()
            order.total_amount = cart.get_total()
            order.save()
            
            # Create OrderItems for each item in Cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    size=item['size'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            
            # Set up Razorpay integration variables
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            amount_in_paise = int(order.total_amount * 100)
            
            try:
                # Create Razorpay Order
                razorpay_order = client.order.create(data={
                    'amount': amount_in_paise,
                    'currency': 'INR',
                    'receipt': f"order_rcpt_{order.id}",
                    'payment_capture': '1'
                })
                # We can store the razorpay order id on the order or pass it directly to payment check templates
                request.session['order_pay_id'] = order.id
                request.session['razorpay_order_id'] = razorpay_order['id']
                
                # Navigate to checkout payment routing
                return render(request, 'payments/checkout_pay.html', {
                    'order': order,
                    'razorpay_order_id': razorpay_order['id'],
                    'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                    'amount_in_paise': amount_in_paise,
                })
            except Exception as e:
                traceback.print_exc()
                print("RAZORPAY ERROR:", repr(e))
                return render(request, 'payments/failure.html', {
                    'error': str(e)
                })
                
    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form,
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/success.html', {'order': order})


def order_track(request):
    phone_number = request.GET.get('phone')
    orders = None
    searched = False
    
    if phone_number:
        # Strip spaces and match
        clean_phone = ''.join(c for c in phone_number if c.isdigit())
        orders = Order.objects.filter(phone_number__icontains=clean_phone).order_by('-created_at')
        searched = True
        
    return render(request, 'orders/track.html', {
        'orders': orders,
        'searched': searched,
        'phone': phone_number
    })
