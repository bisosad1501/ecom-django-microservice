from rest_framework import serializers
from .models import Shoe

class ShoeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = [
            'product_id', 'size', 'color', 'material', 'gender',
            'sport_type', 'style', 'closure_type', 'sole_material',
            'upper_material', 'waterproof', 'breathability',
            'recommended_terrain', 'warranty_period',
            'created_at', 'updated_at'
        ]