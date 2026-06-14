from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    def __init__(self, request):
        """Initialize the cart in Django session."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, size='M', quantity=1, override_quantity=False):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        # Create a unique key for product status and size pairing
        cart_key = f"{product_id}_{size}"
        
        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'product_id': product_id,
                'size': size,
                'quantity': 0,
                'price': str(product.sale_price)
            }
            
        if override_quantity:
            new_qty = quantity
        else:
            new_qty = self.cart[cart_key]['quantity'] + quantity

        if new_qty <= 0:
            if cart_key in self.cart:
                del self.cart[cart_key]
        else:
            self.cart[cart_key]['quantity'] = new_qty
            
        self.save()

    def save(self):
        # Mark the session as modified to make sure it gets saved
        self.session.modified = True

    def remove(self, product_id, size):
        """Remove a product from the cart."""
        cart_key = f"{product_id}_{size}"
        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and get the products from the database."""
        product_ids = [item['product_id'] for item in self.cart.values()]
        # Fetch actual product objects from db
        products = Product.objects.in_bulk(product_ids)
        
        for cart_key, item in self.cart.items():
            product = products.get(int(item['product_id']))
            if product:
                item['product'] = product
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                # Cast integer helper values for direct templates
                item['price_as_int'] = int(item['price'])
                item['total_price_as_int'] = int(item['total_price'])
                yield item

    def __len__(self):
        """Count the total number of items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        """Returns the sum of prices * quantity for all items."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_discount(self):
        """Apply a standard 5% discount matching the frontend cart.html layout."""
        subtotal = self.get_subtotal()
        return (subtotal * Decimal('0.05')).quantize(Decimal('1.00'))

    def get_shipping(self):
        """Free shipping above 999 else 99, matching the frontend cart.html."""
        subtotal = self.get_subtotal()
        if subtotal > 999 or subtotal == 0:
            return Decimal('0.00')
        return Decimal('99.00')

    def get_total(self):
        """Returns total order amount incorporating discount and shipping."""
        return self.get_subtotal() - self.get_discount() + self.get_shipping()

    def get_subtotal_as_int(self):
        return int(self.get_subtotal())

    def get_discount_as_int(self):
        return int(self.get_discount())

    def get_shipping_as_int(self):
        return int(self.get_shipping())

    def get_total_as_int(self):
        return int(self.get_total())

    def clear(self):
        """Empty the cart session."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
