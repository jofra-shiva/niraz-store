from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, size='M', quantity=1, override_quantity=False):
        product_id = str(product.id)
        cart_key = f"{product_id}_{size}"

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                "product_id": product_id,
                "size": size,
                "quantity": 0,
                "price": str(product.sale_price)
            }

        if override_quantity:
            self.cart[cart_key]["quantity"] = quantity
        else:
            self.cart[cart_key]["quantity"] += quantity

        if self.cart[cart_key]["quantity"] <= 0:
            del self.cart[cart_key]

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product_id, size):
        cart_key = f"{product_id}_{size}"

        if cart_key in self.cart:
            del self.cart[cart_key]

        self.save()

    def __iter__(self):
        product_ids = [item["product_id"] for item in self.cart.values()]
        products = Product.objects.in_bulk(product_ids)

        for item in self.cart.values():
            cart_item = item.copy()

            product = products.get(int(cart_item["product_id"]))

            if product:
                cart_item["product"] = product
                cart_item["price"] = Decimal(cart_item["price"])
                cart_item["total_price"] = (
                    cart_item["price"] * cart_item["quantity"]
                )

                cart_item["price_as_int"] = int(cart_item["price"])
                cart_item["total_price_as_int"] = int(cart_item["total_price"])

                yield cart_item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_subtotal(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def get_discount(self):
        return Decimal("0.00")

    def get_shipping(self):
        return Decimal("0.00")

    def get_total(self):
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
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
        self.save()