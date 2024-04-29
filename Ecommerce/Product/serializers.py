from rest_framework import serializers

from .models import Product, Cart, ReviewAndRating, PlaceOrder

# Serializers


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "url",
            "profile",
            "id",
            "image",
            "name",
            "description",
            "brand",
            "category",
            "price",
            "stock_quantity",
            "in_stock",
            "is_active",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "in_stock": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "url",
            "id",
            "profile",
            "product",
            "quantity",
            "total_price",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "profile": {"read_only": True},
            "total_price": {"read_only": True},
        }


# Rating and Review Serializer
class ReviewAndRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAndRating
        fields = ["url", "id", "profile", "product", "review", "rating", "review"]
        extra_kwargs = {
            "profile": {"read_only": True},
        }


# Place Order
class PlaceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOrder
        fields = [
            "url",
            "id",
            "profile",
            "products",
            "shipping_address",
            "payment",
            "order_total",
            "created_at",
            "updated_at",
            "order_status",
        ]
        extra_kwargs = {
            "profile": {"read_only": True},
            "order_total": {"read_only": True},
            "products": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "order_status": {"read_only": True},
        }
