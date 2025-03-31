from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from django.utils import timezone


class User(AbstractUser):
    """🔥 Model User với các quyền Admin, Seller, Customer"""

    class Role(models.TextChoices):  # 🔥 Định nghĩa Role trong User
        ADMIN = "admin", "Admin"
        SELLER = "seller", "Người bán"
        CUSTOMER = "customer", "Người mua"

    class AccountStatus(models.TextChoices):  # 🔥 Định nghĩa AccountStatus trong User
        ACTIVE = "active", "Hoạt động"
        SUSPENDED = "suspended", "Bị khóa"
        PENDING = "pending", "Đang chờ duyệt"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, unique=True,blank=True, null=True, verbose_name="Số điện thoại")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
    status = models.CharField(max_length=10, choices=AccountStatus.choices, default=AccountStatus.PENDING)
    is_verified = models.BooleanField(default=False)
    is_seller_request = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Ảnh đại diện")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_avatar_url(self):
        """Trả về URL avatar hoặc ảnh mặc định nếu chưa có"""
        if self.avatar:
            return self.avatar.url
        return "/media/avatars/default.png"

    def reset_avatar(self):
        """Xóa avatar về ảnh mặc định"""
        self.avatar = "avatars/default.png"
        self.save()


class CustomerProfile(models.Model):
    """🔥 Model Customer Profile với 4 loại khách hàng"""

    class CustomerType(models.TextChoices):
        BRONZE = "bronze", "Khách hàng Đồng"
        SILVER = "silver", "Khách hàng Bạc"
        GOLD = "gold", "Khách hàng Vàng"
        PLATINUM = "platinum", "Khách hàng Bạch Kim"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")

    # Thông tin cơ bản
    address = models.TextField(blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)

    # Loại khách hàng và điểm
    customer_type = models.CharField(
        max_length=10,
        choices=CustomerType.choices,
        default=CustomerType.BRONZE
    )
    loyalty_points = models.PositiveIntegerField(default=0)

    # Thống kê mua hàng
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_purchase_at = models.DateTimeField(null=True, blank=True)
    purchase_frequency = models.FloatField(default=0)  # Số đơn trung bình/tháng

    # Đánh giá và tương tác
    review_count = models.PositiveIntegerField(default=0)
    avg_rating = models.FloatField(default=0)
    return_rate = models.FloatField(default=0)  # Tỷ lệ hoàn trả

    # Ưu đãi
    coupon_usage = models.PositiveIntegerField(default=0)  # Số lần sử dụng coupon
    coupon_count = models.PositiveIntegerField(default=0)  # Số coupon hiện có
    special_offers = models.JSONField(default=dict)

    def calculate_customer_score(self):
        """Tính điểm xếp hạng khách hàng dựa trên nhiều tiêu chí"""

        # 1. Điểm chi tiêu (40%)
        spend_score = min(100, (self.total_spent / 50000000) * 100) * 0.4

        # 2. Điểm tần suất mua hàng (20%)
        frequency_score = min(100, (self.purchase_frequency / 5) * 100) * 0.2

        # 3. Điểm đánh giá (15%)
        if self.review_count > 0:
            rating_score = (self.avg_rating / 5) * 100 * 0.15
        else:
            rating_score = 0

        # 4. Điểm độ tin cậy (15%)
        trust_score = max(0, (1 - self.return_rate) * 100) * 0.15

        # 5. Điểm tương tác (10%)
        engagement_score = min(100, (self.review_count / 20) * 100) * 0.1

        total_score = spend_score + frequency_score + rating_score + trust_score + engagement_score
        return total_score

    def update_customer_type(self):
        """Cập nhật loại khách hàng dựa trên điểm số tổng hợp"""
        score = self.calculate_customer_score()

        old_type = self.customer_type

        # Phân loại dựa trên điểm số
        if score >= 80:
            new_type = self.CustomerType.PLATINUM
        elif score >= 60:
            new_type = self.CustomerType.GOLD
        elif score >= 40:
            new_type = self.CustomerType.SILVER
        else:
            new_type = self.CustomerType.BRONZE

        if new_type != old_type:
            self.customer_type = new_type
            self._update_benefits()
            self.save()

    def _update_benefits(self):
        """Cập nhật quyền lợi theo loại khách hàng"""
        benefits = {
            'discount_rate': 0,
            'birthday_bonus': True,
            'free_shipping': False,
            'priority_support': False,
            'exclusive_access': False,
            'return_period': 7,
            'points_multiplier': 1.0,
            'special_events': False,
            'dedicated_support': False,
            'early_access': False
        }

        if self.customer_type == self.CustomerType.PLATINUM:
            benefits.update({
                'discount_rate': 0.15,
                'free_shipping': True,
                'priority_support': True,
                'exclusive_access': True,
                'return_period': 30,
                'points_multiplier': 2.0,
                'special_events': True,
                'dedicated_support': True,
                'early_access': True
            })
        elif self.customer_type == self.CustomerType.GOLD:
            benefits.update({
                'discount_rate': 0.10,
                'free_shipping': True,
                'priority_support': True,
                'return_period': 21,
                'points_multiplier': 1.5,
                'special_events': True,
                'early_access': True
            })
        elif self.customer_type == self.CustomerType.SILVER:
            benefits.update({
                'discount_rate': 0.05,
                'free_shipping': True,
                'return_period': 14,
                'points_multiplier': 1.2,
                'early_access': True
            })

        self.special_offers = benefits

    def add_purchase(self, amount, rating=None):
        """Ghi nhận giao dịch mới và cập nhật thống kê"""
        # Cập nhật thống kê mua hàng
        self.total_spent += amount
        self.total_orders += 1

        # Cập nhật thời gian và tần suất mua hàng
        if self.last_purchase_at:
            time_diff = timezone.now() - self.last_purchase_at
            days_diff = time_diff.days
            if days_diff > 0:
                self.purchase_frequency = (self.total_orders / (days_diff / 30))
        self.last_purchase_at = timezone.now()

        # Cập nhật đánh giá nếu có
        if rating:
            total_rating = (self.avg_rating * self.review_count) + rating
            self.review_count += 1
            self.avg_rating = total_rating / self.review_count

        # Tính điểm thưởng
        points = int(amount * self.special_offers['points_multiplier'] / 1000)
        self.loyalty_points += points

        self.update_customer_type()
        self.save()

    def record_return(self):
        """Ghi nhận đơn hàng hoàn trả"""
        if self.total_orders > 0:
            self.return_rate = (self.return_rate * self.total_orders + 1) / (self.total_orders + 1)
            self.update_customer_type()
            self.save()

    class Meta:
        verbose_name = "Hồ sơ khách hàng"
        verbose_name_plural = "Hồ sơ khách hàng"

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    store_name = models.CharField(max_length=100, blank=True, null=True)
    business_license_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    total_sales = models.PositiveIntegerField(default=0)
    store_rating = models.FloatField(default=0)
    bank_account_number = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)