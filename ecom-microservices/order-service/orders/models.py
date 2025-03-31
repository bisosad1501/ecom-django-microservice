import uuid
from decimal import Decimal
from django.apps import apps
from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending_payment', 'Chờ thanh toán'),
        ('processing', 'Đang xử lý'),
        ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
        ('refunded', 'Đã hoàn tiền')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart_id = models.UUIDField(null=True, blank=True)
    user_id = models.UUIDField(db_index=True)

    # Customer info
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    # Shipping address
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_ward = models.CharField(max_length=100)
    shipping_district = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100, default='Vietnam')

    # Pricing
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Order info
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    payment_method = models.CharField(max_length=50)
    shipping_method = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relations  coupon = models.ForeignKey('Coupon', null=True, on_delete=models.SET_NULL)

    def calculate_total(self):
        self.sub_total = sum(item.total for item in self.items.all())
        self.shipping_fee = Decimal(str(self.shipping_fee or '0'))
        self.tax = Decimal(str(self.tax or '0'))
        self.discount = Decimal(str(self.discount or '0'))

        self.total_price = (
                self.sub_total +
                self.shipping_fee +
                self.tax -
                self.discount
        )
        self.save()

    def update_status(self, payment_status=None, shipping_status=None):
        if self.status in ['delivered', 'cancelled', 'refunded']:
            raise ValueError(f"Cannot update {self.status} order")

        old_status = self.status  # Store old status before changes

        # Payment updates
        if payment_status:
            if payment_status == 'completed':
                self.status = 'processing'
            elif payment_status == 'failed':
                self.status = 'cancelled'
            elif payment_status == 'refunded':
                self.status = 'refunded'

        # Shipping updates
        if shipping_status:
            if shipping_status == 'shipped':
                self.status = 'shipping'
            elif shipping_status == 'delivered':
                self.status = 'delivered'
                if self.payment_method == 'cod':
                    # Get Payment model using lazy loading
                    Payment = apps.get_model('payment', 'Payment')
                    try:
                        payment = Payment.objects.get(order_id=self.id)
                        payment.update_status('completed')
                    except Payment.DoesNotExist:
                        print(f"❌ Payment not found for order {self.id}")

        self.save()

        # Record history if status changed
        if old_status != self.status:
            OrderHistory.objects.create(
                order=self,
                status=self.status,
                notes=f"Status changed from {old_status} to {self.status}",
                created_by=self.user_id
            )

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.calculate_total()


class OrderHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    notes = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.UUIDField()