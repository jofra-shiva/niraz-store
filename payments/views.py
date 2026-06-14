import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from orders.models import Order
from cart.cart import Cart
from .models import Payment
import razorpay


@csrf_exempt
@require_POST
def payment_verify(request):
    """Verifies Razorpay payment signature and updates models."""
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_signature = request.POST.get('razorpay_signature')
    
    order_id = request.session.get('order_pay_id')
    order = get_object_or_404(Order, id=order_id)
    
    # Try verifying signature
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }
    
    try:
        # Perform signature check
        client.utility.verify_payment_signature(params_dict)
        
        # Save payment details to Database
        payment = Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order_id,
            payment_id=razorpay_payment_id,
            signature=razorpay_signature,
            amount=order.total_amount,
            status=Payment.STATUS_SUCCESS
        )
        
        # Update Order details
        order.payment_status = Order.PAYMENT_COMPLETED
        order.save()
        
        # Clear Shopping Cart
        cart = Cart(request)
        cart.clear()
        
        return redirect('orders:order_success', order_id=order.id)
        
    except razorpay.errors.SignatureVerificationError:
        # Create Failed Payment model
        Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order_id,
            payment_id=razorpay_payment_id,
            signature=razorpay_signature,
            amount=order.total_amount,
            status=Payment.STATUS_FAILED
        )
        order.payment_status = Order.PAYMENT_FAILED
        order.save()
        
        return render(request, 'payments/failure.html', {'order': order})


@csrf_exempt
def payment_failed(request):
    """Handles payments cancelled or crashed client-side."""
    order_id = request.session.get('order_pay_id')
    if order_id:
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.payment_status = Order.PAYMENT_FAILED
            order.save()
            return render(request, 'payments/failure.html', {'order': order})
    return redirect('cart:cart_detail')


@csrf_exempt
def razorpay_webhook(request):
    """Webhook callback endpoint to capture payments from Razorpay backend."""
    if request.method == 'POST':
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        webhook_signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
        webhook_secret = os.getenv('RAZORPAY_WEBHOOK_SECRET', '')
        
        body = request.body.decode('utf-8')
        
        try:
            # Verify Webhook signature if configured
            if webhook_secret:
                client.utility.verify_webhook_signature(body, webhook_signature, webhook_secret)
            
            data = json.loads(body)
            event = data.get('event')
            
            if event == 'payment.captured':
                payment_entity = data['payload']['payment']['entity']
                rzp_order_id = payment_entity.get('order_id')
                rzp_payment_id = payment_entity.get('id')
                
                # Fetch matching order in DB
                order = Order.objects.filter(payments__razorpay_order_id=rzp_order_id).first() or \
                        Order.objects.filter(tracking_code=rzp_order_id).first()
                        
                if order:
                    order.payment_status = Order.PAYMENT_COMPLETED
                    order.save()
                    
                    payment = Payment.objects.filter(razorpay_order_id=rzp_order_id).first()
                    if payment:
                        payment.status = Payment.STATUS_SUCCESS
                        payment.payment_id = rzp_payment_id
                        payment.save()
                    else:
                        Payment.objects.create(
                            order=order,
                            razorpay_order_id=rzp_order_id,
                            payment_id=rzp_payment_id,
                            amount=order.total_amount,
                            status=Payment.STATUS_SUCCESS
                        )
                        
            return HttpResponse(status=200)
        except Exception:
            return HttpResponse(status=400)
            
    return HttpResponse(status=400)
