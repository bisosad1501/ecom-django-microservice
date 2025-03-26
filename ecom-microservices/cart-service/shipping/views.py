# shipping/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Shipment, ShippingHistory
from .serializers import (
    ShipmentSerializer,
    ShipmentCreateSerializer,
    ShipmentStatusUpdateSerializer,
    ShippingHistorySerializer
)


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ShipmentCreateSerializer
        elif self.action == 'update_status':
            return ShipmentStatusUpdateSerializer
        return ShipmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order'].id

        # Kiểm tra xem đã có shipment cho order này chưa
        if Shipment.objects.filter(order_id=order_id).exists():
            return Response({
                "error": "Đã tồn tại thông tin vận chuyển cho đơn hàng này"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Tạo shipment và thiết lập tracking_number
        shipment = serializer.save()

        # Tạo tracking number (có thể tích hợp với API của đơn vị vận chuyển)
        import random
        import string
        tracking = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        shipment.tracking_number = tracking
        shipment.save()

        # Tạo lịch sử vận chuyển đầu tiên
        ShippingHistory.objects.create(
            shipment=shipment,
            status='pending',
            notes="Khởi tạo thông tin vận chuyển"
        )

        return Response(ShipmentSerializer(shipment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        shipment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        notes = serializer.validated_data.get('notes')

        shipment.update_status(new_status, notes)

        return Response(ShipmentSerializer(shipment).data)

    @action(detail=False, methods=['get'])
    def by_order(self, request):
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response({"error": "Thiếu order_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            shipment = Shipment.objects.get(order_id=order_id)
            return Response(ShipmentSerializer(shipment).data)
        except Shipment.DoesNotExist:
            return Response({"error": "Không tìm thấy thông tin vận chuyển"},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        shipment = self.get_object()
        history = ShippingHistory.objects.filter(shipment=shipment).order_by('-created_at')
        serializer = ShippingHistorySerializer(history, many=True)
        return Response(serializer.data)