# CHAPTER 2: DESIGN E-COMMERCE SYSTEM WITH MICROSERVICES AND DJANGO

## 2.1 Design services/components

Thiết kế kiến trúc microservices cho hệ thống thương mại điện tử đòi hỏi việc phân chia rõ ràng các dịch vụ, xác định ranh giới, và thiết lập cách thức giao tiếp giữa chúng. Dựa trên phân tích yêu cầu ở Chương 1, chúng tôi thiết kế các services và components sau đây.

### 2.1.1 Tổng quan kiến trúc

Hệ thống thương mại điện tử của chúng tôi sử dụng kiến trúc microservices với Django và Django REST Framework làm nền tảng chính, kết hợp với một số dịch vụ đặc biệt sử dụng Flask cho các tính năng machine learning. Kiến trúc tổng thể bao gồm 3 tầng chính:

1. **Client Tier**: Frontend ứng dụng
2. **API Gateway**: Tầng điều hướng và bảo mật
3. **Service Tier**: Các microservices chuyên biệt

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│                │     │                │     │                │
│ Web Application├────►│   Mobile App   ├────►│ Admin Dashboard│
│                │     │                │     │                │
└───────┬────────┘     └───────┬────────┘     └───────┬────────┘
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────┐
│                         API Gateway                          │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│  │ Routing │  │  Auth   │  │ Caching │  │ Rate    │         │
│  │         │  │Validation│  │         │  │Limiting │         │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘         │
└───────┬─────────────┬─────────────┬─────────────┬───────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────────┐
│ Customer     │ │ Product  │ │ Order        │ │ Payment      │
│ Service      │ │ Service  │ │ Service      │ │ Service      │
│ (Django+MySQL)│ │(Django+  │ │ (Django+    │ │ (Django+     │
│              │ │MongoDB)  │ │ PostgreSQL)  │ │ PostgreSQL)  │
└──────┬───────┘ └────┬─────┘ └─────┬────────┘ └────┬─────────┘
       │              │            │               │
       ▼              ▼            ▼               ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────────┐
