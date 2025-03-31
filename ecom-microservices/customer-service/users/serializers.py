from rest_framework import serializers
from .models import User, CustomerProfile, SellerProfile


class UserSerializer(serializers.ModelSerializer):
    """🔥 Serializer chung cho User (bao gồm cả Admin, Seller, Customer)"""

    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "phone", "role", "status", "is_verified",
            "is_seller_request", "avatar", "avatar_url", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "status", "is_verified", "created_at", "updated_at"]

    def get_avatar_url(self, obj):
        """Trả về URL ảnh đại diện"""
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return request.build_absolute_uri("/media/avatars/default.png") if request else "/media/avatars/default.png"


class CustomerSerializer(serializers.ModelSerializer):
    """🔥 Serializer cho khách hàng (Customer)"""

    class Meta:
        model = CustomerProfile
        fields = ["address", "province", "total_orders", "loyalty_points",
                  "last_purchase_at", "total_spent", "coupon_count"]


class SellerSerializer(serializers.ModelSerializer):
    """🔥 Serializer cho người bán (Seller)"""

    class Meta:
        model = SellerProfile
        fields = ["store_name", "business_license_number", "total_sales",
                  "store_rating", "bank_account_number", "bank_name"]


class UserRegisterSerializer(serializers.ModelSerializer):
    """🔥 Serializer đăng ký tài khoản mới"""

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        """Tạo user mới với vai trò mặc định là CUSTOMER"""
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        user.role = User.Role.CUSTOMER
        user.status = User.AccountStatus.PENDING
        user.save()

        # Tạo profile Customer mặc định
        CustomerProfile.objects.create(user=user)

        return user


class SellerRequestSerializer(serializers.ModelSerializer):
    """🔥 Serializer để gửi yêu cầu trở thành Seller"""

    class Meta:
        model = User
        fields = ["is_seller_request"]

    def update(self, instance, validated_data):
        """Xử lý yêu cầu đăng ký Seller"""
        if instance.role != User.Role.CUSTOMER:
            raise serializers.ValidationError("Chỉ khách hàng mới có thể yêu cầu trở thành Seller.")

        instance.is_seller_request = True
        instance.save()
        return instance


class ApproveSellerSerializer(serializers.ModelSerializer):
    """🔥 Serializer để Admin duyệt tài khoản Seller"""

    class Meta:
        model = User
        fields = ["role"]

    def update(self, instance, validated_data):
        """Xử lý duyệt tài khoản Seller"""
        if instance.role != User.Role.CUSTOMER or not instance.is_seller_request:
            raise serializers.ValidationError("Chỉ khách hàng có yêu cầu mới được duyệt làm Seller.")

        instance.role = User.Role.SELLER
        instance.is_seller_request = False
        instance.status = User.AccountStatus.ACTIVE
        instance.is_verified = True
        instance.save()

        # Nếu chưa có SellerProfile, mới tạo
        if not hasattr(instance, "seller_profile"):
            SellerProfile.objects.create(user=instance)

        return instance

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