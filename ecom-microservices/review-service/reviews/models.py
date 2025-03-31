from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class BaseReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.CharField(max_length=24, db_index=True)  # ID của sản phẩm từ MongoDB
    user_id = models.UUIDField(db_index=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True)
    media_urls = models.JSONField(default=list, blank=True)
    helpful_votes = models.IntegerField(default=0)
    not_helpful_votes = models.IntegerField(default=0)
    report_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)  # Đánh dấu nếu review bị chỉnh sửa

    class Meta:
        abstract = True  # Đây là model trừu tượng, không tạo bảng
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['user_id']),
            models.Index(fields=['rating']),
            models.Index(fields=['created_at']),
        ]

class VerifiedReview(BaseReview):
    order_id = models.CharField(max_length=100)
    purchase_date = models.DateTimeField()
    quality_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    value_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    shipping_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    seller_response = models.TextField(null=True, blank=True)
    seller_response_date = models.DateTimeField(null=True)

    class Meta:
        unique_together = ['product_id', 'user_id', 'order_id']

class GeneralReview(BaseReview):
    pass

class ReviewComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    verified_review = models.ForeignKey(VerifiedReview, null=True, blank=True, on_delete=models.CASCADE, related_name="comments")
    general_review = models.ForeignKey(GeneralReview, null=True, blank=True, on_delete=models.CASCADE, related_name="comments")
    user_id = models.UUIDField(db_index=True)  # Người dùng đăng comment
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']