import uuid

import requests
from django.db import models
from django.utils import timezone

ORDER_SERVICE_URL = "http://order-service:8007/orders"

class Shipment(models.Model):
    SHIPPING_STATUS = [
        ('pending', 'Chờ xử lý'),
        ('picked_up', 'Đã lấy hàng'),
        ('shipped', 'Đang vận chuyển'),
        ('delivered', 'Đã giao hàng'),
        ('failed', 'Giao hàng thất bại')
    ]

    CARRIERS = [
        ('vnpost', 'VNPost'),
        ('ghn', 'Giao Hàng Nhanh'),
        ('ghtk', 'Giao Hàng Tiết Kiệm'),
        ('dhl', 'DHL'),
        ('other', 'Khác'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField(db_index=True)  # Chỉ lưu ID, không liên kết trực tiếp với Order

    # Shipping status
    status = models.CharField(max_length=20, choices=SHIPPING_STATUS, default='pending')
    carrier = models.CharField(max_length=20, choices=CARRIERS)
    tracking_number = models.CharField(max_length=50, unique=True, null=True, blank=True)

    # Receiver info
    receiver_name = models.CharField(max_length=255)
    receiver_phone = models.CharField(max_length=20)
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_ward = models.CharField(max_length=100)
    shipping_district = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100, default='Vietnam')

    # Package info
    weight = models.FloatField(default=0)  # in kg
    dimension = models.CharField(max_length=50, null=True, blank=True)  # LxWxH
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Delivery info
    pickup_time = models.DateTimeField(null=True, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    shipping_notes = models.TextField(blank=True, null=True)
    failure_reason = models.TextField(null=True, blank=True)

    # Metadata (dữ liệu bổ sung của hãng vận chuyển)
    metadata = models.JSONField(null=True, blank=True, help_text="Lưu thông tin của hãng vận chuyển")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_order_update_event()

    def update_status(self, new_status, notes=None):
        """Update shipment status and handle related logic"""
        if self.status in ['delivered', 'cancelled']:
            raise ValueError(f"Cannot update {self.status} shipment")

        if not self.tracking_number and new_status in ['processing', 'shipped']:
            raise ValueError("Tracking number required for processing/shipped status")

        old_status = self.status
        self.status = new_status

        # Handle specific statuses
        if new_status == 'confirmed':
            if not self.carrier:
                raise ValueError("Carrier required")

        elif new_status == 'picked_up':
            if not self.estimated_delivery:
                raise ValueError("Estimated delivery required")
            self.pickup_time = timezone.now()

        elif new_status == 'shipped':
            # Additional required fields for shipped status
            if not all([self.carrier, self.tracking_number]):
                raise ValueError("Carrier and tracking number required for shipped status")
            if not self.pickup_time:
                self.pickup_time = timezone.now()

        elif new_status == 'delivered':
            if not self.pickup_time:
                raise ValueError("Missing pickup time")
            self.delivered_at = timezone.now()

        elif new_status == 'failed':
            if not notes:
                raise ValueError("Failure reason required")
            self.failure_reason = notes

        self.save()

        ShippingHistory.objects.create(
            shipment=self,
            status=new_status,
            notes=notes or f"Status changed from {old_status} to {new_status}"
        )

        self.send_order_update_event()

    def send_order_update_event(self):
        status_mapping = {
            'shipped': 'shipped',
            'delivered': 'delivered',
            'failed': 'cancelled'
        }

        shipping_status = status_mapping.get(self.status)
        if shipping_status:
            payload = {
                "status": shipping_status,
                "tracking_number": self.tracking_number,
                "method": self.carrier
            }

            try:
                response = requests.put(
                    f"{ORDER_SERVICE_URL}/{self.order_id}/update-shipping/",
                    json=payload,
                    timeout=5
                )
                response.raise_for_status()
                print(f"✅ Order {self.order_id} shipping status updated: {shipping_status}")
            except Exception as e:
                print(f"❌ Error sending shipping update: {e}")

class ShipmentItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(Shipment, related_name='items', on_delete=models.CASCADE)
    order_item_id = models.UUIDField()
    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ShippingHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipment = models.ForeignKey(Shipment, related_name='history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Shipment.SHIPPING_STATUS)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.UUIDField()