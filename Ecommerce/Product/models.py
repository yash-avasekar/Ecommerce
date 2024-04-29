import uuid
from django.db import models

from Profile.models import Profile

# Create your models here.


# Product
class Product(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/product_image/", null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    brand = models.CharField(null=True, blank=True, max_length=50)
    category = models.CharField(null=True, blank=True, max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )

    class Meta:
        ordering = [
            "-in_stock",
            "-created_at",
        ]

    def __str__(self):
        return self.name


# Cart
class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return f"{self.profile.username}'s Cart"


# Review and Rating
class ReviewAndRating(models.Model):
    rating = models.IntegerField(
        choices=((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")),
        null=False,
        blank=False,
    )
    review = models.TextField(max_length=500)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return f"Rating on {self.product} -> {self.rating}"


# PlaceOrder
class PlaceOrder(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    products = models.CharField(max_length=50)
    shipping_address = models.TextField(null=True, blank=True)
    payment = models.CharField(
        max_length=50,
        choices=(("Online_Payment", "Online Payment"), ("COD", "Cash On Delievry")),
    )
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_status = models.CharField(
        max_length=20,
        choices=(
            ("Pending", "Pending"),
            ("Processing", "Processing"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ),
        default="Pending",
    )
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id} by {self.profile.username}"

    @classmethod
    def create_order(cls, validated_data):
        cart = validated_data["cart"]
        default_address = cart.profile.address
        shipping_address = (
            default_address
            if validated_data["shipping_address"] is None
            else validated_data["shipping_address"]
        )
        payment = validated_data["payment"]
