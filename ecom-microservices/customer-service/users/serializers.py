from rest_framework import serializers
from .models import User
import uuid

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)  # Hiển thị UUID
    password = serializers.CharField(write_only=True)  # Không hiển thị password khi GET

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'address']
        extra_kwargs = {
            'password': {'write_only': True}  # Ẩn password trong API response
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', '')
        )
        return user