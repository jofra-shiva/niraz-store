from django.db import models
from orders.models import Order


class Payment(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_SUCCESS = 'Success'
    STATUS_FAILED = 'Failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SUCCESS, 'Success'),
        (STATUS_FAILED, 'Failed'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    razorpay_order_id = models.CharField(max_length=150)
    payment_id = models.CharField(max_length=150, blank=True, null=True)
    signature = models.CharField(max_length=250, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} ({self.status})"
