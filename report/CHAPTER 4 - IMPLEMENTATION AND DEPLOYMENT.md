# CHAPTER 4: IMPLEMENTATION AND DEPLOYMENT

Chương này trình bày chi tiết về quá trình triển khai thực tế hệ thống thương mại điện tử sử dụng kiến trúc microservices với Django, tập trung vào các khía cạnh kỹ thuật như môi trường phát triển, cài đặt cơ sở dữ liệu, triển khai và kiểm thử.

## 4.1 Development Environment

Môi trường phát triển được thiết lập với mục tiêu hỗ trợ phát triển microservices hiệu quả, bảo đảm tính nhất quán giữa các môi trường và tối ưu hóa quy trình làm việc của nhóm phát triển.

### 4.1.1 Development Tools

#### 4.1.1.1 Integrated Development Environment (IDE)

Chúng tôi sử dụng PyCharm Professional làm IDE chính cho phát triển Django microservices, với các tính năng nổi bật:

- Hỗ trợ tối ưu cho Python và Django
- Tích hợp với Docker và Kubernetes
- Hỗ trợ REST Client cho việc kiểm thử API
- Tích hợp với Git và các công cụ CI/CD

Cấu hình PyCharm cho dự án:

```python
# .idea/runConfigurations/customer_service.xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="customer_service" type="Python.DjangoServer" factoryName="Django server">
    <module name="ecom-microservices" />
    <option name="INTERPRETER_OPTIONS" value="" />
    <option name="PARENT_ENVS" value="true" />
    <envs>
      <env name="PYTHONUNBUFFERED" value="1" />
      <env name="DJANGO_SETTINGS_MODULE" value="customer_service.settings" />
      <env name="DATABASE_URL" value="mysql://root:password@localhost:3306/customer_db" />
    </envs>
    <option name="SDK_HOME" value="$PROJECT_DIR$/venv/bin/python" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$/customer-service" />
    <option name="IS_MODULE_SDK" value="false" />
    <option name="ADD_CONTENT_ROOTS" value="true" />
    <option name="ADD_SOURCE_ROOTS" value="true" />
    <option name="launchJavascriptDebuger" value="false" />
    <option name="port" value="8001" />
    <option name="host" value="localhost" />
    <option name="additionalOptions" value="" />
    <option name="browserUrl" value="http://localhost:8001/" />
    <option name="runTestServer" value="false" />
    <option name="runNoReload" value="false" />
    <option name="useCustomRunCommand" value="false" />
    <option name="customRunCommand" value="" />
    <method v="2" />
  </configuration>
</component>
```

#### 4.1.1.2 Version Control

Sử dụng Git với GitHub để quản lý mã nguồn:

```bash
# Cấu trúc repository
.
├── .github/
│   └── workflows/         # CI/CD configurations
├── api-gateway/           # API Gateway service
├── customer-service/      # Customer management service
├── product-service/       # Product management service
├── order-service/         # Order management service
├── payment-service/       # Payment processing service
├── shipment-service/      # Shipping management service
├── recommendation-service/ # Product recommendation service
├── sentiment-service/     # Sentiment analysis service
├── notification-service/  # Notifications service
├── frontend/              # React frontend
├── docker-compose.yml     # Docker Compose configuration
├── docker-compose.dev.yml # Development Compose configuration
├── docker-compose.prod.yml # Production Compose configuration
└── README.md              # Project documentation
```

Quy tắc branch management:

- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `release/*`: Release branches

```bash
# Quy trình phát triển tính năng mới
git checkout develop
git pull
git checkout -b feature/customer-registration
# ... development work ...
git add .
git commit -m "Add customer registration API"
git push -u origin feature/customer-registration
# Create Pull Request to develop
```

#### 4.1.1.3 Containerization

Sử dụng Docker và Docker Compose để chuẩn hóa môi trường phát triển:

```dockerfile
# customer-service/Dockerfile.dev
FROM python:3.9-slim

WORKDIR /app

# Cài đặt dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Cài đặt debugging tools cho development
RUN pip install ipython django-debug-toolbar

# Copy source code
COPY . .

# Run development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```yaml
# docker-compose.dev.yml (trích đoạn)
version: '3.8'

