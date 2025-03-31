# book/serializers.py
from rest_framework import serializers
from .models import Book, BookFormat

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_product_id(self, value):
        if self.instance and self.instance.product_id != value:
            raise serializers.ValidationError("Không thể thay đổi product_id")
        return value

    def validate_isbn_13(self, value):
        if not value or len(value) != 13:
            raise serializers.ValidationError("ISBN-13 must be 13 characters long")
        return value

    def validate_book_format(self, value):
        if value not in [choice[0] for choice in BookFormat.choices]:
            raise serializers.ValidationError("Invalid book format")
        return value

    def validate(self, data):
        if not isinstance(data.get('authors', []), list):
            raise serializers.ValidationError({"authors": "Must be a list"})
        if not isinstance(data.get('table_of_contents', []), list):
            raise serializers.ValidationError({"table_of_contents": "Must be a list"})
        return data