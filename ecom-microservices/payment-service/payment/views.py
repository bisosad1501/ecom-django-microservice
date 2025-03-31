import requests
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer, PaymentUpdateSerializer

ORDER_SERVICE_URL = "http://order-service:8007/orders"

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PaymentUpdateSerializer
        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data.get('order_id')
        method = serializer.validated_data.get('method')
        payment_gateway = serializer.validated_data.get('payment_gateway', method)

        # Lấy thông tin order
        order_data = self._get_order_data(order_id)
        if not order_data:
            return Response({"error": "Không tìm thấy đơn hàng."}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra payment method phải khớp với order
        order_payment_method = order_data.get('payment_method', '').lower()
        if order_payment_method != method.lower():
            return Response(
                {
                    "error": f"Payment method không khớp với order. Order yêu cầu {order_payment_method}, "
                             f"nhưng payment được tạo với {method}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = order_data.get('total_price')
        if not amount:
            return Response({"error": "Lỗi lấy tổng tiền từ đơn hàng."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                payment = Payment.objects.create(
                    order_id=order_id,
                    method=method,
                    payment_gateway=payment_gateway,
                    amount=amount,
                    status='pending'
                )
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _get_order_data(self, order_id):
        try:
            response = requests.get(f"{ORDER_SERVICE_URL}/{order_id}/", timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            return None
        return None

    @action(detail=True, methods=['put'], url_path='update-status')
    def update_status(self, request, pk=None):
        payment = self.get_object()
        new_status = request.data.get('status')
        transaction_id = request.data.get('transaction_id', None)

        if not new_status:
            return Response({"error": "Thiếu trạng thái thanh toán."}, status=status.HTTP_400_BAD_REQUEST)

        payment.update_status(new_status, transaction_id)
        return Response(PaymentSerializer(payment).data)

    @action(detail=False, methods=['get'], url_path='user-payments')
    def user_payments(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "Thiếu user_id."}, status=status.HTTP_400_BAD_REQUEST)

        payments = Payment.objects.filter(order__user_id=user_id).order_by('-created_at')
        return Response(PaymentSerializer(payments, many=True).data)

    @action(detail=True, methods=['post'], url_path='refund')
    def refund(self, request, pk=None):
        payment = self.get_object()
        if payment.status != 'completed':
            return Response({"error": "Chỉ có thể hoàn tiền cho giao dịch đã thanh toán."}, status=status.HTTP_400_BAD_REQUEST)

        refund_amount = request.data.get('refund_amount', payment.paid_amount)
        refund_reason = request.data.get('refund_reason', "")

        payment.update_status('refunded')
        payment.refund_amount = refund_amount
        payment.refund_reason = refund_reason
        payment.save()

        return Response(PaymentSerializer(payment).data)

    @action(detail=False, methods=['get'], url_path='verify-payment')
    def verify_payment(self, request):
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response({"error": "Thiếu order_id"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.filter(order_id=order_id, status='completed').first()
        if payment:
            return Response({
                "verified": True,
                "payment_id": str(payment.id),
                "transaction_id": payment.transaction_id,
                "paid_amount": payment.paid_amount,
                "payment_date": payment.payment_date,
                "method": payment.method
            })

        return Response({"verified": False, "message": "Không tìm thấy thanh toán hợp lệ."}, status=status.HTTP_404_NOT_FOUND)