services:
  customer-service:
    build:
      context: ./customer-service
      dockerfile: Dockerfile.dev
    volumes:
      - ./customer-service:/app
    ports:
      - "8001:8000"
    environment:
      - DEBUG=True
      - DJANGO_SETTINGS_MODULE=customer_service.settings.development
      - DATABASE_URL=mysql://root:password@mysql-customer:3306/customer_db
      - SECRET_KEY=dev_secret_key
    depends_on:
      - mysql-customer

  product-service:
    build:
      context: ./product-service
      dockerfile: Dockerfile.dev
    volumes:
      - ./product-service:/app
    ports:
      - "8002:8000"
    environment:
      - DEBUG=True
      - DJANGO_SETTINGS_MODULE=product_service.settings.development
      - MONGODB_URI=mongodb://mongo-product:27017/product_db
      - SECRET_KEY=dev_secret_key
    depends_on:
      - mongo-product

  # ... Các service khác

  mysql-customer:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=customer_db
    volumes:
      - mysql-customer-data:/var/lib/mysql
    ports:
      - "3306:3306"

  mongo-product:
    image: mongo:5.0
    volumes:
      - mongo-product-data:/data/db
    ports:
      - "27017:27017"

volumes:
  mysql-customer-data:
  mongo-product-data:
  # ... Các volume khác
```

### 4.1.2 Development Workflow

#### 4.1.2.1 Local Development Setup

Quy trình thiết lập môi trường phát triển cục bộ:

```bash
# Clone repository
git clone https://github.com/company/ecom-microservices.git
cd ecom-microservices

# Tạo virtual environment (optional, if not using Docker)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Khởi động các services
docker-compose -f docker-compose.dev.yml up -d

# Truy cập service cụ thể
docker-compose -f docker-compose.dev.yml exec customer-service bash

# Chạy migrations
python manage.py migrate

# Tạo superuser
python manage.py createsuperuser
```

#### 4.1.2.2 Code Quality Tools

Công cụ đảm bảo chất lượng mã:

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-json

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-django]

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
        language_version: python3.9
```

```python
# setup.cfg
[flake8]
max-line-length = 100
exclude = .git,__pycache__,migrations,venv

[isort]
profile = black
multi_line_output = 3

[tool:pytest]
DJANGO_SETTINGS_MODULE = customer_service.settings.test
python_files = test_*.py
```

#### 4.1.2.3 Documentation

Quy trình tạo tài liệu API sử dụng drf-spectacular:

```python
# customer-service/customer_service/settings/base.py
INSTALLED_APPS = [
    # ... other apps
    'drf_spectacular',
]

REST_FRAMEWORK = {
    # ... other settings
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Customer Service API',
    'DESCRIPTION': 'API documentation for Customer Service',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

```python
# customer-service/customer_service/urls.py
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # ... other urls
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

### 4.1.3 Testing Environment

#### 4.1.3.1 Unit Testing

Cấu trúc unit tests cho Django microservices:

```python
# customer-service/users/tests/test_models.py
from django.test import TestCase
from users.models import User, Address

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.get_full_name(), 'Test User')
        
    def test_user_str_method(self):
        self.assertEqual(str(self.user), 'test@example.com')
```

```python
# customer-service/users/tests/test_apis.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class UserRegistrationAPITest(APITestCase):
    def test_user_registration(self):
        url = reverse('user-register')
        data = {
            'email': 'new@example.com',
            'password': 'securepassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'new@example.com')
```

#### 4.1.3.2 Integration Testing

Kiểm thử tích hợp giữa các microservices:

