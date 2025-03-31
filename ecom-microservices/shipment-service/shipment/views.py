import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from .models import Shipment, ShipmentItem, ShippingHistory
from .serializers import (
    ShipmentSerializer,
    ShipmentCreateSerializer,
    ShipmentUpdateSerializer,
    ShipmentItemSerializer
)

ORDER_SERVICE_URL = "http://order-service:8007/orders"

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ShipmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ShipmentUpdateSerializer
        return ShipmentSerializer

    def create(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response(
                {'error': 'order_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate required fields from request
        required_fields = ['carrier', 'weight', 'shipping_cost', 'shipment_fee']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            return Response(
                {'error': f'Missing required fields: {", ".join(missing_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch order details
            response = requests.get(
                f"{ORDER_SERVICE_URL}/{order_id}",
                timeout=5
            )
            if response.status_code != 200:
                return Response(
                    {'error': 'Failed to fetch order details'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            order_data = response.json()

            # Map data from order and request to shipment
            shipment_data = {
                'order_id': order_id,
                'carrier': request.data['carrier'],
                'weight': request.data['weight'],
                'shipping_cost': request.data['shipping_cost'],
                'shipment_fee': request.data['shipment_fee'],

                # Map receiver info from order
                'receiver_name': order_data['customer_name'],
                'receiver_phone': order_data['contact_phone'],
                'shipping_address_line1': order_data['shipping_address_line1'],
                'shipping_ward': order_data['shipping_ward'],
                'shipping_district': order_data['shipping_district'],
                'shipping_city': order_data['shipping_city'],
                'shipping_country': order_data['shipping_country'],

                # Optional fields
                'dimension': request.data.get('dimension'),
                'estimated_delivery': request.data.get('estimated_delivery'),
                'shipping_notes': request.data.get('shipping_notes'),
                'tracking_number': request.data.get('tracking_number')
            }

            serializer = self.get_serializer(data=shipment_data)
            serializer.is_valid(raise_exception=True)

            with transaction.atomic():
                # Create shipment
                shipment = serializer.save(status='pending')

                # Create shipment items from order items
                shipment_items = [
                    ShipmentItem(
                        shipment=shipment,
                        order_item_id=item['id'],
                        product_id=item['product_id'],
                        product_name=item['product_name'],
                        quantity=item['quantity'],
                        price=item['price']
                    ) for item in order_data['items']
                ]
                ShipmentItem.objects.bulk_create(shipment_items)

                # Create shipping history with user_id from order
                ShippingHistory.objects.create(
                    shipment=shipment,
                    status='pending',
                    notes='Shipment created',
                    created_by=order_data['user_id']
                )

                return Response(
                    ShipmentSerializer(shipment).data,
                    status=status.HTTP_201_CREATED
                )

        except requests.RequestException as e:
            return Response(
                {'error': f'Failed to fetch order details: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['PUT'])
    def update_status(self, request, pk=None):
        shipment = self.get_object()
        new_status = request.data.get('status')
        notes = request.data.get('notes')

        if not new_status:
            return Response(
                {'error': 'Status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in dict(Shipment.SHIPPING_STATUS):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            shipment.update_status(new_status, notes)
            return Response(ShipmentSerializer(shipment).data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['PUT'])
    def mark_delivered(self, request, pk=None):
        shipment = self.get_object()

        if shipment.status == 'delivered':
            return Response(
                {'error': 'Shipment already delivered'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            shipment.update_status('delivered', 'Package delivered successfully')
            shipment.delivered_at = timezone.now()
            shipment.save()
            return Response(ShipmentSerializer(shipment).data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['PUT'])
    def mark_failed(self, request, pk=None):
        shipment = self.get_object()
        failure_reason = request.data.get('failure_reason')

        if not failure_reason:
            return Response(
                {'error': 'Failure reason is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            shipment.update_status('failed', f'Delivery failed: {failure_reason}')
            shipment.failure_reason = failure_reason
            shipment.save()
            return Response(ShipmentSerializer(shipment).data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['GET'])
    def by_order(self, request):
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response(
                {'error': 'order_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        shipments = Shipment.objects.filter(order_id=order_id)
        return Response(ShipmentSerializer(shipments, many=True).data)

    @action(detail=False, methods=['GET'])
    def by_tracking(self, request):
        tracking_number = request.query_params.get('tracking_number')
        if not tracking_number:
            return Response(
                {'error': 'tracking_number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
            return Response(ShipmentSerializer(shipment).data)
        except Shipment.DoesNotExist:
            return Response(
                {'error': 'Shipment not found'},
                status=status.HTTP_404_NOT_FOUND
            )