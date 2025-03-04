from decimal import Decimal, InvalidOperation

from rest_framework import serializers
from .models import Book

class BookListSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()

    def get__id(self, obj):
        return str(obj._id)

    class Meta:
        model = Book
        fields = [
            '_id',      # ID sách
            'title',    # Tiêu đề
            'author',   # Tác giả
            'cover_image', # Ảnh bìa
            'category', # Thể loại
            'price',    # Giá
            'sale_price', # Giá khuyến mãi
            'rating'    # Đánh giá
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    # Cho phép update hình ảnh với validation
    cover_image = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    # Xử lý additional_images như một list hoặc null
    additional_images = serializers.JSONField(
        required=False,
        allow_null=True
    )

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,  # Cho phép không bắt buộc
        allow_null=True  # Cho phép null
    )

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = [
            '_id',
            'created_at',
            'updated_at',
            'rating',
            'total_reviews'
        ]
        extra_kwargs = {
            'cover_image': {'required': False},
            'additional_images': {'required': False}
        }

    def validate_price(self, value):
        # Nếu giá trị được truyền vào
        if value is not None:
            try:
                # Chuyển đổi sang Decimal
                price = Decimal(str(value))

                # Kiểm tra giá trị âm
                if price < 0:
                    raise serializers.ValidationError("Giá không thể âm")

                return price
            except (InvalidOperation, ValueError):
                raise serializers.ValidationError("Giá phải là số hợp lệ")
        return value

    def validate_isbn(self, value):
        if value and len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN phải có 10 hoặc 13 ký tự")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Số lượng tồn kho không thể âm")
        return value

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

