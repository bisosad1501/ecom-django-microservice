from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, CustomerProfile, SellerProfile, EmailVerification, PasswordReset, LoginHistory
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """🔥 Serializer chung cho User (bao gồm cả Admin, Seller, Customer)"""

    avatar_url = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "phone", "roles", "role", "status", "is_verified",
            "is_seller_request", "avatar", "avatar_url", "created_at", "updated_at",
            "is_admin", "is_seller", "is_customer"
        ]
        read_only_fields = ["id", "status", "is_verified", "created_at", "updated_at"]

    def get_avatar_url(self, obj):
        """Trả về URL ảnh đại diện"""
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return request.build_absolute_uri("/media/avatars/default.png") if request else "/media/avatars/default.png"
    
    def get_roles(self, obj):
        """Trả về danh sách vai trò của người dùng"""
        roles = []
        if hasattr(obj, 'is_admin') and obj.is_admin:
            roles.append('admin')
        if hasattr(obj, 'is_seller') and obj.is_seller:
            roles.append('seller')
        if hasattr(obj, 'is_customer') and obj.is_customer:
            roles.append('customer')
        return roles


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        exclude = ['user']


class CustomerSerializer(UserSerializer):
    """🔥 Serializer cho khách hàng (Customer)"""
    customer_profile = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ["customer_profile"]

    def get_customer_profile(self, obj):
        if hasattr(obj, "customer_profile"):
            profile = obj.customer_profile
            profile_data = {
                "address": profile.address,
                "province": profile.province,
                "district": profile.district,
                "ward": profile.ward,
                "postal_code": profile.postal_code,
                "country": profile.country,
                "customer_type": profile.customer_type,
                "loyalty_points": profile.loyalty_points,
                # Thông tin thống kê bổ sung
                "last_active": profile.last_active,
                "total_orders": profile.total_orders,
                "completed_orders": profile.completed_orders,
                "cancelled_orders": profile.cancelled_orders,
                "total_spent": profile.total_spent,
                "last_purchase": profile.last_purchase_at,
                "purchase_frequency": profile.purchase_frequency,
                "avg_order_value": profile.avg_order_value,
                "lifetime_value": profile.lifetime_value,
                "churn_risk": profile.churn_risk,
                # Thông tin tương tác
                "review_count": profile.review_count,
                "avg_rating": profile.avg_rating,
                "return_rate": profile.return_rate,
                "support_tickets": profile.support_tickets,
                # Hành vi
                "preferred_categories": profile.preferred_categories,
                "preferred_payment_method": profile.preferred_payment_method,
                "preferred_shipping_method": profile.preferred_shipping_method,
                # Tiếp thị
                "marketing_emails": profile.marketing_emails,
                "sms_notifications": profile.sms_notifications,
                "referral_code": profile.referral_code,
                "referred_users_count": profile.referred_users_count,
            }
            return profile_data
        return None


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        exclude = ['user']


class SellerSerializer(UserSerializer):
    """🔥 Serializer cho người bán (Seller)"""
    seller_profile = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ["seller_profile"]

    def get_seller_profile(self, obj):
        if hasattr(obj, "seller_profile"):
            profile = obj.seller_profile
            profile_data = {
                "store_name": profile.store_name,
                "store_description": profile.store_description,
                "store_logo": profile.get_store_logo_url() if hasattr(profile, 'get_store_logo_url') else None,
                "total_sales": profile.total_sales,
                "store_rating": profile.store_rating,
                # Thông số hiệu suất 
                "products_count": profile.products_count if hasattr(profile, 'products_count') else 0,
                "avg_shipping_time": profile.avg_shipping_time if hasattr(profile, 'avg_shipping_time') else None,
                "return_rate": profile.return_rate if hasattr(profile, 'return_rate') else 0,
                "response_time": profile.response_time if hasattr(profile, 'response_time') else None,
                # Trạng thái xác minh
                "is_identity_verified": profile.is_identity_verified if hasattr(profile, 'is_identity_verified') else False,
                "is_business_verified": profile.is_business_verified if hasattr(profile, 'is_business_verified') else False,
                "opened_since": profile.opened_since if hasattr(profile, 'opened_since') else None,
                "last_active": profile.last_active if hasattr(profile, 'last_active') else None,
            }
            return profile_data
        return None


