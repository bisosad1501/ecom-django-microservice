from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'cart_id', 'user_id', 'shipping_address', 'contact_phone',
            'total_price', 'status', 'payment_method', 'shipping_method',
            'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user_id', 'shipping_address', 'contact_phone', 'payment_method', 'shipping_method']

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['shipping_address', 'contact_phone', 'status', 'payment_method', 'shipping_method']
        extra_kwargs = {
            'shipping_address': {'required': False},
            'contact_phone': {'required': False},
            'status': {'required': False},
            'payment_method': {'required': False},
            'shipping_method': {'required': False}
        }