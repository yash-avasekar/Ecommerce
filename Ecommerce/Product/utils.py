from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import razorpay


# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------


def _create_product(self, request, Product):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid()

    profile = request.user.Profile
    image = serializer.validated_data["image"]  # type: ignore
    name = serializer.validated_data["name"]  # type: ignore
    description = serializer.validated_data["description"]  # type: ignore
    brand = serializer.validated_data["brand"]  # type: ignore
    category = serializer.validated_data["category"]  # type: ignore
    price = serializer.validated_data["price"]  # type: ignore
    stock_quantity = serializer.validated_data["stock_quantity"]  # type: ignore
    in_stock = serializer.validated_data["in_stock"]  # type: ignore
    is_active = serializer.validated_data["is_active"]  # type: ignore

    in_stock = True if stock_quantity > 0 else False

    serializer.save(
        profile=profile,
        name=name,
        description=description,
        brand=brand,
        category=category,
        price=price,
        stock_quantity=stock_quantity,
        in_stock=in_stock,
        is_active=is_active,
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------


def _update_product(self, request, *args, **kwargs):
    product_instance = self.get_object()
    serializer = self.serializer_class(
        instance=product_instance, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)

    stock_quantity = serializer.validated_data.get("stock_quantity", product_instance.stock_quantity)  # type: ignore
    in_stock = serializer.validated_data.get("in_stock", product_instance.in_stock)  # type: ignore

    in_stock = True if stock_quantity > 0 else False
    serializer.save(in_stock=in_stock)
    return Response(serializer.data, status=status.HTTP_200_OK)


# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------


def _add_to_cart(self, request, Product):
    serializer = self.serializer_class(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)

    profile = request.user.Profile
    product = serializer.validated_data["product"]  # type:ignore
    quantity = serializer.validated_data["quantity"]  # type:ignore

    product_instance = Product.objects.get(name=product)

    total_price = product_instance.price * quantity
    serializer.save(profile=profile, quantity=quantity, total_price=total_price)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------


def _update_cart(self, request, Product):
    cart = self.get_object()
    serializer = self.serializer_class(
        instance=cart, data=request.data, partial=True, context={"request": request}
    )
    serializer.is_valid(raise_exception=True)

    quantity = serializer.validated_data["quantity"]  # type: ignore

    serializer.save(total_price=cart.product.price * quantity)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------


def _create_review(self, request):
    serializer = self.serializer_class(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save(profile=request.user.Profile)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------


def _place_order(self, request, Cart, Product):
    serializer = self.serializer_class(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)

    profile = request.user.Profile
    try:
        shipping_address = serializer.validated_data["shipping_address"]  # type: ignore
    except:
        shipping_address = profile.address

    payment = serializer.validated_data["payment"]  # type: ignore

    carts = Cart.objects.filter(profile=profile)
    order_total = 0
    products_id = []

    for item in carts:
        product = Product.objects.get(id=item.product.id)

        if product.in_stock is False:
            return Response(f"{product.name} is out of stock")

        if product.stock_quantity <= 0:
            product.in_stock = False
            product.save()
            return Response(
                f"{product.name} has only {product.stock_quantity} in stock"
            )
        else:
            product.stock_quantity -= item.quantity
            product.in_stock = True if product.stock_quantity != 0 else False
            product.save()
            order_total += product.price * item.quantity
            products_id.append(str(product.id))

    if payment == "Online_Payment":

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

        payment_data = {
            "amount": int(order_total * 100),
            "currency": "INR",
            "receipt": f"receipt_{request.user}_{order_total}",
            "payment_capture": 1,
        }

        try:
            razor_payment = client.order.create(data=payment_data)  # type: ignore
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer.save(
        profile=profile,
        products=products_id,
        shipping_address=shipping_address,
        order_total=order_total,
        payment=payment,
        order_status="Processing",
    )

    carts.delete()

    return Response(serializer.data, status=status.HTTP_201_CREATED)
