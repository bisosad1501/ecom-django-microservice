# payment/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment, PaymentHistory
from .serializers import (
    PaymentSerializer,
    PaymentCreateSerializer,
    PaymentStatusUpdateSerializer,
    PaymentHistorySerializer
)
from orders.models import Order


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        elif self.action == 'update_status':
            return PaymentStatusUpdateSerializer
        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order'].id

        # Kiểm tra xem đã có payment cho order này chưa
        if Payment.objects.filter(order_id=order_id).exists():
            return Response({
                "error": "Đã tồn tại thông tin thanh toán cho đơn hàng này"
            }, status=status.HTTP_400_BAD_REQUEST)

        payment = serializer.save()

        # Tạo lịch sử thanh toán đầu tiên
        PaymentHistory.objects.create(
            payment=payment,
            status='pending',
            notes="Khởi tạo thanh toán"
        )

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        payment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        transaction_id = serializer.validated_data.get('transaction_id')

        payment.update_status(new_status, transaction_id)

        return Response(PaymentSerializer(payment).data)

    @action(detail=False, methods=['get'])
    def by_order(self, request):
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response({"error": "Thiếu order_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(order_id=order_id)
            return Response(PaymentSerializer(payment).data)
        except Payment.DoesNotExist:
            return Response({"error": "Không tìm thấy thông tin thanh toán"},
                            status=status.HTTP_404_NOT_FOUND)