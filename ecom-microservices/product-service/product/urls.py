from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

# Tạo router cho ViewSet
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]