│ Review       │ │ Cart     │ │ Shipment     │ │ ML Services  │
│ Service      │ │ Service  │ │ Service      │ │ (Flask+Redis)│
│ (Django+MySQL)│ │(Django+  │ │ (Django+    │ │              │
│              │ │PostgreSQL)│ │ PostgreSQL)  │ │              │
└──────────────┘ └──────────┘ └──────────────┘ └──────────────┘
```

### 2.1.2 Chi tiết các services

#### 1. API Gateway

- **Công nghệ**: Nginx, Kong hoặc custom Django service
- **Chức năng**:
  - Định tuyến request đến các microservices phù hợp
  - Xác thực và xác minh JWT tokens
  - Rate limiting và bảo vệ DDoS
  - Request logging và monitoring
  - Caching HTTP responses
  - Tổng hợp dữ liệu từ nhiều services (API composition)
- **Các components chính**:
  - Router module
  - Authentication middleware
  - Rate limiter
  - Logging service
  - Circuit breaker implementation

#### 2. Customer Service

- **Công nghệ**: Django, Django REST Framework, MySQL
- **Chức năng**:
  - Quản lý người dùng (đăng ký, đăng nhập, profile)
  - Xác thực và phân quyền
  - Quản lý địa chỉ
  - Quản lý danh sách yêu thích
- **Các components chính**:
  - User Management API
  - Authentication API
  - Address Management API
  - Wishlist API
  - Email verification service

#### 3. Product Service

- **Công nghệ**: Django, Django REST Framework, MongoDB
- **Chức năng**:
  - Quản lý danh mục sản phẩm
  - Quản lý sản phẩm
  - Quản lý tồn kho
  - Tìm kiếm sản phẩm
- **Các components chính**:
  - Category Management API
  - Product Management API
  - Inventory Management API
  - Search API
  - Media management (hình ảnh sản phẩm)

#### 4. Book Service

- **Công nghệ**: Django, Django REST Framework, MongoDB
- **Chức năng**:
  - Quản lý thông tin sách
  - Quản lý tác giả, nhà xuất bản
  - Quản lý thể loại sách
- **Các components chính**:
  - Book Management API
  - Author Management API
  - Publisher Management API
  - Book Category API

#### 5. Shoe Service

- **Công nghệ**: Django, Django REST Framework, MongoDB
- **Chức năng**:
  - Quản lý thông tin giày
  - Quản lý thương hiệu, kiểu dáng
  - Quản lý kích cỡ và màu sắc
- **Các components chính**:
  - Shoe Management API
  - Brand Management API
  - Style Management API
  - Size & Color Management API

#### 6. Cart Service

- **Công nghệ**: Django, Django REST Framework, PostgreSQL
- **Chức năng**:
  - Quản lý giỏ hàng
  - Thêm/xóa sản phẩm
  - Áp dụng mã giảm giá
  - Tính toán giá tiền
- **Các components chính**:
  - Cart Management API
  - Cart Item Management API
  - Discount Application API
  - Price Calculation Service

#### 7. Order Service

- **Công nghệ**: Django, Django REST Framework, PostgreSQL
- **Chức năng**:
  - Tạo và quản lý đơn hàng
  - Xử lý quy trình đặt hàng
  - Quản lý trạng thái đơn hàng
  - Xử lý hoàn trả/đổi hàng
- **Các components chính**:
  - Order Management API
  - Order Status Management API
  - Return/Exchange Management API
  - Order History API

#### 8. Payment Service

- **Công nghệ**: Django, Django REST Framework, PostgreSQL
- **Chức năng**:
  - Tích hợp với các cổng thanh toán (VNPay, Momo, PayPal)
  - Xử lý giao dịch thanh toán
  - Quản lý hoàn tiền
  - Lưu trữ phương thức thanh toán
- **Các components chính**:
  - Payment Processing API
  - Payment Gateway Integration
  - Refund Management API
  - Payment Method Management API

#### 9. Shipment Service

- **Công nghệ**: Django, Django REST Framework, PostgreSQL
- **Chức năng**:
  - Tích hợp với đối tác vận chuyển
  - Tạo và quản lý vận đơn
  - Theo dõi trạng thái giao hàng
  - Tính phí vận chuyển
- **Các components chính**:
  - Shipping Provider Integration
  - Shipment Tracking API
  - Shipping Rate Calculation
  - Delivery Status Management API

#### 10. Review Service

- **Công nghệ**: Django, Django REST Framework, MySQL
- **Chức năng**:
  - Quản lý đánh giá sản phẩm
  - Xếp hạng sản phẩm
  - Duyệt đánh giá
  - Quản lý bình luận
- **Các components chính**:
  - Review Management API
  - Rating Management API
  - Comment Management API
  - Review Moderation API

#### 11. Sentiment Service

- **Công nghệ**: Flask, scikit-learn, TensorFlow, Redis
- **Chức năng**:
  - Phân tích cảm xúc từ đánh giá
  - Trích xuất từ khóa
  - Phân loại đánh giá
  - Tổng hợp báo cáo cảm xúc
- **Các components chính**:
  - Sentiment Analysis API
  - Keyword Extraction Service
  - Review Classification Service
  - Sentiment Report Generator

#### 12. Recommendation Service

- **Công nghệ**: Flask, scikit-learn, TensorFlow, Redis
- **Chức năng**:
  - Đề xuất sản phẩm cá nhân hóa
  - Phân tích hành vi người dùng
  - Xác định sản phẩm tương tự
  - Hiển thị xu hướng mua sắm
- **Các components chính**:
  - Recommendation API
  - User Behavior Analysis
  - Similar Products Service
  - Trending Products Service

### 2.1.3 Giao tiếp giữa các services

Các microservices giao tiếp với nhau thông qua các cơ chế sau:

1. **RESTful APIs**: Cho các giao tiếp đồng bộ giữa các services
   ```
   Service A --HTTP Request--> Service B --HTTP Response--> Service A
   ```

2. **Message Queue**: Cho các giao tiếp không đồng bộ (sử dụng RabbitMQ/Kafka)
   ```
   Service A --Publish Event--> Message Queue --Consume Event--> Service B
   ```

3. **Event Sourcing**: Cho việc duy trì tính nhất quán dữ liệu giữa các services
   ```
   Service A --Emit Event--> Event Store --Subscribe--> Service B, Service C
   ```

4. **API Composition**: Khi cần tổng hợp dữ liệu từ nhiều services
   ```
   Client --Request--> API Gateway --Parallel Requests--> Service A, Service B, Service C
   ```

### 2.1.4 Luồng xử lý dữ liệu

#### Luồng xử lý đặt hàng

```
Frontend -> API Gateway -> Cart Service (lấy thông tin giỏ hàng)
                        -> Customer Service (xác thực người dùng, lấy địa chỉ)
                        -> Order Service (tạo đơn hàng) 
                        -> Payment Service (xử lý thanh toán)
                        -> Shipment Service (tạo vận đơn)
                        -> Notification Service (gửi email xác nhận)
