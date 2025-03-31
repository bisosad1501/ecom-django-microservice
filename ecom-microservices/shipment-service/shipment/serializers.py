from rest_framework import serializers
from .models import Shipment, ShipmentItem, ShippingHistory

class ShipmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentItem
        fields = [
            'id',
            'order_item_id',
            'product_id',
            'product_name',
            'quantity',
            'price'
        ]

class ShippingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingHistory
        fields = ['id', 'status', 'notes', 'created_at', 'created_by']

class ShipmentSerializer(serializers.ModelSerializer):
    items = ShipmentItemSerializer(many=True, read_only=True)
    history = ShippingHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = [
            'id',
            'order_id',
            'status',
            'carrier',
            'tracking_number',
            'receiver_name',
            'receiver_phone',
            'shipping_address_line1',
            'shipping_ward',
            'shipping_district',
            'shipping_city',
            'shipping_country',
            'weight',
            'dimension',
            'shipping_cost',
            'shipment_fee',
            'pickup_time',
            'estimated_delivery',
            'delivered_at',
            'shipping_notes',
            'failure_reason',
            'metadata',
            'created_at',
            'updated_at',
            'items',
            'history'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ShipmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'order_id',
            'carrier',
            'receiver_name',
            'receiver_phone',
            'shipping_address_line1',
            'shipping_ward',
            'shipping_district',
            'shipping_city',
            'shipping_country',
            'weight',
            'dimension',
            'shipping_notes'
        ]

class ShipmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'status',
            'tracking_number',
            'estimated_delivery',
            'shipping_notes',
            'failure_reason',
            'metadata'
        ]