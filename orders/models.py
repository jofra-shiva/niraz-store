import random
from django.db import models
from products.models import Product


class Order(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_PACKED = 'Packed'
    STATUS_SHIPPED = 'Shipped'
    STATUS_DELIVERED = 'Delivered'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PACKED, 'Packed'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
    ]

    PAYMENT_PENDING = 'Pending'
    PAYMENT_COMPLETED = 'Completed'
    PAYMENT_FAILED = 'Failed'

    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETED, 'Completed'),
        (PAYMENT_FAILED, 'Failed'),
    ]

    customer_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100, default='')
    pincode = models.CharField(max_length=10, default='')
    state = models.CharField(max_length=100, default='')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    tracking_code = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate a beautiful dynamic tracking code: e.g. NRZ-123456
        if not self.tracking_code:
            random_num = random.randint(100000, 999999)
            self.tracking_code = f"NRZ-{random_num}"
        super().save(*args, **kwargs)

    @property
    def subtotal_as_int(self):
        return int(self.subtotal)

    @property
    def discount_as_int(self):
        return int(self.discount)

    @property
    def total_amount_as_int(self):
        return int(self.total_amount)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name} ({self.tracking_code})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    size = models.CharField(max_length=10, default='M')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity

    @property
    def price_as_int(self):
        return int(self.price)

    @property
    def total_price_as_int(self):
        return int(self.total_price)

    def __str__(self):
        return f"Item: {self.product.name} × {self.quantity} ({self.size})"