```

#### Luồng xử lý đề xuất sản phẩm

```
Frontend -> API Gateway -> Recommendation Service (yêu cầu gợi ý)
                        -> Product Service (lấy thông tin sản phẩm)
                        -> Customer Service (lấy lịch sử mua hàng)
                        -> Review Service (lấy đánh giá)
```

### 2.1.5 Database Schema

Mỗi microservice sẽ có database riêng để đảm bảo tính độc lập. Việc chọn loại database phụ thuộc vào đặc điểm dữ liệu:

- **Relational DB (MySQL/PostgreSQL)**: Dùng cho dữ liệu cần tính nhất quán cao (Customer, Order, Payment)
- **Document DB (MongoDB)**: Dùng cho dữ liệu có cấu trúc linh hoạt (Product, Book, Shoe)
- **In-memory DB (Redis)**: Dùng cho cache và dữ liệu tạm thời (Cart, Session)

### 2.1.6 Deployment Architecture

Hệ thống được triển khai sử dụng Docker và Docker Compose:

```yaml
# Trích đoạn từ docker-compose.yml
services:
  api-gateway:
    build: ./api-gateway
    ports:
      - "80:80"
    depends_on:
      - customer-service
      - product-service
      - order-service
      
  customer-service:
    build: ./customer-service
    ports:
      - "8001:8000"
    environment:
      - DB_HOST=db-mysql
    depends_on:
      - db-mysql
      
  product-service:
    build: ./product-service
    ports:
      - "8002:8000"
    environment:
      - DB_HOST=db-mongo
    depends_on:
      - db-mongo
      
  # Các services khác...
  
  db-mysql:
    image: mysql:8.0
    volumes:
      - mysql-data:/var/lib/mysql
      
  db-mongo:
    image: mongo:5.0
    volumes:
      - mongo-data:/data/db
```

### 2.1.7 Monitoring và Logging

Hệ thống sử dụng các công cụ sau để giám sát và ghi log:

- **Prometheus**: Thu thập metrics từ các services
- **Grafana**: Visualize metrics và tạo dashboards
- **ELK Stack**: Tập trung logs từ các services
- **Jaeger/Zipkin**: Distributed tracing để theo dõi requests

### 2.1.8 Security Architecture

- **Authentication**: JWT (JSON Web Tokens) cho xác thực người dùng
- **Authorization**: RBAC (Role-Based Access Control) cho phân quyền
- **Data Protection**: HTTPS/TLS cho bảo mật dữ liệu truyền tải
- **API Security**: CORS, rate limiting, input validation
- **Database Security**: Mã hóa dữ liệu nhạy cảm, access control 

## 2.2 Design classes and methods in component

Phần này sẽ tập trung vào thiết kế chi tiết các classes và methods chính trong mỗi microservice. Trong kiến trúc Django, các class chính bao gồm Models (định nghĩa cấu trúc dữ liệu), Serializers (chuyển đổi dữ liệu), Views/ViewSets (xử lý request) và URLs (định tuyến).

### 2.2.1 Customer Service

#### Models

```python
# customer_service/users/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        SELLER = "seller", "Người bán"
        CUSTOMER = "customer", "Người mua"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
    is_verified = models.BooleanField(default=False)
    is_seller_request = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Serializers

```python
# customer_service/users/serializers.py
from rest_framework import serializers
from .models import User, Address

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'is_verified', 'first_name', 'last_name']
        read_only_fields = ['id', 'is_verified', 'role']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'full_name', 'phone', 'street', 'city', 'state', 'country', 'postal_code', 'is_default']
        read_only_fields = ['id']
```

#### Views

```python
# customer_service/users/views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from .models import User, Address
from .serializers import UserSerializer, AddressSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            return []
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
        
class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Gửi email xác nhận
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

#### URLs

```python
# customer_service/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterAPI, AddressViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view(), name='register'),
]
```

### 2.2.2 Product Service

#### Models

```python
# product_service/products/models.py
import uuid
from django.db import models

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    image = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    inventory_count = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    images = models.JSONField(default=list)
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
```

#### Serializers

```python
# product_service/products/serializers.py
from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'category', 'category_name', 
                 'base_price', 'sale_price', 'inventory_count', 'is_available', 
                 'images', 'tags', 'created_at']
