# shipping/models.py
import uuid
from django.db import models
from django.utils import timezone

class Shipment(models.Model):
    SHIPPING_STATUS = [
        ('pending', 'Chờ giao hàng'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đang vận chuyển'),
        ('delivered', 'Đã giao hàng'),
        ('failed', 'Giao hàng thất bại'),
        ('returned', 'Đã hoàn trả'),
    ]

    CARRIERS = [
        ('vnpost', 'VNPost'),
        ('ghn', 'Giao Hàng Nhanh'),
        ('ghtk', 'Giao Hàng Tiết Kiệm'),
        ('dhl', 'DHL'),
        ('other', 'Khác'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name="shipment_info")
    status = models.CharField(max_length=20, choices=SHIPPING_STATUS, default='pending')
    carrier = models.CharField(max_length=20, choices=CARRIERS)
    tracking_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_delivery = models.DateField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    shipping_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_status(self, new_status, notes=None):
        previous_status = self.status
        self.status = new_status

        if new_status == 'delivered':
            self.delivered_at = timezone.now()

        self.save()

        # Cập nhật trạng thái đơn hàng
        self.order.update_status()

        # Ghi lại lịch sử vận chuyển
        ShippingHistory.objects.create(
            shipment=self,
            status=new_status,
            notes=notes or f"Trạng thái cập nhật từ {previous_status} sang {new_status}"
        )


class ShippingHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(Shipment, related_name='history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Shipment.SHIPPING_STATUS)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)