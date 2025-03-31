from rest_framework import serializers
from .models import Order, OrderItem, OrderHistory


class OrderItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product_id', 'product_name', 'quantity', 'price', 'total']

    def get_total(self, obj):
        return obj.total


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ['id', 'order', 'status', 'notes', 'created_at', 'created_by']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    sub_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'cart_id', 'user_id', 'customer_name', 'customer_email', 'contact_phone',
            'shipping_address_line1', 'shipping_ward', 'shipping_district', 'shipping_city', 'shipping_country',
            'sub_total', 'shipping_fee', 'tax', 'discount', 'total_price',
            'status', 'payment_method', 'shipping_method', 'notes',
            'created_at', 'updated_at', 'items'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'cart_id', 'user_id', 'customer_name', 'customer_email', 'contact_phone',
            'shipping_address_line1', 'shipping_ward', 'shipping_district', 'shipping_city', 'shipping_country',
            'payment_method', 'shipping_method',
            'shipping_fee', 'tax', 'discount'
        ]


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'status', 'payment_method', 'shipping_method', 'notes',
        ]
        read_only_fields = ['user_id', 'total_price', 'sub_total']