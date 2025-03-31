from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShipmentViewSet

router = DefaultRouter()
router.register(r'shipments', ShipmentViewSet, basename='shipment')

urlpatterns = [
    path('', include(router.urls)),
]

"""
API Endpoints:
    GET /shipments/ - List all shipments
    POST /shipments/ - Create new shipment
    GET /shipments/{id}/ - Get shipment detail
    PUT /shipments/{id}/ - Update shipment
    DELETE /shipments/{id}/ - Delete shipment
    PUT /shipments/{id}/update-status/ - Update status
    PUT /shipments/{id}/mark-delivered/ - Mark as delivered
    PUT /shipments/{id}/mark-failed/ - Mark as failed
    GET /shipments/by-order/ - Get by order ID
    GET /shipments/by-tracking/ - Get by tracking number
"""