```

#### Views

```python
# product_service/products/views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUser()]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['base_price', 'created_at', 'inventory_count']
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUser()]
    
    @action(detail=True, methods=['patch'])
    def update_inventory(self, request, slug=None):
        product = self.get_object()
        try:
            quantity = int(request.data.get('quantity', 0))
            product.inventory_count = max(0, product.inventory_count + quantity)
            product.save()
            return Response({'status': 'inventory updated'})
        except ValueError:
            return Response({'error': 'Invalid quantity'}, status=400)
```

### 2.2.3 Order Service

#### Models

```python
# order_service/orders/models.py
import uuid
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending_payment', 'Chờ thanh toán'),
        ('processing', 'Đang xử lý'),
        ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
        ('refunded', 'Đã hoàn tiền')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    shipping_address = models.JSONField()
    payment_method = models.CharField(max_length=50)
    shipping_method = models.CharField(max_length=50)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.UUIDField()
    product_name = models.CharField(max_length=255)
    product_image = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Serializers

```python
# order_service/orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'product_image', 'quantity', 'unit_price']
        read_only_fields = ['id']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'total_price', 'status', 'shipping_address', 
                 'payment_method', 'shipping_method', 'shipping_cost', 'notes',
                 'tracking_number', 'items', 'created_at']
        read_only_fields = ['id', 'created_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['user_id', 'shipping_address', 'payment_method', 'shipping_method', 
                 'shipping_cost', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # Tính tổng tiền
        total_price = sum(item['unit_price'] * item['quantity'] for item in items_data)
        total_price += validated_data.get('shipping_cost', 0)
        # Tạo order
        order = Order.objects.create(total_price=total_price, **validated_data)
        # Tạo order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
```

#### Views

```python
# order_service/orders/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return self.queryset.filter(user_id=user_id)
        return self.queryset
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        status = request.data.get('status')
        if status and status in dict(Order.STATUS_CHOICES).keys():
            order.status = status
            order.save()
            return Response({'status': 'Order status updated'})
        return Response({'error': 'Invalid status'}, status=400)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status in ['pending_payment', 'processing']:
            order.status = 'cancelled'
            order.save()
            # Trigger event to update inventory
            return Response({'status': 'Order cancelled'})
        return Response({'error': 'Cannot cancel order in current status'}, status=400)
```

## 2.3 Design API

Phần này mô tả các API endpoint chính của hệ thống e-commerce microservices, tập trung vào việc thiết kế RESTful API với Django REST Framework.

### 2.3.1 API Gateway Routes

API Gateway đóng vai trò là điểm vào duy nhất cho tất cả các API requests. Dưới đây là các routes chính:

```
# Authentication & User Management
/api/auth/register                   -> Customer Service
/api/auth/login                      -> Customer Service
/api/auth/refresh-token              -> Customer Service
/api/users/profile                   -> Customer Service
/api/users/addresses                 -> Customer Service

# Products
/api/products                        -> Product Service
/api/products/{slug}                 -> Product Service
/api/products/search                 -> Product Service
/api/categories                      -> Product Service

# Books
/api/books                          -> Book Service
/api/books/{slug}                   -> Book Service
/api/books/authors                  -> Book Service
/api/books/publishers               -> Book Service

# Shoes
/api/shoes                          -> Shoe Service
/api/shoes/{slug}                   -> Shoe Service
/api/shoes/brands                   -> Shoe Service
/api/shoes/sizes                    -> Shoe Service

# Cart
/api/cart                           -> Cart Service
/api/cart/items                     -> Cart Service
/api/cart/checkout                  -> Cart Service

# Orders
/api/orders                         -> Order Service
/api/orders/{id}                    -> Order Service
/api/orders/{id}/status             -> Order Service
/api/orders/{id}/cancel             -> Order Service

# Payments
/api/payments/methods               -> Payment Service
/api/payments/process               -> Payment Service
/api/payments/{id}/status           -> Payment Service

# Shipping
/api/shipping/methods               -> Shipment Service
/api/shipping/calculate             -> Shipment Service
/api/shipping/track/{id}            -> Shipment Service

# Reviews
/api/reviews/product/{product_id}   -> Review Service
/api/reviews/user/{user_id}         -> Review Service
/api/reviews/{id}/vote              -> Review Service

# Recommendations
/api/recommendations/user/{user_id} -> Recommendation Service
/api/recommendations/similar/{product_id} -> Recommendation Service
/api/recommendations/trending       -> Recommendation Service
```

