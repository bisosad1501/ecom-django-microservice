import requests
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import (
    CartDetailSerializer,
    CartItemCreateSerializer,
    CartItemSerializer
)
from decimal import Decimal

CUSTOMER_SERVICE_URL = "http://customer-service:8001/user/list/"
PRODUCT_SERVICE_URL = "http://product-service:8005/products/"

def is_valid_user(user_id):
    try:
        response = requests.get(CUSTOMER_SERVICE_URL)
        if response.status_code != 200:
            return False

        users = response.json()
        return any(user['id'] == str(user_id) for user in users)

    except requests.exceptions.RequestException:
        return False


class CreateCartAPI(APIView):
    def post(self, request, user_id):
        if not is_valid_user(user_id):
            return Response(
                {'error': 'User không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart, created = Cart.objects.get_or_create(
            user_id=user_id,
            cart_type='active'
        )

        serializer = CartDetailSerializer(cart)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class AddItemToCartView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not user_id or not product_id:
            return Response(
                {"error": "Thiếu user_id hoặc product_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Số lượng phải lớn hơn 0")
        except ValueError:
            return Response(
                {"error": "Số lượng không hợp lệ"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product_data = self.get_product_data(product_id)
        if not product_data:
            return Response(
                {"error": "Không thể lấy thông tin sản phẩm"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = Cart.objects.get_or_create(
            user_id=user_id,
            cart_type="active"
        )

        cart_item_data = {
            'cart': cart.id,
            'product_id': str(product_id),
            'product_name': product_data.get("name", "Sản phẩm không có tên"),
            'original_price': product_data.get("base_price"),
            'sale_price': product_data.get("sale_price"),
            'discount_percentage': self.calculate_discount_percentage(
                product_data.get("base_price"),
                product_data.get("sale_price")
            ),
            'quantity': quantity
        }

        existing_item = CartItem.objects.filter(
            cart=cart,
            product_id=str(product_id)
        ).first()

        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
            serializer = CartItemSerializer(existing_item)
        else:
            serializer = CartItemCreateSerializer(data=cart_item_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def get_product_data(self, product_id):
        try:
            response = requests.get(f"{PRODUCT_SERVICE_URL}{product_id}/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def calculate_discount_percentage(self, original_price, sale_price):
        if not original_price or not sale_price:
            return None

        try:
            original = Decimal(str(original_price))
            sale = Decimal(str(sale_price))

            if original <= sale:
                return None

            discount = ((original - sale) / original) * 100
            return round(discount, 2)
        except (TypeError, ValueError):
            return None


class RemoveItemFromCartView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")

        if not user_id or not product_id:
            return Response(
                {"error": "Thiếu user_id hoặc product_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = get_object_or_404(Cart, user_id=user_id, cart_type="active")

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=str(product_id))
        cart_item.delete()

        return Response(
            {"message": "Sản phẩm đã được xóa khỏi giỏ hàng"},
            status=status.HTTP_200_OK
        )


class GetCartView(APIView):
    def get(self, request, user_id):
        cart = get_object_or_404(Cart, user_id=user_id, cart_type="active")

        serializer = CartDetailSerializer(cart)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCartItemView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not user_id or not product_id or quantity is None:
            return Response(
                {"error": "Thiếu user_id, product_id hoặc quantity"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Số lượng phải lớn hơn 0")
        except ValueError:
            return Response(
                {"error": "Số lượng không hợp lệ"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = get_object_or_404(Cart, user_id=user_id, cart_type="active")

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=str(product_id))
        cart_item.quantity = quantity
        cart_item.save()

        return Response(
            CartItemSerializer(cart_item).data,
            status=status.HTTP_200_OK
        )