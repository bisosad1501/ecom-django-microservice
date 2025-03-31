from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Shoe
from .serializers import ShoeSerializer

class ShoeViewSet(viewsets.ModelViewSet):
    """API CRUD giày"""
    queryset = Shoe.objects.all()
    serializer_class = ShoeSerializer

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')  # Lấy product_id từ URL
        shoe = get_object_or_404(Shoe, product_id=product_id)
        serializer = ShoeSerializer(shoe)
        return Response(serializer.data, status=status.HTTP_200_OK)