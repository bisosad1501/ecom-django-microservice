from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
import pyotp
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from django.conf import settings
import datetime
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Model User tùy chỉnh với roles, status, profiles."""
    
    # Định nghĩa cho role (đa vai trò)
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Quản trị viên')
        SELLER = 'seller', _('Người bán')
        CUSTOMER = 'customer', _('Khách hàng')
    
    # Định nghĩa trạng thái tài khoản
    class Status(models.TextChoices):
        PENDING = 'pending', _('Chờ xác thực')
        ACTIVE = 'active', _('Hoạt động')
        BANNED = 'banned', _('Bị cấm')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Thay đổi từ role đơn lẻ thành 3 boolean fields
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    # Giữ lại trường role cho khả năng tương thích ngược (không sử dụng trực tiếp)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
    
    # Các trường khác
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Trường quan hệ với seller
    is_seller_request = models.BooleanField(default=False)
    
    # Fields cho 2FA
    is_2fa_enabled = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=100, blank=True, null=True)
    otp_qr = models.CharField(max_length=255, blank=True, null=True)
    
    # Timestamp
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    # Hàm helper cho permissions
    def get_roles(self):
        """Trả về danh sách tất cả vai trò của người dùng"""
        roles = []
        if self.is_admin:
            roles.append('admin')
        if self.is_seller:
            roles.append('seller')
        if self.is_customer:
            roles.append('customer')
        return roles
    
    def add_role(self, role):
        """Thêm vai trò cho người dùng"""
        if role == self.Role.ADMIN:
            self.is_admin = True
        elif role == self.Role.SELLER:
            self.is_seller = True
        elif role == self.Role.CUSTOMER:
            self.is_customer = True
        self.save()
    
    def remove_role(self, role):
        """Xóa vai trò của người dùng"""
        if role == self.Role.ADMIN:
            self.is_admin = False
        elif role == self.Role.SELLER:
            self.is_seller = False
        elif role == self.Role.CUSTOMER:
            self.is_customer = False
        self.save()
    
    # Các hàm utility cho permission
    @property
    def is_admin_user(self):
        """Kiểm tra xem user có phải admin không"""
        return self.is_admin
    
    @property
    def is_seller_user(self):
        """Kiểm tra xem user có phải seller không"""
        return self.is_seller
    
    @property
    def is_customer_user(self):
        """Kiểm tra xem user có phải customer không"""
        return self.is_customer
    
    @property
    def has_seller_profile(self):
        """Kiểm tra xem user có SellerProfile không"""
        return hasattr(self, 'seller_profile')
    
    @property
    def has_customer_profile(self):
        """Kiểm tra xem user có CustomerProfile không"""
        return hasattr(self, 'customer_profile')

    def get_avatar_url(self):
        """Trả về URL avatar hoặc ảnh mặc định nếu chưa có"""
        if self.avatar:
            return self.avatar.url
        return "/media/avatars/default.png"

    def reset_avatar(self):
        """Xóa avatar về ảnh mặc định"""
        self.avatar = "avatars/default.png"
        self.save()
        
    def generate_otp_secret(self):
        """Tạo secret key cho 2FA"""
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
            self.save(update_fields=['otp_secret'])
        return self.otp_secret
    
    def get_otp_uri(self):
        """Tạo URI cho Google Authenticator"""
        if not self.otp_secret:
            self.generate_otp_secret()
        totp = pyotp.TOTP(self.otp_secret)
        return totp.provisioning_uri(name=self.email, issuer_name="Ecommerce Platform")
    
    def generate_qr_code(self):
        """Tạo QR code cho 2FA"""
        if not self.otp_secret:
            self.generate_otp_secret()
            
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.get_otp_uri())
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        self.otp_qr.save(f"otp_qr_{self.id}.png", 
                         ContentFile(buffer.read()), 
                         save=True)
        return self.otp_qr
        
    def verify_otp(self, code):
        """Xác thực OTP code"""
        if not self.otp_secret:
            return False
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(code)
    
    def enable_2fa(self):
        """Bật xác thực hai yếu tố"""
        if not self.otp_secret:
            self.generate_otp_secret()
        self.is_2fa_enabled = True
        self.save(update_fields=['is_2fa_enabled'])
        self.generate_qr_code()
        return True
    
    def disable_2fa(self):
        """Tắt xác thực hai yếu tố"""
        self.is_2fa_enabled = False
        self.otp_secret = None
        
        # Remove the QR code image
        if self.otp_qr:
            self.otp_qr.delete(save=False)
            self.otp_qr = None
            
        self.save(update_fields=['is_2fa_enabled', 'otp_secret', 'otp_qr'])
        return True


class EmailVerification(models.Model):
    """Model xác thực email người dùng"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_verifications")
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Email verification for {self.user.email}"
    
    def is_valid(self):
        """Kiểm tra token còn hiệu lực không"""
        return not self.is_used and self.expires_at > timezone.now()
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=1)
        super().save(*args, **kwargs)


