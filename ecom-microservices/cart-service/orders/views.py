# orders/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderItemSerializer, OrderUpdateSerializer
import requests

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get('user_id')
        if not user_id:
            return Response({"error": "Thiếu user_id."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart_service_url = "http://localhost:8003"
            response = requests.get(f"{cart_service_url}/cart/get/{user_id}/")
            if response.status_code == 200:
                cart_data = response.json()
                cart_id = cart_data.get('id')
                if not cart_id:
                    return Response({"error": "Không tìm thấy cart_id cho user này"}, status=status.HTTP_404_NOT_FOUND)
                cart_items = cart_data.get('items', [])
                if not cart_items:
                    return Response({"error": "Giỏ hàng trống"}, status=status.HTTP_400_BAD_REQUEST)
                total_price = sum(item['quantity'] * float(item['sale_price']) for item in cart_items)
                order = Order.objects.create(
                    cart_id=cart_id,
                    user_id=user_id,
                    shipping_address=serializer.validated_data['shipping_address'],
                    contact_phone=serializer.validated_data['contact_phone'],
                    payment_method=request.data.get('payment_method'),
                    shipping_method=request.data.get('shipping_method'),
                    total_price=total_price,
                    status='pending'
                )
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product_id=cart_item['product_id'],
                        product_name=cart_item['product_name'],
                        quantity=cart_item['quantity'],
                        price=float(cart_item['sale_price'])
                    )
                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": f"Không thể lấy thông tin giỏ hàng. Mã lỗi: {response.status_code}"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Lỗi khi xử lý đơn hàng: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update-payment')
    def update_payment(self, request, pk=None):
        order = self.get_object()
        payment_status = request.data.get('status')
        payment_method = request.data.get('method')
        if not payment_status:
            return Response({"error": "Thiếu status thanh toán."}, status=status.HTTP_400_BAD_REQUEST)
        PaymentInfo = type('PaymentInfo', (), {})
        order.payment_info = PaymentInfo()
        order.payment_info.status = payment_status
        if payment_method:
            order.payment_method = payment_method
        order.update_status()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['put'], url_path='update-shipping')
    def update_shipping(self, request, pk=None):
        order = self.get_object()
        shipping_status = request.data.get('status')
        shipping_method = request.data.get('method')
        if not shipping_status:
            return Response({"error": "Thiếu status giao hàng."}, status=status.HTTP_400_BAD_REQUEST)
        ShipmentInfo = type('ShipmentInfo', (), {})
        order.shipment_info = ShipmentInfo()
        order.shipment_info.status = shipping_status
        if shipping_method:
            order.shipping_method = shipping_method
        order.update_status()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['put'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status == 'delivered':
            return Response({"error": "Không thể hủy đơn hàng đã giao"},
                            status=status.HTTP_400_BAD_REQUEST)
        order.status = 'cancelled'
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=False, methods=['get'])
    def user_orders(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "Thiếu user_id"}, status=status.HTTP_400_BAD_REQUEST)
        orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
        return Response(OrderSerializer(orders, many=True).data)