# payment/models.py
import uuid
from django.db import models

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('vnpay', 'VNPay'),
        ('momo', 'Momo'),
        ('bank', 'Chuyển khoản ngân hàng'),
        ('paypal', 'PayPal'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Chờ thanh toán'),
        ('completed', 'Đã thanh toán'),
        ('failed', 'Thanh toán thất bại'),
        ('refunded', 'Đã hoàn tiền'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='payment_info')
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def process_payment(self):
        # Xử lý thanh toán dựa trên phương thức
        pass

    def update_status(self, new_status, transaction_id=None):
        self.status = new_status
        if transaction_id:
            self.transaction_id = transaction_id
        self.save()

        # Cập nhật trạng thái đơn hàng
        self.order.update_status()

        # Ghi lại lịch sử thanh toán
        PaymentHistory.objects.create(
            payment=self,
            status=new_status,
            notes=f"Cập nhật trạng thái thanh toán sang {new_status}"
        )

class PaymentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, related_name='history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Payment.PAYMENT_STATUS)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)