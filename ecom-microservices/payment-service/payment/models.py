import uuid
import requests
from django.db import models
from django.utils import timezone

ORDER_SERVICE_URL = "http://order-service:8007/orders"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('vnpay', 'VNPay'),
        ('momo', 'Momo'),
        ('bank', 'Chuyển khoản ngân hàng'),
        ('paypal', 'PayPal'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Chờ thanh toán'),  # Trạng thái khởi tạo
        ('completed', 'Đã thanh toán'),
        ('failed', 'Thanh toán thất bại'),
        ('refunded', 'Đã hoàn tiền'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField(db_index=True)  # Chỉ lưu ID, không liên kết trực tiếp với Order Service

    # Payment details
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_gateway = models.CharField(max_length=50, help_text="Cổng thanh toán (VNPay, Momo, PayPal, v.v.)")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')

    # Amount info
    currency = models.CharField(max_length=3, default='VND')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    refund_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Transaction info
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_proof = models.CharField(max_length=255, null=True, blank=True)
    refund_reason = models.TextField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True, help_text="Lưu thông tin bổ sung của cổng thanh toán")

    # Timestamps
    payment_date = models.DateTimeField(null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_order_update_event()

    def update_status(self, new_status, transaction_id=None):
        if new_status not in dict(self.PAYMENT_STATUS):
            raise ValueError("Invalid payment status")

        if self.status in ['completed', 'refunded']:
            raise ValueError(f"Cannot update {self.status} payment")

        if new_status == 'completed' and self.method != 'cod' and not transaction_id:
            raise ValueError("Transaction ID required for online payment")

        old_status = self.status

        # Handle online payment completion
        if new_status == 'completed':
            if not transaction_id:
                raise ValueError("Transaction ID required for completed payment")
            self.transaction_id = transaction_id
            self.payment_date = timezone.now()
            self.paid_amount = self.amount

        # Handle refund
        elif new_status == 'refunded':
            if self.status != 'completed':
                raise ValueError("Can only refund completed payment")
            self.refund_date = timezone.now()
            self.refund_amount = self.paid_amount

        # Update status
        self.status = new_status
        self.save()

        # Create history record
        PaymentHistory.objects.create(
            payment=self,
            status=new_status,
            notes=f"Status changed from {old_status} to {new_status}"
        )

    def send_order_update_event(self):
        # Only send update for final states
        if self.status not in ['completed', 'failed', 'refunded']:
            return

        try:
            # Get current order status before updating
            response = requests.get(f"{ORDER_SERVICE_URL}/{self.order_id}/", timeout=5)
            response.raise_for_status()
            order_data = response.json()

            # Add validation for delivered status
            if (self.status == 'completed' and
                    self.method == 'cod' and
                    order_data['status'] != 'shipping'):
                raise ValueError("Order must be in shipping status before COD completion")

            # Send update
            payload = {
                "payment_status": self.status,
                "transaction_id": self.transaction_id
            }

            update_response = requests.put(
                f"{ORDER_SERVICE_URL}/{self.order_id}/update-payment/",
                json=payload,
                timeout=5
            )
            update_response.raise_for_status()
            print(f"✅ Order {self.order_id} payment status updated to {self.status}")

        except requests.exceptions.HTTPError as e:
            print(f"⚠️ Failed to update order {self.order_id}: {e.response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error sending payment update: {str(e)}")

class PaymentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, related_name='history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Payment.PAYMENT_STATUS)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
