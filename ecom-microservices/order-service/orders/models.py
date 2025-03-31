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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50)
    shipping_method = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relations
    coupon = models.ForeignKey('Coupon', null=True, on_delete=models.SET_NULL)

    # Thêm các trường để tracking payment và shipping
    payment_status = models.CharField(max_length=20, default='pending')
    shipping_status = models.CharField(max_length=20, default='pending')

    def update_status(self):
        if self.status == 'cancelled':
            return

        payment = self.payment_info
        shipment = self.shipment_info

        if payment and payment.status == 'completed':
            if not shipment:
                self.status = 'ready_to_ship'
            elif shipment.status == 'delivered':
                self.status = 'delivered'
            elif shipment.status == 'shipped':
                self.status = 'shipped'
            else:
                self.status = 'processing'

        elif payment and payment.status == 'refunded':
            self.status = 'refunded'

        self.save()

    def update_status(self):
        if self.status == 'cancelled':
            return

        if hasattr(self, 'payment_info'):
            payment = self.payment_info
            if payment.status == 'refunded':
                self.status = 'refunded'
            elif payment.status == 'completed':
                if hasattr(self, 'shipment_info'):
                    shipment = self.shipment_info
                    if shipment.status == 'delivered':
                        self.status = 'delivered'
                    elif shipment.status == 'shipped':
                        self.status = 'shipped'
                    else:
                        self.status = 'processing'
                else:
                    self.status = 'processing'
        self.save()

    def calculate_total(self):
        self.total_price = (
                self.sub_total
                + self.shipping_fee
                + self.tax
                - self.discount
        )
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


class OrderHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='history', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    notes = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.UUIDField()