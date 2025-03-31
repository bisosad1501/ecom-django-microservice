import uuid
from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Nháp'),
        ('pending_payment', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('processing', 'Đang xử lý'),
        ('ready_to_ship', 'Sẵn sàng giao hàng'),
        ('shipped', 'Đang giao hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
        ('refunded', 'Đã hoàn tiền'),
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

    # External IDs để liên kết với Payment và Shipping Service
    external_payment_id = models.UUIDField(null=True, blank=True, help_text="ID từ Payment Service")
    external_shipping_id = models.UUIDField(null=True, blank=True, help_text="ID từ Shipping Service")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relations
    coupon = models.ForeignKey('Coupon', null=True, on_delete=models.SET_NULL)

    def update_status(self, payment_status=None, shipping_status=None):
        """
        Cập nhật trạng thái đơn hàng dựa trên Payment Service & Shipping Service.
        """
        if self.status == 'cancelled':
            return

        # Nếu Payment Service báo thanh toán thành công
        if payment_status == 'completed':
            if shipping_status == 'delivered':
                self.status = 'delivered'
            elif shipping_status == 'shipped':
                self.status = 'shipped'
            elif shipping_status == 'ready_to_ship':
                self.status = 'ready_to_ship'
            else:
                self.status = 'processing'

        # Nếu Payment bị hoàn tiền
        elif payment_status == 'refunded':
            self.status = 'refunded'

        self.save()

    def calculate_total(self):
        """
        Tự động tính tổng giá trị đơn hàng dựa trên OrderItems.
        """
        self.sub_total = sum(item.total for item in self.items.all())
        self.total_price = self.sub_total + self.shipping_fee + self.tax - self.discount
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.status}"


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
        """
        Khi OrderItem thay đổi, cập nhật tổng giá trị của Order.
        """
        super().save(*args, **kwargs)
        self.order.calculate_total()


class OrderHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    notes = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.UUIDField()