### 2.3.2 API Documentation

Dưới đây là mô tả chi tiết một số API endpoint quan trọng:

#### Customer Service APIs

```
# GET /api/users/profile
Mô tả: Lấy thông tin profile của người dùng đã đăng nhập
Headers: Authorization: Bearer {token}
Response: 200 OK
{
  "id": "uuid",
  "username": "example_user",
  "email": "user@example.com",
  "phone": "0123456789",
  "role": "customer",
  "first_name": "Example",
  "last_name": "User",
  "is_verified": true
}

# POST /api/auth/register
Mô tả: Đăng ký tài khoản mới
Request:
{
  "username": "new_user",
  "email": "newuser@example.com",
  "password": "securepassword",
  "phone": "0123456789",
  "first_name": "New",
  "last_name": "User"
}
Response: 201 Created
{
  "id": "uuid",
  "username": "new_user",
  "email": "newuser@example.com",
  "phone": "0123456789",
  "role": "customer",
  "is_verified": false
}

# POST /api/auth/login
Mô tả: Đăng nhập và lấy token
Request:
{
  "username": "example_user",
  "password": "securepassword"
}
Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI...",
  "refresh_token": "eyJhbGciOiJIUzI...",
  "user": {
    "id": "uuid",
    "username": "example_user",
    "email": "user@example.com",
    "role": "customer"
  }
}
```

#### Product Service APIs

```
# GET /api/products
Mô tả: Lấy danh sách sản phẩm với phân trang
Parameters:
  - page: Số trang (mặc định: 1)
  - limit: Số sản phẩm mỗi trang (mặc định: 10)
  - category: ID danh mục để lọc
  - search: Từ khóa tìm kiếm
  - sort: Trường để sắp xếp (created_at, price)
  - order: Thứ tự sắp xếp (asc, desc)
Response: 200 OK
{
  "results": [
    {
      "id": "uuid",
      "name": "Product Name",
      "slug": "product-name",
      "description": "Product description...",
      "category": "uuid",
      "category_name": "Category Name",
      "base_price": 100.00,
      "sale_price": 85.00,
      "inventory_count": 50,
      "is_available": true,
      "images": ["url1", "url2"],
      "tags": ["tag1", "tag2"],
      "created_at": "2023-05-20T14:30:00Z"
    },
    // ...
  ],
  "count": 100,
  "page": 1,
  "total_pages": 10
}

# GET /api/products/{slug}
Mô tả: Lấy chi tiết một sản phẩm theo slug
Response: 200 OK
{
  "id": "uuid",
  "name": "Product Name",
  "slug": "product-name",
  "description": "Detailed product description...",
  "category": "uuid",
  "category_name": "Category Name",
  "base_price": 100.00,
  "sale_price": 85.00,
  "inventory_count": 50,
  "is_available": true,
  "images": ["url1", "url2", "url3"],
  "tags": ["tag1", "tag2", "tag3"],
  "created_at": "2023-05-20T14:30:00Z",
  "attributes": {
    // Additional product attributes
  }
}
```

#### Cart Service APIs

```
# GET /api/cart
Mô tả: Lấy thông tin giỏ hàng hiện tại
Headers: Authorization: Bearer {token}
Response: 200 OK
{
  "id": "uuid",
  "user_id": "uuid",
  "items": [
    {
      "id": "uuid",
      "product_id": "uuid",
      "product_name": "Product Name",
      "product_image": "image_url",
      "quantity": 2,
      "unit_price": 85.00
    },
    // ...
  ],
  "total_items": 3,
  "total_price": 170.00,
  "created_at": "2023-05-21T09:15:00Z",
  "updated_at": "2023-05-21T10:20:00Z"
}

# POST /api/cart/items
Mô tả: Thêm sản phẩm vào giỏ hàng
Headers: Authorization: Bearer {token}
Request:
{
  "product_id": "uuid",
  "quantity": 1
}
Response: 201 Created
{
  "id": "uuid",
  "product_id": "uuid",
  "product_name": "Product Name",
  "product_image": "image_url",
  "quantity": 1,
  "unit_price": 85.00
}
```

