from rest_framework import serializers
from .models import Cart, CartItem, Wishlist
from decimal import Decimal


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer chi tiết cho từng sản phẩm trong giỏ hàng
    """
    total_item_price = serializers.SerializerMethodField()
    savings = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product_id',
            'product_name',
            'original_price',
            'sale_price',
            'discount_percentage',
            'quantity',
            'total_item_price',
            'savings',
            'added_at'
        ]

    def get_total_item_price(self, obj):
        return obj.sale_price * obj.quantity

    def get_savings(self, obj):
        return obj.calculate_savings() * obj.quantity


class CartDetailSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items_count = serializers.SerializerMethodField()
    total_cart_value = serializers.SerializerMethodField()
    total_original_value = serializers.SerializerMethodField()
    total_savings = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'user_id',
            'cart_type',
            'created_at',
            'updated_at',
            'items',
            'total_items_count',
            'total_cart_value',
            'total_original_value',
            'total_savings'
        ]

    def get_total_items_count(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_cart_value(self, obj):
        return sum(
            item.sale_price * item.quantity
            for item in obj.items.all()
        )

    def get_total_original_value(self, obj):
        return sum(
            (item.original_price or item.sale_price) * item.quantity
            for item in obj.items.all()
        )

    def get_total_savings(self, obj):
        return sum(
            item.calculate_savings() * item.quantity
            for item in obj.items.all()
        )


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = [
            'id',
            'user_id',
            'product_id',
            'product_name',
            'product_price',
            'created_at'
        ]


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user_id', 'cart_type']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'cart',
            'product_id',
            'product_name',
            'original_price',
            'sale_price',
            'discount_percentage',
            'quantity'
        ]

    def validate(self, data):
        if data.get('quantity', 1) < 1:
            raise serializers.ValidationError("Số lượng sản phẩm phải lớn hơn 0")

        # Kiểm tra giá
        if data['sale_price'] <= 0:
            raise serializers.ValidationError("Giá sản phẩm phải lớn hơn 0")

        # Kiểm tra giá gốc (nếu có)
        if data.get('original_price') and data['original_price'] < data['sale_price']:
            raise serializers.ValidationError("Giá gốc phải lớn hơn hoặc bằng giá bán")

        return data


class WishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = [
            'user_id',
            'product_id',
            'product_name',
            'product_price'
        ]

    def validate(self, data):
        # Kiểm tra trùng lặp
        existing = Wishlist.objects.filter(
            user_id=data['user_id'],
            product_id=data['product_id']
        ).exists()

        if existing:
            raise serializers.ValidationError("Sản phẩm đã tồn tại trong danh sách yêu thích")

        return data
