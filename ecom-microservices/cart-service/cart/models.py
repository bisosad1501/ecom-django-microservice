import uuid
from decimal import Decimal

from django.db import models

class Cart(models.Model):
    CART_TYPES = [
        ('active', 'Giỏ hàng hiện tại'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)  # UUID của user từ customer-service
    cart_type = models.CharField(
        max_length=20,
        choices=CART_TYPES,
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} - User {self.user_id}"

class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    product_id = models.CharField(max_length=24)  # Lưu ObjectId từ MongoDB dưới dạng string
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user_id', 'product_id']
        indexes = [models.Index(fields=['user_id', 'product_id'])]

    def __str__(self):
        return f"Wishlist {self.product_name} - User {self.user_id}"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_id = models.CharField(max_length=24)
    product_name = models.CharField(max_length=255)

    # Giá gốc
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Giá khuyến mãi (giá cuối cùng)
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # % Giảm giá (tùy chọn)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product_id']
        indexes = [models.Index(fields=['cart', 'product_id'])]

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    @property
    def total_item_price(self):
        return self.sale_price * self.quantity

    def calculate_savings(self):
        if self.original_price and self.original_price > self.sale_price:
            return self.original_price - self.sale_price
        return Decimal('0.00')