#### Order Service APIs

```
# POST /api/orders
Mô tả: Tạo đơn hàng mới
Headers: Authorization: Bearer {token}
Request:
{
  "user_id": "uuid",
  "shipping_address": {
    "full_name": "Example User",
    "phone": "0123456789",
    "street": "123 Example St",
    "city": "Example City",
    "state": "Example State",
    "country": "Example Country",
    "postal_code": "12345"
  },
  "payment_method": "vnpay",
  "shipping_method": "standard",
  "shipping_cost": 10.00,
  "notes": "Please deliver in the morning",
  "items": [
    {
      "product_id": "uuid",
      "product_name": "Product Name",
      "product_image": "image_url",
      "quantity": 2,
      "unit_price": 85.00
    },
    // ...
  ]
}
Response: 201 Created
{
  "id": "uuid",
  "status": "pending_payment",
  "total_price": 180.00,  // including shipping cost
  "tracking_number": "",
  "created_at": "2023-05-21T11:30:00Z"
}

# GET /api/orders/{id}
Mô tả: Lấy chi tiết đơn hàng
Headers: Authorization: Bearer {token}
Response: 200 OK
{
  "id": "uuid",
  "user_id": "uuid",
  "total_price": 180.00,
  "status": "processing",
  "shipping_address": {
    // Address details
  },
  "payment_method": "vnpay",
  "shipping_method": "standard",
  "shipping_cost": 10.00,
  "notes": "Please deliver in the morning",
  "tracking_number": "ABC123",
  "items": [
    {
      "id": "uuid",
      "product_id": "uuid",
      "product_name": "Product Name",
      "product_image": "image_url",
      "quantity": 2,
      "unit_price": 85.00
    },
    // ...
  ],
  "created_at": "2023-05-21T11:30:00Z",
  "updated_at": "2023-05-21T11:45:00Z"
}
```

### 2.3.3 API Authentication Flow

Flow xác thực người dùng:

1. **Đăng ký tài khoản**:
   - Client gửi thông tin đăng ký đến `/api/auth/register`
   - Service tạo tài khoản và gửi email xác nhận
   - Trả về thông tin người dùng đã tạo

2. **Đăng nhập**:
   - Client gửi thông tin đăng nhập đến `/api/auth/login`
   - Service xác thực và phát hành JWT tokens (access token và refresh token)
   - Trả về tokens và thông tin người dùng cơ bản

3. **Xác thực request**:
   - Client đính kèm access token trong header: `Authorization: Bearer {token}`
   - API Gateway xác thực token trước khi chuyển tiếp request đến service tương ứng
   - Nếu token hết hạn, client sử dụng refresh token để lấy token mới thông qua `/api/auth/refresh-token`

### 2.3.4 API Versioning

API sử dụng versioning qua URL prefix để đảm bảo khả năng tương thích:

```
/api/v1/products
/api/v1/users
...
```

Điều này cho phép chúng ta phát triển và triển khai phiên bản API mới mà không ảnh hưởng đến các clients hiện có.

### 2.3.5 API Standards

Tất cả API tuân thủ các tiêu chuẩn sau:

1. **RESTful Design**:
   - Sử dụng HTTP methods (GET, POST, PUT, PATCH, DELETE) đúng cách
   - Sử dụng URL endpoints dễ hiểu và mô tả rõ tài nguyên
   - Sử dụng status codes HTTP chuẩn

2. **Response Format**:
   - Tất cả responses đều trả về dạng JSON
   - Các successful responses có cấu trúc nhất quán
   - Error responses bao gồm status code, error message, và error details

3. **Pagination**:
   - List endpoints hỗ trợ phân trang qua query parameters `page` và `limit`
   - Responses bao gồm metadata: tổng số items, số trang, trang hiện tại

4. **Filtering, Sorting and Searching**:
   - Filtering: `?field=value`
   - Sorting: `?sort=field&order=asc|desc`
   - Searching: `?search=keyword`

### 2.3.6 Inter-Service Communication

Giao tiếp giữa các services được thực hiện qua hai cơ chế:

1. **Synchronous (HTTP)** - Cho các yêu cầu thời gian thực:
   ```python
   # Example in Cart Service
   def get_product_details(product_id):
       response = requests.get(f"{PRODUCT_SERVICE_URL}/api/v1/products/{product_id}/")
       if response.status_code == 200:
           return response.json()
       return None
   ```

