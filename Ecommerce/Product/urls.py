from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Urls

router = DefaultRouter()
router.register("products", views.ProductViewsets)
router.register("cart", views.CartViewsets)
router.register("review", views.ReviewAndRatingViewsets)
router.register("place-order", views.PlaceOrderViewsets)

urlpatterns = [
    path("", include(router.urls)),
]
