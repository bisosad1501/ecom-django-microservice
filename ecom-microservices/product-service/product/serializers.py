from rest_framework import serializers
from .models import Product, ProductType, ProductStatus
import requests
from django.conf import settings
from decimal import Decimal


class ProductSerializer(serializers.ModelSerializer):    
    current_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )  # Giá hiện tại (chỉ đọc)

    category_path = serializers.JSONField(default=list)  # Danh mục cha-con
    image_urls = serializers.JSONField(default=list)  # Danh sách ảnh
    tags = serializers.JSONField(default=list)  # Tags sản phẩm
    dimensions = serializers.JSONField(default=dict)  # Kích thước (dài, rộng, cao)

    class Meta:
        model = Product
        fields = [
            "_id",
            "sku",
            "name",
            "product_type",
            "category_path",
            "base_price",
            "sale_price",
            "current_price",  # Read-only
            "quantity",
            "low_stock_threshold",
            "primary_image",
            "image_urls",
            "seller_id",
            "vendor_id",
            "brand",
            "status",
            "total_views",
            "total_sold",
            "rating",
            "review_count",
            "weight",
            "dimensions",
            "tags",
            "created_at",
            "updated_at",
            "last_sold_at",
        ]
        read_only_fields = ["_id", "created_at", "updated_at", "last_sold_at"]  # Không cho phép chỉnh sửa

    def validate_sale_price(self, value):
        """Không cho phép sale_price cao hơn base_price"""
        base_price = self.initial_data.get("base_price", None)
        if base_price and value and Decimal(value) > Decimal(base_price):
            raise serializers.ValidationError("Sale price cannot be higher than base price.")
        return value

    def validate_quantity(self, value):
        """Không cho phép số lượng âm"""
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value

    def validate_product_type(self, value):
        """Kiểm tra xem `product_type` có hợp lệ không"""
        if value not in ProductType.values:
            raise serializers.ValidationError("Invalid product type.")
        return value