```python
# integration-tests/test_order_flow.py
import pytest
import requests

@pytest.fixture
def api_base_url():
    return "http://api-gateway:8000/api/v1"

@pytest.fixture
def auth_token(api_base_url):
    # Login to get token
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = requests.post(f"{api_base_url}/users/login/", json=login_data)
    return response.json()["token"]

def test_complete_order_flow(api_base_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 1. Add product to cart
    cart_data = {
        "product_id": "12345",
        "quantity": 2
    }
    cart_response = requests.post(
        f"{api_base_url}/cart/items/", 
        json=cart_data, 
        headers=headers
    )
    assert cart_response.status_code == 201
    
    # 2. Create order from cart
    order_response = requests.post(
        f"{api_base_url}/orders/", 
        headers=headers
    )
    assert order_response.status_code == 201
    order_id = order_response.json()["id"]
    
    # 3. Add shipping address
    address_data = {
        "street": "123 Test St",
        "city": "Test City",
        "state": "TS",
        "country": "Test Country",
        "zip_code": "12345"
    }
    address_response = requests.post(
        f"{api_base_url}/orders/{order_id}/shipping-address/", 
        json=address_data, 
        headers=headers
    )
    assert address_response.status_code == 200
    
    # 4. Process payment
    payment_data = {
        "payment_method": "credit_card",
        "card_number": "4111111111111111",
        "expiry_month": "12",
        "expiry_year": "2025",
        "cvv": "123"
    }
    payment_response = requests.post(
        f"{api_base_url}/orders/{order_id}/pay/", 
        json=payment_data, 
        headers=headers
    )
    assert payment_response.status_code == 200
    
    # 5. Verify order status
    order_status_response = requests.get(
        f"{api_base_url}/orders/{order_id}/", 
        headers=headers
    )
    assert order_status_response.status_code == 200
    assert order_status_response.json()["status"] == "PAID"
```

#### 4.1.3.3 Contract Testing

Sử dụng Pact để thực hiện contract testing giữa các services:

```python
# customer-service/tests/contract/test_product_service_contract.py
import atexit
import unittest
from pact import Consumer, Provider

class ProductServiceContractTest(unittest.TestCase):
    def setUp(self):
        self.pact = Consumer('CustomerService').has_pact_with(Provider('ProductService'))
        self.pact.start_service()
        atexit.register(self.pact.stop_service)

    def test_get_product_by_id(self):
        expected = {
            'id': '12345',
            'name': 'Test Product',
            'price': 19.99,
            'description': 'A test product'
        }

        (self.pact
         .given('a product with ID 12345 exists')
         .upon_receiving('a request for product 12345')
         .with_request('get', '/api/v1/products/12345/')
         .will_respond_with(200, body=expected))

        with self.pact:
            # Make the request from your customer service client
            from product_client import ProductClient
            client = ProductClient(self.pact.uri)
            product = client.get_product('12345')
            
            self.assertEqual(product['id'], '12345')
            self.assertEqual(product['name'], 'Test Product') 
```

## 4.2 Service Implementation

Phần này mô tả chi tiết việc triển khai các microservices chính trong hệ thống, bao gồm mã nguồn, cấu trúc dự án, và cách thức giao tiếp giữa các services.

### 4.2.1 API Gateway Service

API Gateway đóng vai trò điểm vào chính của hệ thống, chịu trách nhiệm định tuyến các request đến các microservices phù hợp và xử lý authentication/authorization.

#### 4.2.1.1 Cấu trúc dự án

```
api-gateway/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py        # Cấu hình ứng dụng
│   │   └── urls.py            # URL routing
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py            # JWT authentication middleware
│   │   └── rate_limiter.py    # Rate limiting middleware
│   ├── proxy/
│   │   ├── __init__.py
│   │   ├── service_registry.py # Service discovery
│   │   └── router.py          # Request routing logic
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cache.py           # Redis cache utilities
│   │   └── logging.py         # Logging configuration
│   └── app.py                 # Main application
├── Dockerfile
├── requirements.txt
└── README.md
```

#### 4.2.1.2 Cài đặt API Gateway với Kong

Chúng tôi sử dụng Kong làm API Gateway với các plugin chính:

```yaml
# kong.yml
_format_version: "2.1"

services:
  - name: customer-service
    url: http://customer-service:8000
    routes:
      - name: customer-routes
        paths:
          - /api/v1/users
          - /api/v1/auth
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 60
          policy: local

  - name: product-service
    url: http://product-service:8000
    routes:
      - name: product-routes
        paths:
          - /api/v1/products
          - /api/v1/categories
    plugins:
      - name: cors
        config:
          origins:
            - "*"
          methods:
            - GET
            - POST
            - PUT
            - DELETE
          headers:
            - Accept
            - Content-Type
            - Authorization

  - name: order-service
    url: http://order-service:8000
    routes:
      - name: order-routes
        paths:
          - /api/v1/orders
          - /api/v1/cart
    plugins:
      - name: jwt
      - name: request-transformer
        config:
          add:
            headers:
              - X-Consumer-ID:$(consumer.id)

consumers:
  - username: frontend-app
    jwt_secrets:
      - key: frontend-app-key
        secret: frontend-app-secret

  - username: mobile-app
    jwt_secrets:
      - key: mobile-app-key
        secret: mobile-app-secret
```