class UserRegisterSerializer(serializers.ModelSerializer):
    """🔥 Serializer đăng ký tài khoản"""
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password', 'confirm_password', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Mật khẩu không khớp"})
            
        return attrs
    
    def create(self, validated_data):
        # Loại bỏ trường confirm_password
        validated_data.pop('confirm_password', None)
        
        # Đảm bảo first_name và last_name có giá trị
        if 'first_name' not in validated_data or validated_data['first_name'] is None:
            validated_data['first_name'] = ''
        
        if 'last_name' not in validated_data or validated_data['last_name'] is None:
            validated_data['last_name'] = ''
        
        # Tạo user với role mặc định là customer
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data.get('phone'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_customer=True,
            is_seller=False,
            is_admin=False,
            role='customer'  # Giữ lại cho khả năng tương thích ngược
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        # Tạo customer profile với tất cả các trường cần thiết
        CustomerProfile.objects.create(
            user=user,
            address='',
            province=None,
            district=None,
            ward=None,
            postal_code=None,
            country='Việt Nam',
            date_of_birth=None
        )
        
        return user


class SellerRequestSerializer(serializers.Serializer):
    """🔥 Serializer xử lý yêu cầu trở thành người bán"""
    store_name = serializers.CharField(max_length=100, required=True)
    business_license_number = serializers.CharField(max_length=50, required=True)
    bank_account_number = serializers.CharField(max_length=50, required=True)
    bank_name = serializers.CharField(max_length=100, required=True)
    
    def validate_business_license_number(self, value):
        # Kiểm tra xem giấy phép kinh doanh đã được đăng ký chưa
        if SellerProfile.objects.filter(business_license_number=value).exists():
            raise serializers.ValidationError("Giấy phép kinh doanh đã được đăng ký")
        return value
    
    def validate_bank_account_number(self, value):
        # Kiểm tra định dạng số tài khoản ngân hàng
        if not value.isdigit():
            raise serializers.ValidationError("Số tài khoản ngân hàng chỉ được chứa số")
        return value


class ApproveSellerSerializer(serializers.Serializer):
    """🔥 Serializer xử lý phê duyệt yêu cầu trở thành người bán"""
    approved = serializers.BooleanField(required=True)
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)


class AdminCreateUserSerializer(serializers.ModelSerializer):
    """🔥 Serializer để Admin tạo tài khoản mới (Admin hoặc Seller)"""

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "role"]

    def create(self, validated_data):
        """Admin tạo tài khoản mới"""
        role = validated_data["role"]
        if role not in [User.Role.ADMIN, User.Role.SELLER]:
            raise serializers.ValidationError("Admin chỉ có thể tạo tài khoản Admin hoặc Seller.")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            password=validated_data["password"]
        )

        user.role = role
        user.status = User.AccountStatus.ACTIVE
        user.is_verified = True
        user.save()

        # Nếu là Seller, tạo profile Seller luôn
        if role == User.Role.SELLER:
            SellerProfile.objects.create(user=user)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """🔥 Serializer để cập nhật thông tin cá nhân người dùng"""
    id = serializers.UUIDField(read_only=True)
    customer_profile = CustomerSerializer(required=False)
    seller_profile = SellerSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "phone", "avatar",
            "customer_profile", "seller_profile"
        ]
        read_only_fields = ["username"]  # Không cho phép đổi username

    def update(self, instance, validated_data):
        """Cập nhật thông tin user, đảm bảo hỗ trợ cả Customer & Seller"""
        if 'customer_profile' in validated_data:
            customer_profile_data = validated_data.pop('customer_profile')
            if hasattr(instance, "customer_profile"):
                CustomerProfile.objects.filter(user=instance).update(**customer_profile_data)
            else:
                CustomerProfile.objects.create(user=instance, **customer_profile_data)

        if 'seller_profile' in validated_data:
            seller_profile_data = validated_data.pop('seller_profile')
            if hasattr(instance, "seller_profile"):
                SellerProfile.objects.filter(user=instance).update(**seller_profile_data)
            else:
                SellerProfile.objects.create(user=instance, **seller_profile_data)

        # Cập nhật thông tin cơ bản của user
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Tùy chỉnh dữ liệu trả về: Seller vẫn có thể có CustomerProfile"""
        ret = super().to_representation(instance)

        # Nếu User là Seller nhưng vẫn có CustomerProfile, giữ lại cả hai
        if instance.role == User.Role.CUSTOMER:
            ret.pop('seller_profile', None)
        elif instance.role == User.Role.SELLER:
            # Kiểm tra xem có `customer_profile` không, nếu có thì giữ lại
            if not hasattr(instance, "customer_profile"):
                ret.pop('customer_profile', None)

        return ret


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.', code='authorization')
            attrs['user'] = user
            return attrs
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer thay đổi mật khẩu"""
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_('Mật khẩu hiện tại không chính xác.'))
        return value
    
    def validate_new_password(self, value):
        try:
            validate_password(value, self.context['request'].user)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer yêu cầu đặt lại mật khẩu"""
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            # Không trả lỗi tại đây để tránh tiết lộ thông tin tài khoản
            # nhưng vẫn lưu trữ để dùng trong quá trình tạo token
            pass
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer xác nhận đặt lại mật khẩu"""
    token = serializers.UUIDField(required=True)
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})
    
    def validate_token(self, value):
        try:
            self.reset_request = PasswordReset.objects.get(token=value, is_used=False)
            if not self.reset_request.is_valid():
                raise serializers.ValidationError(_('Token đã hết hạn.'))
        except PasswordReset.DoesNotExist:
            raise serializers.ValidationError(_('Token không hợp lệ.'))
        return value
    
    def validate_new_password(self, value):
        try:
            validate_password(value, self.reset_request.user)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def save(self):
        user = self.reset_request.user
        user.set_password(self.validated_data['new_password'])
        user.save()
        
        # Đánh dấu token đã được sử dụng
        self.reset_request.is_used = True
        self.reset_request.save()
        
        return user


