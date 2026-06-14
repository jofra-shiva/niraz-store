from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)  # Will auto-use Cloudinary if designated
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Decimals are correct for database transactions
    discount_percent = models.PositiveIntegerField(default=0)  # E.g. 40
    stock = models.PositiveIntegerField(default=10)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # We also keep track of product emojis for direct front-end visual mapping, matching the uploaded visual layout!
    emoji = models.CharField(max_length=10, default="👔")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def sale_price(self):
        """Calculates price after applying discount_percent."""
        if self.discount_percent > 0:
            discount_amount = (self.price * self.discount_percent) / 100
            return self.price - discount_amount
        return self.price

    @property
    def price_as_int(self):
        return int(self.price)

    @property
    def sale_price_as_int(self):
        return int(self.sale_price)

    @property
    def original_price_as_int(self):
        # original price in uploaded templates was original price, and price was the sale price.
        # Let's align exactly: 
        # In base models: 'price' is original price, and 'price_after_discount' is current sale price.
        # Thus:
        # Original Price = Product.price
        # Sale Price = Product.sale_price
        return int(self.price)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"Image for {self.product.name} (Order: {self.display_order})"
