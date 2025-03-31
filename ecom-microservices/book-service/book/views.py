# book/views.py
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
import requests

from .models import Book
from .serializers import BookSerializer

# Setup logger
logger = logging.getLogger(__name__)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def validate_product(self, product_id):
        """Kiểm tra product tồn tại và có type là BOOK"""
        try:
            response = requests.get(
                f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}/"
            )
            logger.info(f"Product validation response: {response.status_code}")
            logger.info(f"Product validation data: {response.json()}")

            if response.status_code != 200:
                return False, "Product không tồn tại"

            product_data = response.json()
            if product_data.get('product_type') != 'BOOK':
                return False, "Product không phải là sách"

            return True, None
        except requests.RequestException as e:
            logger.error(f"Error validating product: {str(e)}")
            return False, "Lỗi kết nối tới Product Service"

    def create(self, request, *args, **kwargs):
        """Tạo thông tin chi tiết cho sách với product_id đã có"""
        logger.info(f"Creating book with data: {request.data}")

        if 'product_id' not in request.data:
            logger.error("Missing product_id in request data")
            return Response(
                {"error": "product_id là bắt buộc"},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_valid, error = self.validate_product(request.data['product_id'])
        if not is_valid:
            logger.error(f"Product validation failed: {error}")
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            instance = serializer.save()
            logger.info(f"Book created successfully with id: {instance.product_id}")
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            error_msg = str(e) if str(e) else "Unknown error occurred while saving book"
            logger.exception(f"Error saving book: {error_msg}")
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )