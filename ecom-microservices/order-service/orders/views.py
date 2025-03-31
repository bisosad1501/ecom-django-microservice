from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import Order, OrderItem, OrderHistory
from .serializers import OrderSerializer, OrderCreateSerializer, OrderItemSerializer, OrderUpdateSerializer
import requests
from decimal import Decimal


CART_SERVICE_URL = "http://cart-service:8003"


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get('user_id')

        if not user_id:
            return Response({"error": "Thiếu user_id."}, status=status.HTTP_400_BAD_REQUEST)

        cart_data = self._get_cart_data(user_id)
        if not cart_data:
            return Response({"error": "Không tìm thấy giỏ hàng của user."}, status=status.HTTP_404_NOT_FOUND)

        cart_id = cart_data.get('id')
        cart_items = cart_data.get('items', [])

        if not cart_items:
            return Response({"error": "Giỏ hàng trống."}, status=status.HTTP_400_BAD_REQUEST)

        sub_total = sum(Decimal(item['quantity']) * Decimal(item['sale_price']) for item in cart_items)
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    cart_id=cart_id,
                    user_id=user_id,
                    customer_name=serializer.validated_data['customer_name'],
                    customer_email=serializer.validated_data['customer_email'],
                    contact_phone=serializer.validated_data['contact_phone'],
                    shipping_address_line1=serializer.validated_data['shipping_address_line1'],
                    shipping_ward=serializer.validated_data['shipping_ward'],
                    shipping_district=serializer.validated_data['shipping_district'],
                    shipping_city=serializer.validated_data['shipping_city'],
                    shipping_country=serializer.validated_data['shipping_country'],
                    payment_method=request.data.get('payment_method'),
                    shipping_method=request.data.get('shipping_method'),
                    sub_total=sub_total,
                    shipping_fee=request.data.get('shipping_fee', 0),
                    tax=request.data.get('tax', 0),
                    discount=request.data.get('discount', 0),
                    total_price=0,
                    status='pending_payment'
                )

                # Tạo OrderItem từ Cart
                order_items = [
                    OrderItem(
                        order=order,
                        product_id=item['product_id'],
                        product_name=item['product_name'],
                        quantity=item['quantity'],
                        price=Decimal(item['sale_price'])
                    ) for item in cart_items
                ]
                OrderItem.objects.bulk_create(order_items)

                order.calculate_total()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Lỗi khi tạo đơn hàng: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _get_cart_data(self, user_id):
        try:
            response = requests.get(f"{CART_SERVICE_URL}/cart/get/{user_id}/", timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            return None
        return None

    @action(detail=True, methods=['put'], url_path='update-payment')
    def update_payment(self, request, pk=None):
        order = self.get_object()
        payment_status = request.data.get("payment_status")
        transaction_id = request.data.get("transaction_id")

        if not payment_status:
            return Response(
                {"error": "Thiếu trạng thái thanh toán."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            if transaction_id:
                order.external_payment_id = transaction_id
            order.update_status(payment_status=payment_status)
            return Response(OrderSerializer(order).data)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Internal error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['put'], url_path='update-shipping')
    def update_shipping(self, request, pk=None):
        order = self.get_object()
        shipping_status = request.data.get('status')
        shipping_method = request.data.get('method')

        if not shipping_status:
            return Response({"error": "Thiếu status giao hàng."}, status=status.HTTP_400_BAD_REQUEST)

        order.shipping_method = shipping_method if shipping_method else order.shipping_method
        order.update_status(shipping_status=shipping_status)

        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['put'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status == 'delivered':
            return Response({"error": "Không thể hủy đơn hàng đã giao."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'cancelled'
        order.save()

        # Ghi lại lịch sử đơn hàng
        OrderHistory.objects.create(
            order=order,
            status='cancelled',
            notes='Đơn hàng bị hủy bởi khách hàng hoặc hệ thống',
            created_by=request.user.id  # Cần truyền user vào request
        )

        return Response(OrderSerializer(order).data)

    @action(detail=False, methods=['get'])
    def user_orders(self, request):
        """
        Lấy danh sách đơn hàng của một user.
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "Thiếu user_id."}, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
        return Response(OrderSerializer(orders, many=True).data)

    @action(detail=False, methods=['GET'], url_path='verify-purchase')
    def verify_purchase(self, request):
        """
        API để Review Service kiểm tra trạng thái mua hàng của user.
        """
        user_id = request.query_params.get('user_id')
        product_id = request.query_params.get('product_id')

        if not user_id or not product_id:
            return Response({"error": "Thiếu user_id hoặc product_id"}, status=status.HTTP_400_BAD_REQUEST)

        order_item = OrderItem.objects.filter(
            order__user_id=user_id,
            product_id=product_id,
            order__status='delivered'
        ).first()

        if order_item:
            return Response({
                'verified': True,
                'order_id': str(order_item.order.id),
                'purchase_date': order_item.order.created_at,
                'delivery_date': order_item.order.updated_at
            })

        return Response({"verified": False, "message": "Không tìm thấy đơn hàng đã giao của sản phẩm này"},
                        status=status.HTTP_404_NOT_FOUND)