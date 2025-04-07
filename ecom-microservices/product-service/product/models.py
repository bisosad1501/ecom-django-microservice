from djongo import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class ProductType(models.TextChoices):
    BOOK = 'BOOK', 'Book'
    SHOE = 'SHOE', 'Shoe'
    ELECTRONIC = 'ELECTRONIC', 'Electronic'
    CLOTHING = 'CLOTHING', 'Clothing'
    HOME_APPLIANCE = 'HOME_APPLIANCE', 'Home Appliance'  # Đồ gia dụng
    FURNITURE = 'FURNITURE', 'Furniture'  # Nội thất
    BEAUTY = 'BEAUTY', 'Beauty & Personal Care'  # Mỹ phẩm
    FOOD = 'FOOD', 'Food & Beverage'  # Thực phẩm
    SPORTS = 'SPORTS', 'Sports & Outdoors'  # Đồ thể thao
    TOYS = 'TOYS', 'Toys & Games'  # Đồ chơi
    AUTOMOTIVE = 'AUTOMOTIVE', 'Automotive'  # Đồ xe cộ
    PET_SUPPLIES = 'PET_SUPPLIES', 'Pet Supplies'  # Đồ dùng thú cưng
    HEALTH = 'HEALTH', 'Health & Wellness'  # Sản phẩm sức khỏe
    OFFICE = 'OFFICE', 'Office Supplies'  # Đồ văn phòng phẩm
    MUSIC = 'MUSIC', 'Musical Instruments'  # Nhạc cụ

class ProductStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'  # Chưa hoàn thiện, chưa bán
    ACTIVE = 'ACTIVE', 'Active'  # Đang bán bình thường
    OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out of Stock'  # Hết hàng
    DISCONTINUED = 'DISCONTINUED', 'Discontinued'  # Ngừng kinh doanh
    PRE_ORDER = 'PRE_ORDER', 'Pre-Order'  # Đặt trước
    BACK_ORDER = 'BACK_ORDER', 'Back Order'  # Chờ nhập hàng
    LIMITED = 'LIMITED', 'Limited Edition'  # Phiên bản giới hạn
    EXPIRED = 'EXPIRED', 'Expired'  # Hết hạn (cho thực phẩm, mỹ phẩm)
    RESTRICTED = 'RESTRICTED', 'Restricted'  # Bị giới hạn bán (ví dụ: hàng cấm, hàng đặc biệt)
    BANNED = 'BANNED', 'Banned'  # Bị khóa do vi phạm chính sách

class Product(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=50, choices=ProductType.choices)
    category_path = models.JSONField(default=list)

    # 🔹 **Giá cả** - Sử dụng FloatField thay vì DecimalField
    base_price = models.FloatField(validators=[MinValueValidator(0.01)])
    sale_price = models.FloatField(null=True, blank=True)

    # 🔹 **Tồn kho**
    quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)

    # 🔹 **Hình ảnh**
    primary_image = models.URLField()
    image_urls = models.JSONField(default=list, blank=True)

    # 🔹 **Thông tin nhà bán hàng**
    seller_id = models.CharField(max_length=50, null=True, blank=True)
    vendor_id = models.CharField(max_length=50, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)

    # 🔹 **Trạng thái**
    status = models.CharField(max_length=20, choices=ProductStatus.choices, default=ProductStatus.ACTIVE)

    # 🔹 **Metrics**
    total_views = models.IntegerField(default=0)
    total_sold = models.IntegerField(default=0)

    # 🔹 **Mới thêm**
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])  # ⭐ 0-5
    review_count = models.IntegerField(default=0)  # 📝 Tổng số đánh giá

    weight = models.FloatField(null=True, blank=True)  # ⚖️ Trọng lượng sản phẩm
    dimensions = models.JSONField(default=dict, blank=True)  # 📏 {'length': 30, 'width': 20, 'height': 10}

    tags = models.JSONField(default=list, blank=True)  # 🔖 ['electronics', 'gaming', 'sony']

    # 🔹 **Thời gian**
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_sold_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['product_type']),
            models.Index(fields=['status']),
            models.Index(fields=['seller_id']),
            models.Index(fields=['total_sold']),
            models.Index(fields=['brand']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def current_price(self):
        """Lấy giá hiện tại"""
        return self.sale_price if self.sale_price else self.base_price

    def update_stock(self, quantity_change: int):
        """Cập nhật số lượng tồn kho"""
        new_quantity = self.quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Stock cannot be negative")

        self.quantity = new_quantity

        if new_quantity == 0:
            self.status = ProductStatus.OUT_OF_STOCK
        elif self.status == ProductStatus.OUT_OF_STOCK and new_quantity > 0:
            self.status = ProductStatus.ACTIVE

        self.save()

    def update_metrics(self, sale_amount: float = None):
        """Cập nhật doanh số"""
        if sale_amount:
            self.total_sold += 1
        self.save()

    def save(self, *args, **kwargs):
        # Đảm bảo tính nhất quán giữa product_type và category_path
        product_type_mapping = {
            'BOOK': 'Books',
            'SHOE': 'Shoes',
            'ELECTRONIC': 'Electronics',
            'CLOTHING': 'Clothing',
            'HOME_APPLIANCE': 'Home Appliances',
            'FURNITURE': 'Furniture',
            'BEAUTY': 'Beauty & Personal Care',
            'FOOD': 'Food & Beverage',
            'SPORTS': 'Sports Equipment',
            'TOYS': 'Toys & Games',
            'AUTOMOTIVE': 'Automotive',
            'PET_SUPPLIES': 'Pet Supplies',
            'HEALTH': 'Health & Wellness',
            'OFFICE': 'Office Supplies',
            'MUSIC': 'Musical Instruments'
        }
        
        # Đảm bảo category_path không rỗng
        if not self.category_path or len(self.category_path) == 0:
            # Nếu category_path trống, tạo mặc định từ product_type
            self.category_path = [product_type_mapping.get(self.product_type, self.product_type)]
        else:
            # Đảm bảo phần tử đầu tiên khớp với product_type
            expected_category = product_type_mapping.get(self.product_type)
            if expected_category and self.category_path[0] != expected_category:
                # Ghi lại thay đổi vào log để dễ debug
                print(f"Chuẩn hóa category_path từ {self.category_path[0]} thành {expected_category} cho sản phẩm {self.name}")
                self.category_path[0] = expected_category
                
        super().save(*args, **kwargs)