#### 4.2.1.3 JWT Authentication

Cài đặt middleware xác thực JWT:

```python
# api-gateway/src/middleware/auth.py
import jwt
import time
from jwt.exceptions import PyJWTError
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED

class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key, excluded_paths=None):
        super().__init__(app)
        self.secret_key = secret_key
        self.excluded_paths = excluded_paths or []

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for excluded paths
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        
        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, 
                detail="Missing or invalid Authorization header"
            )
        
        # Extract and validate token
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # Check if token is expired
            if payload.get("exp") and payload["exp"] < time.time():
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, 
                    detail="Token has expired"
                )
            
            # Add user info to request state
            request.state.user = payload
            
        except PyJWTError as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, 
                detail=f"Invalid token: {str(e)}"
            )
        
        # Continue processing the request
        return await call_next(request)
```

### 4.2.2 Customer Service

Customer Service quản lý thông tin người dùng, xác thực và ủy quyền.

#### 4.2.2.1 Cấu trúc dự án

```
customer-service/
├── customer_service/         # Main Django project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py          # Base settings
│   │   ├── development.py   # Development settings
│   │   ├── production.py    # Production settings
│   │   └── test.py          # Test settings
│   ├── urls.py
│   └── wsgi.py
├── users/                    # User management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py            # User models
│   ├── serializers.py       # User serializers
│   ├── services.py          # Business logic
│   ├── tests/               # Unit tests
│   ├── urls.py              # URL routing
│   └── views.py             # API endpoints
├── authentication/           # Authentication app
│   ├── __init__.py
│   ├── apps.py
│   ├── backends.py          # Custom auth backends
│   ├── jwt_utils.py         # JWT utilities
│   ├── serializers.py       # Auth serializers
│   ├── tests/               # Unit tests
│   ├── urls.py              # URL routing
│   └── views.py             # Auth endpoints
├── manage.py
├── Dockerfile
├── Dockerfile.dev
├── requirements.txt
└── README.md
```

#### 4.2.2.2 Mô hình User

```python
# customer-service/users/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('admin', 'Administrator'),
    )
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email

class Address(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'address_type', 'is_default')
    
    def __str__(self):
        return f"{self.user.email} - {self.address_type} - {self.street}"
```

#### 4.2.2.3 Serializers

```python
# customer-service/users/serializers.py
from rest_framework import serializers
from .models import User, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address_type', 'street', 'city', 'state', 'country', 
                  'zip_code', 'is_default')

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'user_type', 
                  'is_active', 'date_joined', 'addresses')
        read_only_fields = ('id', 'date_joined', 'is_active')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'user_type')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data.get('user_type', 'customer')
        )
        return user
```

#### 4.2.2.4 API Endpoints

```python
# customer-service/users/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Address
from .serializers import UserSerializer, UserRegistrationSerializer, AddressSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.user_type == 'admin':
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    @action(detail=True, methods=['get'])
    def addresses(self, request, pk=None):
        user = self.get_object()
        addresses = Address.objects.filter(user=user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_address(self, request, pk=None):
        user = self.get_object()
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

#### 4.2.2.5 JWT Authentication

```python
# customer-service/authentication/jwt_utils.py
import jwt
import datetime
from django.conf import settings

def generate_jwt_token(user):
    """Generate a JWT token for the given user."""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'user_type': user.user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
    return token

