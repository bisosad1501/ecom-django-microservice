# shipping/serializers.py
from rest_framework import serializers
from .models import Shipment, ShippingHistory


class ShippingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingHistory
        fields = ['id', 'status', 'notes', 'created_at']


class ShipmentSerializer(serializers.ModelSerializer):
    history = ShippingHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = ['id', 'order', 'status', 'carrier', 'tracking_number',
                  'shipping_cost', 'estimated_delivery', 'delivered_at',
                  'shipping_notes', 'created_at', 'updated_at', 'history']
        read_only_fields = ['id', 'created_at', 'updated_at', 'history', 'delivered_at']


class ShipmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['order', 'carrier', 'shipping_cost', 'estimated_delivery']


class ShipmentStatusUpdateSerializer(serializers.ModelSerializer):
    notes = serializers.CharField(required=False)

    class Meta:
        model = Shipment
        fields = ['status', 'notes']