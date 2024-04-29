from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response


from .models import PlaceOrder, Product, Cart, ReviewAndRating
from .serializers import (
    PlaceOrderSerializer,
    ProductSerializer,
    CartSerializer,
    ReviewAndRatingSerializer,
)
from .permissions import IsOwnerOrReadOnly, _IsOwnerOrReadOnly
from .utils import (
    _add_to_cart,
    _create_product,
    _create_review,
    _place_order,
    _update_cart,
    _update_product,
)

# Create your views here.


# Product Viewsets
class ProductViewsets(ModelViewSet):
    """
    Product Viewsets

    Admin View ---> create ,get ,update ,delete
    Customer View ---> get only
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    # filter_backends=[ DjangoFilterBackend]
    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = ["name", "branch", "category"]
    ordering_fields = ["brand", "category", "price"]

    def create(self, request):
        return _create_product(self, request, Product)

    def update(self, request, *args, **kwargs):
        return _update_product(self, request, *args, *kwargs)


# Cart Viewset
class CartViewsets(ModelViewSet):
    """
    Cart Viewsets

    get, create, update, delete cart item
    """

    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):

        return Cart.objects.filter(profile=self.request.user.Profile)  # type:ignore

    def create(self, request):
        return _add_to_cart(self, request, Product)

    def update(self, request, *args, **kwargs):
        return _update_cart(self, request, Product)


# Review and Rating Viewsets
class ReviewAndRatingViewsets(ModelViewSet):
    """
    all profile -> get only
    profile who reviews -> get ,create, update ,delete
    """

    queryset = ReviewAndRating.objects.all()
    serializer_class = ReviewAndRatingSerializer
    permission_classes = [IsAuthenticated, _IsOwnerOrReadOnly]

    def create(self, request):
        return _create_review(self, request)


# Place Order Viewsets
class PlaceOrderViewsets(ModelViewSet):
    queryset = PlaceOrder.objects.all()
    serializer_class = PlaceOrderSerializer
    permission_classes = [IsAuthenticated, _IsOwnerOrReadOnly]

    def get_queryset(self):
        return PlaceOrder.objects.filter(profile=self.request.user.Profile)

    def create(self, request):

        # carts = Cart.objects.filter(profile=profile)
        # order_total = 0
        # for item in carts:

        #     order_total += item.total_price  # type: ignore

        return _place_order(self, request, Cart, Product)
