# payment/serializers.py
from rest_framework import serializers
from .models import Payment, PaymentHistory


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = ['id', 'status', 'notes', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    history = PaymentHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'method', 'amount', 'status',
                  'transaction_id', 'created_at', 'updated_at', 'history']
        read_only_fields = ['id', 'created_at', 'updated_at', 'history']


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'method', 'amount']


class PaymentStatusUpdateSerializer(serializers.ModelSerializer):
    transaction_id = serializers.CharField(required=False)

    class Meta:
        model = Payment
        fields = ['status', 'transaction_id']