class PasswordReset(models.Model):
    """Model đặt lại mật khẩu"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="password_resets")
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Password reset for {self.user.email}"
    
    def is_valid(self):
        """Kiểm tra token còn hiệu lực không"""
        return not self.is_used and self.expires_at > timezone.now()
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)


class LoginHistory(models.Model):
    """Model lịch sử đăng nhập"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_history")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    device = models.CharField(max_length=255, null=True, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Login by {self.user.username} at {self.login_time}"
    
    class Meta:
        ordering = ['-login_time']
        verbose_name = "Lịch sử đăng nhập"
        verbose_name_plural = "Lịch sử đăng nhập"


class AuditLog(models.Model):
    """🔥 Model lưu trữ nhật ký hành động quan trọng trong hệ thống"""
    
    class ActionType(models.TextChoices):
        USER_CREATE = 'user_create', _('Tạo tài khoản')
        USER_UPDATE = 'user_update', _('Cập nhật tài khoản')
        USER_DELETE = 'user_delete', _('Xóa tài khoản')
        USER_BAN = 'user_ban', _('Khóa tài khoản')
        USER_UNBAN = 'user_unban', _('Mở khóa tài khoản')
        SELLER_REQUEST = 'seller_request', _('Yêu cầu trở thành người bán')
        SELLER_APPROVE = 'seller_approve', _('Phê duyệt người bán')
        SELLER_REJECT = 'seller_reject', _('Từ chối người bán')
        SECURITY_CHANGE = 'security_change', _('Thay đổi bảo mật')
        PAYMENT_VERIFY = 'payment_verify', _('Xác minh thanh toán')
        IDENTITY_VERIFY = 'identity_verify', _('Xác minh danh tính')
        ADMIN_ACTION = 'admin_action', _('Thao tác admin khác')
        USER_DATA_ACCESS = 'user_data_access', _('Truy cập dữ liệu người dùng')
        SELLER_DATA_ACCESS = 'seller_data_access', _('Truy cập dữ liệu người bán')
        SECURITY_ALERT = 'security_alert', _('Cảnh báo bảo mật')
        SUSPICIOUS_LOGIN = 'suspicious_login', _('Đăng nhập đáng ngờ')
        LOGIN_ATTEMPT = 'login_attempt', _('Nỗ lực đăng nhập')
    
    # Thông tin cơ bản
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action_type = models.CharField(max_length=20, choices=ActionType.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Người thực hiện và đối tượng
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_actions')
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_targets')
    
    # Thông tin chi tiết
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    description = models.TextField()
    
    # Chi tiết thay đổi (JSON)
    previous_state = models.JSONField(null=True, blank=True)
    new_state = models.JSONField(null=True, blank=True)
    
    # Thông tin phê duyệt (cho các hành động cần phê duyệt)
    requires_approval = models.BooleanField(default=False)
    approved = models.BooleanField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approvals')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_action_type_display()} by {self.actor.username} at {self.timestamp}"
    
    @classmethod
    def log_action(cls, action_type, actor, target_user=None, description=None, 
                  previous_state=None, new_state=None, request=None, 
                  requires_approval=False):
        """
        Tạo log hành động mới
        
        Args:
            action_type: Loại hành động
            actor: User thực hiện
            target_user: User bị tác động (nếu có)
            description: Mô tả hành động
            previous_state: Trạng thái trước khi thay đổi (dict)
            new_state: Trạng thái sau khi thay đổi (dict)
            request: HttpRequest object (để lấy IP, User-Agent)
            requires_approval: Hành động có cần phê duyệt không
        """
        ip_address = None
        user_agent = None
        
        if request:
            ip_address = cls.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        log = cls.objects.create(
            action_type=action_type,
            actor=actor,
            target_user=target_user,
            description=description or f"{action_type} action",
            previous_state=previous_state,
            new_state=new_state,
            ip_address=ip_address,
            user_agent=user_agent,
            requires_approval=requires_approval
        )
        return log
    
    @staticmethod
    def get_client_ip(request):
        """Lấy IP của client từ request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Nhật ký hệ thống"
        verbose_name_plural = "Nhật ký hệ thống"


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
    district = models.CharField(max_length=50, blank=True, null=True)
    ward = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, default="Việt Nam")
    
    # Thông tin bổ sung 
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], blank=True, null=True)
    
    # Số liệu tracking
    last_active = models.DateTimeField(auto_now=True)
    last_cart_activity = models.DateTimeField(null=True, blank=True)
    wishlist_count = models.PositiveIntegerField(default=0)
    cart_abandonment_rate = models.FloatField(default=0)  # Tỷ lệ bỏ giỏ hàng

    # Loại khách hàng và điểm
    customer_type = models.CharField(
        max_length=10,
        choices=CustomerType.choices,
        default=CustomerType.BRONZE
    )
    loyalty_points = models.PositiveIntegerField(default=0)
    points_earned_total = models.PositiveIntegerField(default=0)  # Tổng số điểm đã kiếm được
    points_spent = models.PositiveIntegerField(default=0)         # Số điểm đã sử dụng

    # Thống kê mua hàng
    total_orders = models.PositiveIntegerField(default=0)
    completed_orders = models.PositiveIntegerField(default=0)  # Số đơn hoàn thành
    cancelled_orders = models.PositiveIntegerField(default=0)  # Số đơn bị hủy
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_purchase_at = models.DateTimeField(null=True, blank=True)
    purchase_frequency = models.FloatField(default=0)  # Số đơn trung bình/tháng
    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Giá trị đơn hàng trung bình

    # Đánh giá và tương tác
    review_count = models.PositiveIntegerField(default=0)
    avg_rating = models.FloatField(default=0)
    return_rate = models.FloatField(default=0)  # Tỷ lệ hoàn trả
    support_tickets = models.PositiveIntegerField(default=0)  # Số lượng ticket hỗ trợ
    
    # Ưu đãi
    coupon_usage = models.PositiveIntegerField(default=0)  # Số lần sử dụng coupon
    coupon_count = models.PositiveIntegerField(default=0)  # Số coupon hiện có
    special_offers = models.JSONField(default=dict)
    
    # Thông tin hành vi
    preferred_categories = models.JSONField(default=list)  # Danh mục ưa thích
    preferred_payment_method = models.CharField(max_length=50, blank=True, null=True)  # Phương thức thanh toán ưa thích
    preferred_shipping_method = models.CharField(max_length=50, blank=True, null=True)  # Phương thức vận chuyển ưa thích
    
    # Thông tin tiếp thị
    marketing_emails = models.BooleanField(default=True)  # Đồng ý nhận email
    sms_notifications = models.BooleanField(default=True)  # Đồng ý nhận SMS
    referral_code = models.CharField(max_length=20, blank=True, null=True)  # Mã giới thiệu
    referred_users_count = models.PositiveIntegerField(default=0)  # Số người dùng đã giới thiệu
    
    # Thông tin phân tích
    lifetime_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # Giá trị vòng đời
    churn_risk = models.FloatField(default=0)  # Nguy cơ rời bỏ (0-1)
    
    # Các trường không đổi khác

    def calculate_customer_score(self):
        """Tính điểm khách hàng dựa trên nhiều yếu tố"""
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
    """🔥 Model Seller Profile với thông tin chi tiết người bán"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    
    # Thông tin cửa hàng
    store_name = models.CharField(max_length=100, null=True, blank=True)
    store_description = models.TextField(blank=True, null=True)
    store_logo = models.ImageField(upload_to='store_logos/', null=True, blank=True)
    store_banner = models.ImageField(upload_to='store_banners/', null=True, blank=True)
    
    # Thông số hiệu suất
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    store_rating = models.FloatField(default=0)
    products_count = models.PositiveIntegerField(default=0)
    avg_shipping_time = models.FloatField(null=True, blank=True)  # Tính bằng ngày
    return_rate = models.FloatField(default=0)  # Tỷ lệ trả hàng (%)
    response_time = models.FloatField(null=True, blank=True)  # Thời gian phản hồi (giờ)
    
    # Xác minh và pháp lý
    is_identity_verified = models.BooleanField(default=False)
    is_business_verified = models.BooleanField(default=False)
    business_registration_number = models.CharField(max_length=50, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    
    # Thông tin ngân hàng
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_account_name = models.CharField(max_length=100, blank=True, null=True)
    bank_branch = models.CharField(max_length=100, blank=True, null=True)
    
    # Thông tin thống kê
    last_active = models.DateTimeField(auto_now=True)
    opened_since = models.DateField(auto_now_add=True)
    total_followers = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        store_name = self.store_name or f"{self.user.username}'s Store"
        return f"{store_name}"
    
    def get_store_logo_url(self):
        """Trả về URL logo cửa hàng hoặc ảnh mặc định nếu chưa có"""
        if self.store_logo:
            return self.store_logo.url
        return "/media/store_logos/default.png"
    
    def update_performance_metrics(self, products_count=None, avg_rating=None, 
                                  total_sales=None, return_rate=None):
        """Cập nhật các chỉ số hiệu suất của cửa hàng"""
        if products_count is not None:
            self.products_count = products_count
        
        if avg_rating is not None:
            self.store_rating = avg_rating
            
        if total_sales is not None:
            self.total_sales = total_sales
            
        if return_rate is not None:
            self.return_rate = return_rate
            
        self.save()
        
    class Meta:
        verbose_name = "Hồ sơ người bán"
        verbose_name_plural = "Hồ sơ người bán"