2. **Asynchronous (Message Queue)** - Cho các sự kiện và xử lý nền:
   ```python
   # Example in Order Service
   def order_created(order):
       message = {
           'event': 'order_created',
           'data': {
               'order_id': str(order.id),
               'user_id': str(order.user_id),
               'items': [{'product_id': str(item.product_id), 'quantity': item.quantity} 
                         for item in order.items.all()]
           }
       }
       # Publish message to RabbitMQ/Kafka
       publish_message('order_events', message)
   ```

## 2.4 Conclusion

Trong chương này, chúng tôi đã trình bày thiết kế chi tiết của hệ thống thương mại điện tử sử dụng kiến trúc microservices với Django. Các điểm chính đã đạt được bao gồm:

### 2.4.1 Những đặc điểm nổi bật trong thiết kế

1. **Kiến trúc phân tách theo domain**: Mỗi microservice đảm nhận một phạm vi chức năng riêng biệt, giúp dễ dàng phát triển, triển khai và bảo trì.

2. **Database independence**: Mỗi service quản lý database riêng, với việc lựa chọn công nghệ cơ sở dữ liệu phù hợp với đặc thù dữ liệu của service (SQL, NoSQL, in-memory).

3. **API-first design**: Giao diện giao tiếp rõ ràng thông qua RESTful APIs, đảm bảo tính nhất quán và dễ sử dụng.

4. **Authentication & Authorization**: Hệ thống xác thực tập trung sử dụng JWT, đảm bảo tính bảo mật và dễ dàng mở rộng.

5. **Scalability & Resilience**: Các services có thể được scale độc lập, tăng khả năng chịu tải và khả năng phục hồi của hệ thống.

### 2.4.2 Lợi ích của thiết kế

1. **Tính linh hoạt cao**: Dễ dàng thêm mới hoặc cập nhật các tính năng mà không ảnh hưởng đến toàn bộ hệ thống.

2. **Khả năng mở rộng tốt**: Có thể scale từng service riêng biệt dựa trên nhu cầu thực tế.

3. **Đa dạng công nghệ**: Có thể lựa chọn công nghệ phù hợp nhất cho từng service (ví dụ: MongoDB cho sản phẩm, PostgreSQL cho đơn hàng).

4. **Phát triển song song**: Các team khác nhau có thể phát triển các services độc lập.

5. **Fault isolation**: Sự cố ở một service không ảnh hưởng đến toàn bộ hệ thống.

### 2.4.3 Thách thức và giải pháp

1. **Data consistency**: Sử dụng Saga pattern và event sourcing để đảm bảo tính nhất quán dữ liệu giữa các services.

2. **Distributed transactions**: Áp dụng eventual consistency kết hợp với compensation transactions khi cần.

3. **Service discovery**: Sử dụng API Gateway và service registry để quản lý các endpoints.

4. **Monitoring complexity**: Triển khai hệ thống giám sát tập trung với Prometheus, Grafana và ELK Stack.

5. **Testing challenges**: Xây dựng chiến lược testing bao gồm unit tests, service-level tests và end-to-end tests.

### 2.4.4 Hướng phát triển tiếp theo

Thiết kế microservices cho hệ thống thương mại điện tử này cung cấp nền tảng vững chắc cho việc phát triển các tính năng nâng cao trong tương lai:

1. **Personalization**: Mở rộng Recommendation Service với các thuật toán ML phức tạp hơn.

2. **Advanced analytics**: Xây dựng data warehouse để phân tích dữ liệu và hỗ trợ ra quyết định kinh doanh.

3. **Multi-tenant support**: Cho phép nhiều người bán hoặc thương hiệu hoạt động trên cùng một nền tảng.

4. **International expansion**: Bổ sung hỗ trợ đa ngôn ngữ, đa tiền tệ và tuân thủ quy định khu vực.

5. **IoT integration**: Kết nối với các thiết bị thông minh để nâng cao trải nghiệm mua sắm.

Tóm lại, thiết kế microservices cho hệ thống thương mại điện tử với Django cung cấp một giải pháp linh hoạt, có khả năng mở rộng và dễ bảo trì. Mặc dù có một số thách thức về mặt phức tạp trong triển khai và quản lý, những lợi ích mà nó mang lại là đáng kể và phù hợp với xu hướng phát triển hiện đại của các hệ thống thương mại điện tử quy mô lớn.