# orders/models.py
import uuid
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ thanh toán'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã gửi hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart_id = models.UUIDField(null=True, blank=True)
    user_id = models.UUIDField(db_index=True)
    shipping_address = models.TextField()
    contact_phone = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    shipping_method = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_status(self):
        # Update status based on payment and shipping details.
        if hasattr(self, 'payment_info') and self.payment_info.status == 'completed':
            if hasattr(self, 'shipment_info'):
                if self.shipment_info.status == 'delivered':
                    self.status = 'delivered'
                elif self.shipment_info.status == 'shipped':
                    self.status = 'shipped'
                else:
                    self.status = 'processing'
            else:
                self.status = 'processing'
        self.save()


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.quantity * self.price