def validate_jwt_token(token):
    """Validate a JWT token and return the payload if valid."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.PyJWTError:
        return None
```

```python
# customer-service/authentication/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from .jwt_utils import generate_jwt_token

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            token = generate_jwt_token(user)
            return Response({
                'token': token,
                'user_id': user.id,
                'email': user.email,
                'user_type': user.user_type
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
```

### 4.2.3 Product Service

Product Service quản lý danh mục sản phẩm, thông tin sản phẩm và kho hàng.

#### 4.2.3.1 Cấu trúc dự án

```
product-service/
├── product_service/         # Main Django project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py          # Base settings
│   │   ├── development.py   # Development settings
│   │   ├── production.py    # Production settings
│   │   └── test.py          # Test settings
│   ├── urls.py
│   └── wsgi.py
├── products/                # Products app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # Product models
│   ├── serializers.py       # Product serializers
│   ├── services.py          # Business logic
│   ├── tests/               # Unit tests
│   ├── urls.py              # URL routing
│   └── views.py             # API endpoints
├── categories/              # Categories app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests/
│   ├── urls.py
│   └── views.py
├── inventory/               # Inventory app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests/
│   ├── urls.py
│   └── views.py
├── manage.py
├── Dockerfile
├── Dockerfile.dev
├── requirements.txt
└── README.md
```

#### 4.2.3.2 Product Models

MongoDB được sử dụng cho Product Service để lưu trữ dữ liệu sản phẩm, với định nghĩa mô hình như sau:

```python
# product-service/products/models.py
from django.db import models
from djongo.models import ObjectIdField, ArrayField
from categories.models import Category

class ProductAttribute(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    
    class Meta:
        abstract = True

class ProductImage(models.Model):
    url = models.URLField()
    alt_text = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

class Product(models.Model):
    _id = ObjectIdField()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    # MongoDB-specific fields
    attributes = ArrayField(
        model_container=ProductAttribute
    )
    images = ArrayField(
        model_container=ProductImage
    )
    tags = ArrayField(
        model_field=models.CharField(max_length=100)
    )
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    _id = ObjectIdField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Variant-specific attributes
    attributes = ArrayField(
        model_container=ProductAttribute
    )
    
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'product_variants'
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"
```

#### 4.2.3.3 Product API Endpoints

```python
# product-service/products/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductVariant
from .serializers import ProductSerializer, ProductDetailSerializer, ProductVariantSerializer
from .filters import ProductFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['price', 'created_at', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer
    
    @action(detail=True, methods=['get'])
    def variants(self, request, pk=None):
        product = self.get_object()
        variants = product.variants.filter(is_active=True)
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = Product.objects.filter(is_active=True, is_featured=True)
        serializer = ProductSerializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({'error': 'category_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        products = Product.objects.filter(is_active=True, category_id=category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
```

### 4.2.4 Order Service

Order Service quản lý giỏ hàng và đơn hàng trong hệ thống thương mại điện tử.

#### 4.2.4.1 Cấu trúc dự án

```
order-service/
├── order_service/           # Main Django project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py          # Base settings
│   │   ├── development.py   # Development settings
│   │   ├── production.py    # Production settings
│   │   └── test.py          # Test settings
│   ├── urls.py
│   └── wsgi.py
├── carts/                   # Shopping cart app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py          # Business logic
│   ├── tests/
│   ├── urls.py
│   └── views.py
├── orders/                  # Orders app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests/
│   ├── urls.py
│   └── views.py
├── clients/                 # Service clients
│   ├── __init__.py
│   ├── product_client.py    # Product service client
│   ├── customer_client.py   # Customer service client
│   └── payment_client.py    # Payment service client
├── manage.py
├── Dockerfile
├── Dockerfile.dev
├── requirements.txt
└── README.md
```

#### 4.2.4.2 Order Models

```python
# order-service/orders/models.py
from django.db import models

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    )
    
    user_id = models.CharField(max_length=36)  # UUID from customer service
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address_id = models.CharField(max_length=36, null=True, blank=True)
    
    # Payment information
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Shipping information
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.CharField(max_length=36)
    product_name = models.CharField(max_length=255)
    variant_id = models.CharField(max_length=36, null=True, blank=True)
    variant_name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Store product data as JSON for historical record
    product_data = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.product_name}"
```

#### 4.2.4.3 Service Communication

```python
# order-service/clients/product_client.py
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ProductClient:
    def __init__(self):
        self.base_url = settings.PRODUCT_SERVICE_URL
        self.timeout = settings.SERVICE_TIMEOUT
    
    def get_product(self, product_id):
        """Fetch product details from Product Service."""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/products/{product_id}/",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching product {product_id}: {str(e)}")
            return None
    
    def get_product_variant(self, product_id, variant_id):
        """Fetch product variant details from Product Service."""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/products/{product_id}/variants/{variant_id}/",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching variant {variant_id}: {str(e)}")
            return None
    
    def check_stock(self, product_id, variant_id=None, quantity=1):
        """Check if product is in stock with required quantity."""
        try:
            url = f"{self.base_url}/api/v1/inventory/check-stock/"
            data = {
                'product_id': product_id,
                'quantity': quantity
            }
            if variant_id:
                data['variant_id'] = variant_id
                
            response = requests.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking stock: {str(e)}")
            return {'is_available': False, 'message': 'Service unavailable'} 
```

## 4.3 Deployment

Phần này mô tả quy trình triển khai hệ thống thương mại điện tử microservices lên môi trường sản xuất, bao gồm các công nghệ và công cụ được sử dụng.

### 4.3.1 Containerization và Orchestration

#### 4.3.1.1 Docker Images cho Production

Tối ưu hóa Docker images cho môi trường sản xuất:

```dockerfile
# customer-service/Dockerfile
FROM python:3.9-slim AS builder

# Cài đặt dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Tạo final image
FROM python:3.9-slim

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Cài đặt dependencies từ wheels
WORKDIR /app
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy source code
COPY . .

# Chown tất cả các files đến user app
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=customer_service.settings.production

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "customer_service.wsgi:application"]
```

#### 4.3.1.2 Kubernetes Deployment

Triển khai hệ thống trên Kubernetes:

```yaml
# kubernetes/customer-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: customer-service
  namespace: ecom
  labels:
    app: customer-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: customer-service
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  template:
    metadata:
      labels:
        app: customer-service
    spec:
      containers:
      - name: customer-service
        image: ${DOCKER_REGISTRY}/customer-service:${VERSION}
        ports:
        - containerPort: 8000
        env:
        - name: DJANGO_SETTINGS_MODULE
          value: "customer_service.settings.production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: customer-service-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: customer-service-secrets
              key: secret-key
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: customer-service-secrets
              key: jwt-secret-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: customer-service
  namespace: ecom
spec:
  selector:
    app: customer-service
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

#### 4.3.1.3 Helm Charts

Sử dụng Helm charts để quản lý các ứng dụng Kubernetes:

```yaml
# helm/ecom-microservices/values.yaml
global:
  environment: production
  imageRegistry: registry.example.com
  imageTag: latest
  imagePullPolicy: Always

customerService:
  replicaCount: 3
  image:
    repository: customer-service
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  database:
    engine: mysql
    host: mysql-customer
    port: 3306
    name: customer_db
    user: customer_user

productService:
  replicaCount: 3
  image:
    repository: product-service
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  database:
    engine: mongodb
    host: mongodb-product
    port: 27017
    name: product_db

orderService:
  replicaCount: 3
  image:
    repository: order-service
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  database:
    engine: postgresql
    host: postgres-order
    port: 5432
    name: order_db
    user: order_user

# Các services khác...
```

### 4.3.2 CI/CD Pipeline

#### 4.3.2.1 GitHub Actions Workflow

Tự động hóa quy trình CI/CD với GitHub Actions:

```yaml
# .github/workflows/customer-service-ci-cd.yml
name: Customer Service CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - 'customer-service/**'
      - '.github/workflows/customer-service-ci-cd.yml'
  pull_request:
    branches: [main, develop]
    paths:
      - 'customer-service/**'

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        cd customer-service
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-django pytest-cov
        
    - name: Run tests
      env:
        DATABASE_URL: mysql://root:root@localhost:3306/test_db
        DJANGO_SETTINGS_MODULE: customer_service.settings.test
      run: |
        cd customer-service
        pytest --cov=. --cov-report=xml
        
    - name: Upload coverage report
      uses: codecov/codecov-action@v3
      with:
        file: ./customer-service/coverage.xml
        flags: customer-service
  
  build:
    needs: test
    if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop')
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
      
    - name: Login to Docker Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ secrets.DOCKER_REGISTRY }}
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
        
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: ./customer-service
        push: true
        tags: |
          ${{ secrets.DOCKER_REGISTRY }}/customer-service:${{ github.sha }}
          ${{ secrets.DOCKER_REGISTRY }}/customer-service:latest
  
  deploy-dev:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: development
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      
    - name: Set Kubernetes context
      uses: azure/k8s-set-context@v3
      with:
        kubeconfig: ${{ secrets.KUBE_CONFIG_DEV }}
        
    - name: Deploy to Kubernetes
      run: |
        cd kubernetes
        sed -i "s|\${DOCKER_REGISTRY}|${{ secrets.DOCKER_REGISTRY }}|g" customer-service-deployment.yaml
        sed -i "s|\${VERSION}|${{ github.sha }}|g" customer-service-deployment.yaml
        kubectl apply -f customer-service-deployment.yaml
        kubectl rollout status deployment/customer-service -n ecom
        
  deploy-prod:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      
    - name: Set Kubernetes context
      uses: azure/k8s-set-context@v3
      with:
        kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
        
    - name: Deploy to Kubernetes
      run: |
        cd kubernetes
        sed -i "s|\${DOCKER_REGISTRY}|${{ secrets.DOCKER_REGISTRY }}|g" customer-service-deployment.yaml
        sed -i "s|\${VERSION}|${{ github.sha }}|g" customer-service-deployment.yaml
        kubectl apply -f customer-service-deployment.yaml
        kubectl rollout status deployment/customer-service -n ecom
```

### 4.3.3 Database Migration và Quản lý Dữ liệu

#### 4.3.3.1 Django Migrations

Quản lý cấu trúc cơ sở dữ liệu với Django migrations:

```python
# customer-service/users/migrations/0001_initial.py
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('user_type', models.CharField(choices=[('customer', 'Customer'), ('seller', 'Seller'), ('admin', 'Administrator')], default='customer', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
```

#### 4.3.3.2 Migration Script

Tự động hóa migrations trong quá trình triển khai:

```bash
#!/bin/bash
# kubernetes/scripts/apply-migrations.sh

# Apply migrations for customer service
echo "Applying migrations for customer-service..."
kubectl exec -it $(kubectl get pods -l app=customer-service -n ecom -o jsonpath="{.items[0].metadata.name}") -n ecom -- python manage.py migrate

# Apply migrations for order service
echo "Applying migrations for order-service..."
kubectl exec -it $(kubectl get pods -l app=order-service -n ecom -o jsonpath="{.items[0].metadata.name}") -n ecom -- python manage.py migrate

# Apply migrations for other services...

echo "All migrations applied successfully!"
```

### 4.3.4 Monitoring và Logging

#### 4.3.4.1 Prometheus Metrics

Cấu hình metrics cho Prometheus:

```python
# customer-service/customer_service/metrics.py
from prometheus_client import Counter, Histogram
import time
from functools import wraps

# Define metrics
REQUEST_COUNT = Counter(
    'request_count', 
    'HTTP Request count',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'request_latency_seconds', 
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

USER_REGISTRATION = Counter(
    'user_registration_count', 
    'User registration count',
    ['status']
)

# Middleware để ghi metrics
class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method
        path = request.path
        
        # Đo thời gian xử lý request
        start_time = time.time()
        response = self.get_response(request)
        latency = time.time() - start_time
        
        # Ghi metrics
        REQUEST_LATENCY.labels(method=method, endpoint=path).observe(latency)
        REQUEST_COUNT.labels(
            method=method, 
            endpoint=path, 
            status=response.status_code
        ).inc()
        
        return response

# Decorator để đo lường hàm cụ thể
def measure_execution_time(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            REQUEST_LATENCY.labels(method='function', endpoint=name).observe(execution_time)
            
            return result
        return wrapper
    return decorator
```

#### 4.3.4.2 Centralized Logging với ELK Stack

Cấu hình Filebeat để thu thập logs từ các microservices:

```yaml
# kubernetes/logging/filebeat-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: filebeat-config
  namespace: monitoring
  labels:
    app: filebeat
data:
  filebeat.yml: |-
    filebeat.inputs:
    - type: container
      paths:
        - /var/log/containers/*.log
      processors:
        - add_kubernetes_metadata:
            host: ${NODE_NAME}
            matchers:
            - logs_path:
                logs_path: "/var/log/containers/"

    processors:
      - add_cloud_metadata:
      - add_host_metadata:

    output.elasticsearch:
      hosts: ['${ELASTICSEARCH_HOST:elasticsearch}:${ELASTICSEARCH_PORT:9200}']
      username: ${ELASTICSEARCH_USERNAME}
      password: ${ELASTICSEARCH_PASSWORD}
      index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"
```

#### 4.3.4.3 Grafana Dashboard

Cài đặt Grafana dashboard để visualize metrics:

```json
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": 1,
  "links": [],
  "panels": [
    {
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": "Prometheus",
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 0
      },
      "hiddenSeries": false,
      "id": 2,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "dataLinks": []
      },
      "percentage": false,
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "expr": "sum(rate(request_count{endpoint=~\"/api/v1/users.*\"}[5m])) by (endpoint)",
          "interval": "",
          "legendFormat": "{{endpoint}}",
          "refId": "A"
        }
      ],
      "thresholds": [],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "User API Request Rate",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    }
  ],
  "schemaVersion": 22,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "Customer Service Dashboard",
  "uid": "customer-service",
  "variables": {
    "list": []
  },
  "version": 1
}
```

### 4.3.5 Bảo mật hệ thống

#### 4.3.5.1 Kubernetes Network Policies

Thiết lập Network Policies để bảo vệ các services:

```yaml
# kubernetes/security/network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: customer-service-policy
  namespace: ecom
spec:
  podSelector:
    matchLabels:
      app: customer-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: mysql-customer
    ports:
    - protocol: TCP
      port: 3306
  - to:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 9090  # Prometheus
```

#### 4.3.5.2 HTTPS và TLS

Cấu hình HTTPS với cert-manager:

```yaml
# kubernetes/security/certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ecom-tls-cert
  namespace: ecom
spec:
  secretName: ecom-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: api.ecom-example.com
  dnsNames:
  - api.ecom-example.com
  - www.ecom-example.com
```

```yaml
# kubernetes/security/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecom-ingress
  namespace: ecom
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - api.ecom-example.com
    - www.ecom-example.com
    secretName: ecom-tls-secret
  rules:
  - host: api.ecom-example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-gateway
            port:
              number: 80
  - host: www.ecom-example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

## 4.4 Kết luận

Trong chương này, chúng tôi đã trình bày chi tiết về quá trình triển khai thực tế hệ thống thương mại điện tử sử dụng kiến trúc microservices với Django. Các điểm chính bao gồm:

1. **Môi trường phát triển**: Thiết lập môi trường phát triển nhất quán với Docker, đảm bảo các thành viên trong nhóm có thể làm việc hiệu quả.

2. **Triển khai microservices**: Mỗi microservice được cài đặt độc lập, với cơ sở dữ liệu riêng và API rõ ràng để giao tiếp với các services khác.

3. **Cài đặt CI/CD**: Tự động hóa quy trình kiểm thử, xây dựng và triển khai sử dụng GitHub Actions, giúp giảm thiểu lỗi và tăng tốc độ phát triển.

4. **Quản lý Container và Orchestration**: Sử dụng Docker và Kubernetes để đảm bảo tính nhất quán, khả năng mở rộng và tính sẵn sàng cao của hệ thống.

5. **Monitoring và Logging**: Triển khai hệ thống giám sát toàn diện với Prometheus, Grafana và ELK Stack để theo dõi hiệu suất và khắc phục sự cố nhanh chóng.

6. **Bảo mật**: Áp dụng các biện pháp bảo mật nhiều lớp, từ mã hóa dữ liệu, HTTPS, đến Network Policies và quản lý bí mật an toàn.

Việc triển khai thành công hệ thống thương mại điện tử microservices đòi hỏi sự kết hợp giữa kiến trúc phần mềm vững chắc, các công nghệ container hiện đại và quy trình DevOps tự động hóa. Điều này không chỉ giúp cải thiện hiệu suất và khả năng mở rộng của hệ thống mà còn tăng tốc quá trình phát triển và triển khai các tính năng mới.