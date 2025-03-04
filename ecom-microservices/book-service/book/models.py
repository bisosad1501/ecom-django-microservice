from djongo import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    # Thông tin cơ bản
    _id = models.ObjectIdField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)

    # Thông tin xuất bản
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)

    # Thông tin kinh doanh
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Thông tin sản phẩm
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    subcategory = models.CharField(max_length=100, blank=True, null=True)

    # Thông tin kho và quản lý
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)

    # Thông tin chi tiết sách
    language = models.CharField(max_length=50, null=True, blank=True)
    pages = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    dimensions = models.JSONField(null=True, blank=True)

    # Hình ảnh và đa phương tiện
    cover_image = models.URLField(blank=True, null=True)
    additional_images = models.JSONField(blank=True, null=True)

    # Đánh giá và xếp hạng
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
        null=True,
        blank=True
    )
    total_reviews = models.IntegerField(default=0, null=True, blank=True)

    # Trạng thái và quản lý
    is_active = models.BooleanField(default=True, null=True)
    is_featured = models.BooleanField(default=False, null=True)

    # Thẻ và nhãn
    tags = models.JSONField(blank=True, null=True)

    # Thời gian
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'books'
        indexes = [
            models.Index(fields=['category', 'author']),
            models.Index(fields=['price']),
            models.Index(fields=['rating'])
        ]

    def __str__(self):
        return self.title or 'Unnamed Book'
