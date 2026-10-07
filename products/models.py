from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    # ImgBB URL
    image = models.URLField(max_length=1000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount_percent = models.PositiveIntegerField(default=0)

    stock = models.PositiveIntegerField(default=10)

    available = models.BooleanField(default=True)

    featured = models.BooleanField(default=False)

    is_new = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    emoji = models.CharField(
        max_length=10,
        default="👔"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    @property
    def sale_price(self):
        if self.discount_percent > 0:
            discount_amount = (
                self.price * self.discount_percent
            ) / 100

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
        return int(self.price)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )

    image = models.URLField(max_length=1000)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"Image for {self.product.name} (Order: {self.display_order})"