class EmailVerificationSerializer(serializers.Serializer):
    """Serializer xác thực email"""
    token = serializers.UUIDField(required=True)
    
    def validate_token(self, value):
        try:
            self.verification = EmailVerification.objects.get(token=value, is_used=False)
            if not self.verification.is_valid():
                raise serializers.ValidationError(_('Token xác thực đã hết hạn.'))
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError(_('Token xác thực không hợp lệ.'))
        return value
    
    def save(self):
        user = self.verification.user
        user.is_verified = True
        if user.status == 'pending':
            user.status = 'active'
        user.save()
        
        # Đánh dấu token đã được sử dụng
        self.verification.is_used = True
        self.verification.save()
        
        return user


class TwoFactorSetupSerializer(serializers.Serializer):
    """Serializer thiết lập 2FA"""
    enable = serializers.BooleanField(required=True)
    code = serializers.CharField(required=False, min_length=6, max_length=6)
    
    def validate(self, attrs):
        user = self.context['request'].user
        enable = attrs.get('enable')
        
        if enable and not user.otp_secret:
            # Tạo mới secret nếu chưa có khi bật 2FA
            user.generate_otp_secret()
        
        if enable and not 'code' in attrs:
            # Nếu bật 2FA mà chưa cung cấp code, trả về lỗi
            raise serializers.ValidationError({
                'code': _('Vui lòng nhập mã xác thực để kích hoạt 2FA.')
            })
        
        if enable and 'code' in attrs:
            # Xác thực mã OTP khi bật 2FA
            if not user.verify_otp(attrs['code']):
                raise serializers.ValidationError({
                    'code': _('Mã xác thực không chính xác.')
                })
        
        return attrs
    
    def save(self):
        user = self.context['request'].user
        enable = self.validated_data['enable']
        
        if enable:
            user.enable_2fa()
        else:
            user.disable_2fa()
        
        return user


class TwoFactorVerifySerializer(serializers.Serializer):
    """Serializer xác thực 2FA"""
    user_id = serializers.UUIDField(required=True)
    code = serializers.CharField(required=True, min_length=6, max_length=6)
    
    def validate(self, attrs):
        try:
            user = User.objects.get(id=attrs['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'user_id': _('Người dùng không tồn tại.')
            })
        
        if not user.is_2fa_enabled:
            raise serializers.ValidationError({
                'detail': _('Người dùng chưa bật xác thực hai yếu tố.')
            })
        
        if not user.verify_otp(attrs['code']):
            raise serializers.ValidationError({
                'code': _('Mã xác thực không chính xác.')
            })
        
        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    """Serializer đăng xuất"""
    refresh_token = serializers.CharField(required=True)


class LoginHistorySerializer(serializers.ModelSerializer):
    """Serializer lịch sử đăng nhập"""
    class Meta:
        model = LoginHistory
        fields = ['id', 'ip_address', 'user_agent', 'location', 'device', 'login_time', 'success']
        read_only_fields = fields


class UserDetailSerializer(UserSerializer):
    """🔥 Serializer chi tiết cho User, bao gồm cả customer_profile và seller_profile"""
    customer_profile = CustomerProfileSerializer(required=False)
    seller_profile = SellerProfileSerializer(required=False)
    
    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ['customer_profile', 'seller_profile']


class SellerFullDetailSerializer(UserDetailSerializer):
    """🔥 Serializer chi tiết đầy đủ cho Seller, bao gồm thông tin profile"""
    class Meta(UserDetailSerializer.Meta):
        model = User
        fields = UserDetailSerializer.Meta.fields