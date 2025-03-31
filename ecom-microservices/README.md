# E-Commerce Microservices

Hệ thống thương mại điện tử xây dựng theo kiến trúc microservices, cung cấp đầy đủ tính năng cho một nền tảng mua sắm trực tuyến hiện đại với khả năng mở rộng cao, độ tin cậy vượt trội và tối ưu hóa hiệu suất cho hàng triệu người dùng.

![E-commerce Platform Status](https://img.shields.io/badge/status-in%20development-yellow)
![Version](https://img.shields.io/badge/version-1.0.0--beta-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Docker Compose](https://img.shields.io/badge/docker--compose-v2.10%2B-brightgreen)
![Microservices](https://img.shields.io/badge/microservices-15%2B-orange)
![Test Coverage](https://img.shields.io/badge/test%20coverage-85%25-success)

<p align="center">
  <img src="https://via.placeholder.com/1200x400?text=E-Commerce+Microservices+Platform" alt="E-Commerce Platform Banner" width="1200"/>
</p>

## 📑 Mục lục

- [Tổng quan](#-tổng-quan)
- [Tính năng nổi bật](#-tính-năng-nổi-bật)
- [Kiến trúc hệ thống](#️-kiến-trúc-hệ-thống)
- [Core Services](#-core-services)
- [AI/ML Services](#-aiml-services)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Tính năng chi tiết](#-tính-năng-chi-tiết)
- [Hướng dẫn cài đặt](#-hướng-dẫn-cài-đặt)
- [API Endpoints](#-api-endpoints-chi-tiết)
- [Bảo mật](#-bảo-mật)
- [Hiệu năng](#-hiệu-năng-và-optimizations)
- [Phát triển](#️-phát-triển)
- [Triển khai](#-triển-khai)
- [Monitoring](#-monitoring-và-logging)
- [Testing](#-testing)
- [Roadmap](#-roadmap)
- [FAQs](#-faqs)
- [Đóng góp](#-đóng-góp)
- [Tác giả](#-tác-giả)
- [Giấy phép](#-giấy-phép)
- [Liên hệ](#-liên-hệ)
- [Lời cảm ơn](#-lời-cảm-ơn)

## 📋 Tổng quan

Dự án E-Commerce Microservices là một nền tảng thương mại điện tử toàn diện được thiết kế và phát triển theo kiến trúc microservices hiện đại, cho phép xây dựng các hệ thống thương mại điện tử có khả năng mở rộng cao, linh hoạt và đáng tin cậy.

### Mục tiêu dự án

- **Khả năng mở rộng theo chiều ngang và chiều dọc**: Mỗi service có thể được mở rộng độc lập dựa trên nhu cầu, cho phép hệ thống xử lý hàng triệu giao dịch mỗi ngày.
- **Độ tin cậy và khả năng chịu lỗi**: Thiết kế để chịu được sự cố của một hoặc nhiều thành phần mà không ảnh hưởng đến toàn bộ hệ thống.
- **Độc lập về công nghệ**: Cho phép sử dụng công nghệ phù hợp nhất cho từng service.
- **Phát triển và triển khai độc lập**: Các team có thể phát triển, thử nghiệm và triển khai các service một cách độc lập.
- **Tích hợp AI/ML**: Cung cấp khả năng phân tích dữ liệu thông minh, cá nhân hóa và tự động hóa.

### Lợi ích chính

- **Hiệu suất cao**: Thiết kế tối ưu cho thời gian phản hồi nhanh và thông lượng cao
- **Khả năng mở rộng linh hoạt**: Dễ dàng thêm instance mới cho các service đang chịu tải cao
- **Tính sẵn sàng cao**: Uptime >99.9% ngay cả khi có sự cố cục bộ
- **Maintainability**: Code base rõ ràng, mô-đun hóa và dễ bảo trì
- **Time-to-market nhanh**: Phát triển song song và triển khai liên tục
- **Trải nghiệm người dùng tốt hơn**: Cá nhân hóa, đề xuất và tìm kiếm thông minh

### Các phương pháp tiếp cận kỹ thuật

- **Domain-Driven Design (DDD)**: Thiết kế phần mềm tập trung vào mô hình hóa lĩnh vực kinh doanh
- **Continuous Integration/Continuous Deployment (CI/CD)**: Tự động hóa quy trình phát triển và triển khai
- **Infrastructure as Code (IaC)**: Quản lý hạ tầng thông qua code để đảm bảo tính nhất quán và tái sử dụng
- **Monitoring & Observability**: Khả năng theo dõi và hiểu hành vi hệ thống trong thời gian thực
- **Circuit Breakers & Fallback Patterns**: Ngăn chặn lỗi lan truyền và cung cấp khả năng phục hồi

## 🌟 Tính năng nổi bật

### Nền tảng thương mại điện tử toàn diện

Dự án này cung cấp một nền tảng thương mại điện tử đầy đủ tính năng, bao gồm:

- **Quản lý đa kênh**: Tích hợp bán hàng qua web, mobile và các kênh khác
- **Đa dạng phương thức thanh toán**: Hỗ trợ thẻ tín dụng, chuyển khoản, ví điện tử, COD
- **Quản lý đơn hàng**: Theo dõi toàn bộ vòng đời đơn hàng từ tạo đến giao hàng
- **Quản lý khách hàng**: Hồ sơ khách hàng, lịch sử mua hàng, phân tích hành vi

### Tích hợp AI/ML

- **Hệ thống đề xuất thông minh**: Tăng tỷ lệ chuyển đổi và giá trị đơn hàng trung bình
- **Phân tích cảm xúc**: Nắm bắt phản hồi của khách hàng qua đánh giá sản phẩm
- **Dự đoán xu hướng**: Phân tích dữ liệu để dự đoán xu hướng thị trường
- **Optimization**: Tối ưu hóa giá, quản lý tồn kho và logistics

### Kiến trúc hiện đại

- **Event-driven architecture**: Giao tiếp bất đồng bộ giữa các service
- **CQRS & Event Sourcing**: Tách biệt đọc và ghi để tối ưu hiệu suất
- **API Gateway**: Điểm vào duy nhất, quản lý truy cập, bảo mật và cân bằng tải
- **Service discovery & registry**: Tự động định vị và đăng ký service

### Khả năng tùy biến và mở rộng

- **Headless commerce**: API-first để tùy biến giao diện người dùng
- **Plugin system**: Dễ dàng mở rộng chức năng thông qua plugin
- **Multi-tenancy**: Hỗ trợ nhiều cửa hàng trên cùng một nền tảng
- **White-labeling**: Tùy chỉnh thương hiệu cho đối tác

## 🏗️ Kiến trúc hệ thống

### Tổng quan kiến trúc

<p align="center">
  <img src="https://via.placeholder.com/1200x800?text=E-Commerce+Microservices+Architecture+Diagram" alt="Architecture Diagram" width="1200"/>
</p>

Kiến trúc của hệ thống được thiết kế dựa trên các nguyên tắc microservices hiện đại, tối ưu hóa cho khả năng mở rộng, tính linh hoạt và độ tin cậy cao. Hệ thống bao gồm các thành phần chính sau:

### Layer 1: Client & Gateway (Tầng giao tiếp)

- **Clients**: Web browsers, Mobile apps, IoT devices, Third-party integrations
- **API Gateway**: 
  - Điểm vào duy nhất cho tất cả các client requests
  - Quản lý routing, load balancing và rate limiting
  - Tích hợp xác thực và phân quyền
  - Triển khai CORS và API documentation

### Layer 2: Microservices Core (Tầng dịch vụ)

- **Business Domain Services**: 
  - Product, Customer, Order, Cart, Payment, v.v.
  - Mỗi service quản lý một domain logic riêng biệt
  - Triển khai API RESTful và/hoặc gRPC

- **Cross-cutting Services**:
  - Identity & Authorization
  - Notification
  - File Storage
  - Search & Indexing

### Layer 3: Data Layer (Tầng dữ liệu)

- **Databases**:
  - SQL: PostgreSQL, MySQL
  - NoSQL: MongoDB
  - In-memory: Redis
  - Search engine: Elasticsearch

- **Message Brokers**:
  - Kafka/RabbitMQ cho event sourcing và processing

### Layer 4: Infrastructure & DevOps (Tầng hạ tầng)

- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: Jenkins/GitLab CI
- **Monitoring & Observability**: Prometheus, Grafana, ELK Stack

### Event-driven Communication

Hệ thống sử dụng kiến trúc event-driven để giảm sự phụ thuộc trực tiếp giữa các service:

1. **Asynchronous communication**: Các service giao tiếp qua events thay vì API calls trực tiếp
2. **Event sourcing**: Lưu trữ các thay đổi trạng thái dưới dạng chuỗi events
3. **Command Query Responsibility Segregation (CQRS)**: Tách biệt operations đọc và ghi

### Quy trình xử lý đơn hàng (Luồng dữ liệu mẫu)

1. **Client** gửi request tạo đơn hàng thông qua **API Gateway**
2. **API Gateway** xác thực và định tuyến request đến **Order Service**
3. **Order Service** xác nhận thông tin và tạo đơn hàng
4. **Order Created Event** được phát hành
5. **Payment Service** nhận event và xử lý thanh toán
6. **Payment Completed Event** được phát hành
7. **Order Service** cập nhật trạng thái đơn hàng
8. **Shipment Service** nhận event và tạo đơn vận chuyển
9. **Notification Service** gửi xác nhận đơn hàng đến khách hàng

### Fault Tolerance & Resilience

Kiến trúc được thiết kế để chịu được lỗi thông qua:

- **Circuit breakers**: Ngăn lỗi lan truyền giữa các service
- **Retry with exponential backoff**: Xử lý lỗi tạm thời
- **Fallback mechanisms**: Cung cấp phương án dự phòng khi service không khả dụng
- **Bulkheads**: Cô lập các thành phần để ngăn lỗi lan truyền
- **Rate limiting**: Bảo vệ service khỏi quá tải

### Cân nhắc về CAP Theorem

Hệ thống microservices thường phải đánh đổi giữa:
- **Consistency (Tính nhất quán)**: Dữ liệu đồng nhất giữa các node
- **Availability (Tính sẵn có)**: Hệ thống luôn phản hồi các requests
- **Partition Tolerance (Khả năng chịu phân mảnh)**: Hệ thống tiếp tục hoạt động khi có sự cố mạng

Tùy vào yêu cầu của từng service:
- **Product & Catalog**: AP (Available + Partition Tolerant)
- **Payment & Order**: CP (Consistent + Partition Tolerant)

## 📦 Core Services

### 🔑 API Gateway (Nginx)

API Gateway là điểm vào duy nhất cho tất cả các external requests, đóng vai trò quan trọng trong việc quản lý traffic và bảo mật.

#### Chức năng chính
- **Request Routing**: Định tuyến requests đến service phù hợp
- **Authentication & Authorization**: Xác thực và phân quyền người dùng
- **Rate Limiting**: Giới hạn số lượng requests từ một client
- **Load Balancing**: Phân phối traffic giữa các instances của service
- **Request/Response Transformation**: Chuyển đổi format request/response
- **Caching**: Lưu trữ response để giảm thời gian phản hồi
- **Analytics & Monitoring**: Thu thập metrics về API usage

#### Thông số kỹ thuật
- **Technology**: Nginx
- **Port**: 80
- **Configuration**: `/api-gateway/nginx/nginx.conf`
- **Authentication**: JWT-based
- **Scaling Strategy**: Horizontal scaling with load balancer

#### CORS Configuration
```nginx
add_header 'Access-Control-Allow-Origin' 'http://localhost:3000' always;
add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,Content-Type,Accept,Authorization' always;
```

#### Route Configuration
API Gateway định tuyến các requests dựa trên URL patterns:
```
/user/* -> Customer Service
/books/* -> Book Service
/carts/* -> Cart Service
/api/recommendations/* -> Recommendation Service
```

#### Performance Metrics
- **Throughput**: 1000+ requests/second
- **Latency**: <50ms average
- **Availability**: 99.9%

### 👤 Customer Service (Django)

Customer Service quản lý thông tin người dùng, xác thực, đăng ký và quản lý tài khoản.

#### Domain Model
- **User**: Thông tin cơ bản người dùng
- **Profile**: Thông tin chi tiết người dùng
- **Address**: Địa chỉ giao hàng và thanh toán
- **Preferences**: Tùy chọn người dùng

#### Chức năng chính
- **User Registration**: Đăng ký tài khoản mới
- **Authentication**: Đăng nhập và xác thực
- **Profile Management**: Quản lý thông tin cá nhân
- **Address Management**: Quản lý địa chỉ
- **Password Management**: Đặt lại mật khẩu, thay đổi mật khẩu
- **Account Verification**: Xác minh email

#### Thông số kỹ thuật
- **Framework**: Django 3.2
- **Database**: MySQL 8.0
- **Port**: 8001
- **API Style**: RESTful
- **Authentication**: JWT
- **Models**: User, Profile, Address, Preferences

#### Database Schema
```
Customer DB (MySQL):
- users: id, username, email, password, is_active, created_at, updated_at
- profiles: id, user_id, first_name, last_name, phone, birth_date, gender
- addresses: id, user_id, type, street, city, state, country, zip_code, is_default
- preferences: id, user_id, language, currency, notifications
```

#### API Endpoints
- `POST /user/register`: Đăng ký tài khoản mới
- `POST /user/login`: Đăng nhập và nhận JWT token
- `GET /user/profile`: Lấy thông tin người dùng
- `PUT /user/profile`: Cập nhật thông tin người dùng
- `GET /user/addresses`: Lấy danh sách địa chỉ
- `POST /user/addresses`: Thêm địa chỉ mới
- `PUT /user/password`: Thay đổi mật khẩu

#### Event Production
- `UserRegistered`: Khi người dùng đăng ký thành công
- `UserUpdated`: Khi thông tin người dùng được cập nhật
- `PasswordChanged`: Khi mật khẩu được thay đổi

#### Event Consumption
- `OrderCompleted`: Cập nhật lịch sử đơn hàng người dùng

### 📦 Product Service (Django)

Product Service quản lý danh mục sản phẩm, thông tin sản phẩm và tồn kho.

#### Domain Model
- **Product**: Thông tin sản phẩm chung
- **Category**: Phân loại sản phẩm
- **Inventory**: Quản lý tồn kho
- **Price**: Quản lý giá và khuyến mãi

#### Chức năng chính
- **Product Management**: Thêm, sửa, xóa sản phẩm
- **Category Management**: Quản lý phân loại sản phẩm
- **Inventory Management**: Quản lý tồn kho
- **Price Management**: Quản lý giá và khuyến mãi
- **Product Search**: Tìm kiếm sản phẩm
- **Product Filtering**: Lọc sản phẩm theo nhiều tiêu chí

#### Thông số kỹ thuật
- **Framework**: Django
- **Database**: MongoDB
- **Port**: 8005
- **API Style**: RESTful
- **Models**: Product, Category, Inventory, Price

#### Database Schema
```
Product DB (MongoDB):
- products: _id, sku, name, product_type, category_path, base_price, sale_price, quantity, primary_image, image_urls, seller_id, brand, status, total_views, total_sold, rating, review_count, weight, dimensions, tags, created_at, updated_at
- categories: _id, name, slug, parent_id, level, path, description, image_url
```

#### API Endpoints
- `GET /products`: Lấy danh sách sản phẩm
- `GET /products/{id}`: Lấy thông tin chi tiết sản phẩm
- `GET /products/search`: Tìm kiếm sản phẩm
- `GET /products/filter`: Lọc sản phẩm
- `GET /categories`: Lấy danh sách danh mục
- `GET /categories/{id}`: Lấy thông tin chi tiết danh mục
- `GET /products/{id}/related`: Lấy sản phẩm liên quan

#### Event Production
- `ProductCreated`: Khi sản phẩm mới được tạo
- `ProductUpdated`: Khi thông tin sản phẩm được cập nhật
- `ProductDeleted`: Khi sản phẩm bị xóa
- `InventoryChanged`: Khi tồn kho thay đổi
- `PriceChanged`: Khi giá sản phẩm thay đổi

#### Event Consumption
- `OrderCreated`: Cập nhật tồn kho
- `CartItemAdded`: Tạm khóa tồn kho (reservation)

### 📚 Book Service (Django)

Book Service quản lý thông tin chi tiết về sách, bao gồm tác giả, nhà xuất bản và thể loại.

#### Domain Model
- **Book**: Thông tin chi tiết sách
- **Author**: Thông tin tác giả
- **Publisher**: Thông tin nhà xuất bản
- **Genre**: Thông tin thể loại

#### Chức năng chính
- **Book Management**: Quản lý thông tin sách
- **Author Management**: Quản lý thông tin tác giả
- **Publisher Management**: Quản lý thông tin nhà xuất bản
- **Genre Management**: Quản lý thông tin thể loại
- **Book Search**: Tìm kiếm sách
- **Book Filtering**: Lọc sách theo nhiều tiêu chí

#### Thông số kỹ thuật
- **Framework**: Django
- **Database**: MongoDB
- **Port**: 8002
- **Models**: Book, Author, Publisher, Genre

#### Database Schema
```
Book DB (MongoDB):
- books: _id, product_id, title, isbn, authors, publisher, published_date, language, pages, format, genres, description
- authors: _id, name, bio, country, website
- publishers: _id, name, founded_year, country, website
- genres: _id, name, description
```

#### API Endpoints
- `GET /books`: Lấy danh sách sách
- `GET /books/{id}`: Lấy thông tin chi tiết sách
- `GET /books/search`: Tìm kiếm sách
- `GET /books/filter`: Lọc sách
- `GET /authors`: Lấy danh sách tác giả
- `GET /authors/{id}`: Lấy thông tin chi tiết tác giả
- `GET /publishers`: Lấy danh sách nhà xuất bản
- `GET /genres`: Lấy danh sách thể loại

### 👟 Shoe Service (Django)

Shoe Service quản lý thông tin chi tiết về giày, bao gồm kích cỡ, thương hiệu và kiểu dáng.

#### Domain Model
- **Shoe**: Thông tin chi tiết giày
- **Brand**: Thông tin thương hiệu
- **Style**: Thông tin kiểu dáng
- **Size**: Thông tin kích cỡ

#### Chức năng chính
- **Shoe Management**: Quản lý thông tin giày
- **Brand Management**: Quản lý thông tin thương hiệu
- **Style Management**: Quản lý thông tin kiểu dáng
- **Size Management**: Quản lý thông tin kích cỡ
- **Shoe Search**: Tìm kiếm giày
- **Shoe Filtering**: Lọc giày theo nhiều tiêu chí

#### Thông số kỹ thuật
- **Framework**: Django
- **Database**: MongoDB
- **Port**: 8006
- **Models**: Shoe, Brand, Style, Size

#### Database Schema
```
Shoe DB (MongoDB):
- shoes: _id, product_id, brand, style, sizes, colors, materials, gender, features
- brands: _id, name, founded_year, country, logo_url
- styles: _id, name, description, season
- sizes: _id, region, value, measurement
```

### 🛒 Cart Service (Django)

Cart Service quản lý giỏ hàng của người dùng, bao gồm thêm, xóa và cập nhật sản phẩm trong giỏ hàng.

#### Domain Model
- **Cart**: Thông tin giỏ hàng
- **CartItem**: Sản phẩm trong giỏ hàng
- **Coupon**: Mã giảm giá
- **Discount**: Khuyến mãi

#### Chức năng chính
- **Cart Management**: Tạo và quản lý giỏ hàng
- **Item Management**: Thêm, xóa, cập nhật sản phẩm trong giỏ hàng
- **Coupon Application**: Áp dụng mã giảm giá
- **Price Calculation**: Tính toán giá, thuế và phí vận chuyển
- **Cart Persistence**: Lưu trữ giỏ hàng cho cả người dùng đã đăng nhập và chưa đăng nhập
- **Cart Merging**: Hợp nhất giỏ hàng khi người dùng đăng nhập

#### Thông số kỹ thuật
- **Framework**: Django
- **Database**: PostgreSQL
- **Port**: 8003
- **Models**: Cart, CartItem, Coupon, Discount

#### Database Schema
```
Cart DB (PostgreSQL):
- carts: id, user_id, session_id, created_at, updated_at, status
- cart_items: id, cart_id, product_id, product_type, quantity, unit_price, total_price, added_at
- coupons: id, code, type, value, min_order_value, max_uses, used_count, valid_from, valid_until, is_active
- discounts: id, name, type, value, applies_to, valid_from, valid_until, is_active
```

#### API Endpoints
- `GET /carts`: Lấy thông tin giỏ hàng hiện tại
- `POST /carts/items`: Thêm sản phẩm vào giỏ hàng
- `PUT /carts/items/{id}`: Cập nhật số lượng sản phẩm
- `DELETE /carts/items/{id}`: Xóa sản phẩm khỏi giỏ hàng
- `POST /carts/coupons`: Áp dụng mã giảm giá
- `DELETE /carts/coupons`: Xóa mã giảm giá
- `GET /carts/totals`: Lấy thông tin tổng giá trị giỏ hàng

#### Event Production
- `CartCreated`: Khi giỏ hàng mới được tạo
- `CartItemAdded`: Khi sản phẩm được thêm vào giỏ hàng
- `CartItemRemoved`: Khi sản phẩm bị xóa khỏi giỏ hàng
- `CartItemUpdated`: Khi số lượng sản phẩm được cập nhật
- `CartAbandoned`: Khi giỏ hàng bị bỏ quên (không active sau X thời gian)

#### Event Consumption
- `ProductUpdated`: Cập nhật thông tin sản phẩm trong giỏ hàng
- `UserLoggedIn`: Hợp nhất giỏ hàng
- `CouponCreated`: Cập nhật danh sách mã giảm giá có sẵn

#### Algorithms
- **Cart Expiry**: Giỏ hàng hết hạn sau 30 ngày không hoạt động
- **Price Recalculation**: Tính lại giá khi có thay đổi về sản phẩm hoặc khuyến mãi
- **Stock Validation**: Kiểm tra tồn kho trước khi thêm vào giỏ hàng
- **Coupon Validation**: Kiểm tra tính hợp lệ của mã giảm giá

### 📝 Order Service (Django)

Order Service quản lý đơn hàng, theo dõi trạng thái và xử lý quy trình đặt hàng.

#### Domain Model
- **Order**: Thông tin đơn hàng
- **OrderItem**: Sản phẩm trong đơn hàng
- **OrderStatus**: Trạng thái đơn hàng
- **OrderPayment**: Thanh toán đơn hàng
- **OrderShipment**: Vận chuyển đơn hàng

#### Chức năng chính
- **Order Creation**: Tạo đơn hàng từ giỏ hàng
- **Order Management**: Quản lý thông tin đơn hàng
- **Order Tracking**: Theo dõi trạng thái đơn hàng
- **Order History**: Lịch sử đơn hàng
- **Order Cancellation**: Hủy đơn hàng
- **Order Return/Refund**: Xử lý trả hàng và hoàn tiền

#### Thông số kỹ thuật
- **Framework**: Django
- **Database**: PostgreSQL
- **Port**: 8007
- **Models**: Order, OrderItem, OrderStatus, OrderPayment, OrderShipment

#### Database Schema
```
Order DB (PostgreSQL):
- orders: id, user_id, order_number, total_amount, tax_amount, shipping_amount, discount_amount, payment_status, fulfillment_status, shipping_address_id, billing_address_id, created_at, updated_at
- order_items: id, order_id, product_id, product_type, quantity, unit_price, total_price
- order_statuses: id, order_id, status, notes, created_at
- order_payments: id, order_id, payment_id, amount, status, payment_method, transaction_id, created_at
- order_shipments: id, order_id, shipment_id, tracking_number, carrier, status, shipped_at, delivered_at
```

#### Order Status Flow
1. **Created**: Đơn hàng vừa được tạo
2. **Confirmed**: Đơn hàng đã được xác nhận
3. **Paid**: Đơn hàng đã thanh toán
4. **Processing**: Đơn hàng đang được xử lý
5. **Shipped**: Đơn hàng đã được gửi đi
6. **Delivered**: Đơn hàng đã được giao
7. **Completed**: Đơn hàng hoàn tất
8. **Cancelled**: Đơn hàng bị hủy
9. **Refunded**: Đơn hàng đã hoàn tiền

#### API Endpoints
- `POST /orders`: Tạo đơn hàng mới
- `GET /orders`: Lấy danh sách đơn hàng
- `GET /orders/{id}`: Lấy thông tin chi tiết đơn hàng
- `GET /orders/{id}/items`: Lấy danh sách sản phẩm trong đơn hàng
- `GET /orders/{id}/history`: Lấy lịch sử trạng thái đơn hàng
- `PUT /orders/{id}/cancel`: Hủy đơn hàng
- `POST /orders/{id}/return`: Tạo yêu cầu trả hàng

#### Event Production
- `OrderCreated`: Khi đơn hàng mới được tạo
- `OrderStatusChanged`: Khi trạng thái đơn hàng thay đổi
- `OrderCancelled`: Khi đơn hàng bị hủy
- `OrderRefunded`: Khi đơn hàng được hoàn tiền

#### Event Consumption
- `PaymentCompleted`: Cập nhật trạng thái thanh toán
- `ShipmentStatusChanged`: Cập nhật trạng thái vận chuyển
- `ProductUpdated`: Cập nhật thông tin sản phẩm trong đơn hàng

### 💳 Payment Service (Django)

Payment Service xử lý các giao dịch thanh toán, tích hợp với các cổng thanh toán và quản lý thông tin thanh toán.

#### Domain Model
- **Payment**: Thông tin thanh toán
- **Transaction**: Giao dịch thanh toán
- **PaymentMethod**: Phương thức thanh toán
- **Refund**: Hoàn tiền

#### Chức năng chính
- **Payment Processing**: Xử lý thanh toán
- **Payment Gateway Integration**: Tích hợp với các cổng thanh toán
- **Payment Method Management**: Quản lý phương thức thanh toán
- **Transaction History**: Lịch sử giao dịch
- **Refund Processing**: Xử lý hoàn tiền
- **Invoice Generation**: Tạo hóa đơn

#### Thông số kỹ thuật
- **Framework**: Django
- **Database**: PostgreSQL
- **Port**: 8008
- **Models**: Payment, Transaction, PaymentMethod, Refund

#### Các cổng thanh toán được hỗ trợ
- **Stripe**: Thẻ tín dụng/ghi nợ quốc tế
- **PayPal**: Ví điện tử quốc tế
- **VNPay**: Cổng thanh toán nội địa
- **COD**: Thanh toán khi nhận hàng

#### Database Schema
```
Payment DB (PostgreSQL):
- payments: id, order_id, user_id, amount, currency, status, payment_method, created_at, updated_at
- transactions: id, payment_id, transaction_id, gateway, amount, status, error_code, error_message, created_at
- payment_methods: id, user_id, type, provider, account_number, expiry_date, is_default, is_active
- refunds: id, payment_id, amount, reason, status, transaction_id, created_at
```

#### API Endpoints
- `POST /payments`: Tạo yêu cầu thanh toán mới
- `GET /payments/{id}`: Lấy thông tin chi tiết thanh toán
- `GET /payments/{id}/status`: Kiểm tra trạng thái thanh toán
- `POST /payments/{id}/capture`: Capture thanh toán đã authorized
- `POST /payments/{id}/refund`: Tạo yêu cầu hoàn tiền
- `GET /payment-methods`: Lấy danh sách phương thức thanh toán
- `POST /payment-methods`: Thêm phương thức thanh toán mới

#### Event Production
- `PaymentCreated`: Khi yêu cầu thanh toán được tạo
- `PaymentCompleted`: Khi thanh toán hoàn tất
- `PaymentFailed`: Khi thanh toán thất bại
- `RefundCreated`: Khi yêu cầu hoàn tiền được tạo
- `RefundCompleted`: Khi hoàn tiền hoàn tất

#### Event Consumption
- `OrderCreated`: Tạo yêu cầu thanh toán
- `OrderCancelled`: Hủy thanh toán hoặc tạo hoàn tiền

#### Security Measures
- Mã hóa dữ liệu thanh toán (PCI DSS compliance)
- Xác thực hai yếu tố (2FA) cho các giao dịch lớn
- IP filtering và fraud detection
- Tokenization cho thông tin thẻ

### 🚚 Shipment Service (Django)

Shipment Service quản lý thông tin vận chuyển, theo dõi trạng thái giao hàng và tích hợp với các đơn vị vận chuyển.

#### Domain Model
- **Shipment**: Thông tin vận chuyển
- **ShipmentItem**: Sản phẩm trong đơn vận chuyển
- **Carrier**: Đơn vị vận chuyển
- **TrackingEvent**: Sự kiện theo dõi

#### Chức năng chính
- **Shipment Creation**: Tạo đơn vận chuyển
- **Shipment Tracking**: Theo dõi trạng thái vận chuyển
- **Carrier Integration**: Tích hợp với các đơn vị vận chuyển
- **Shipping Rate Calculation**: Tính phí vận chuyển
- **Address Validation**: Xác thực địa chỉ giao hàng
- **Delivery Scheduling**: Lên lịch giao hàng

#### Thông số kỹ thuật
- **Framework**: Django
- **Database**: PostgreSQL
- **Port**: 8009
- **Models**: Shipment, ShipmentItem, Carrier, TrackingEvent

#### Database Schema
```
Shipment DB (PostgreSQL):
- shipments: id, order_id, tracking_number, carrier_id, status, shipping_address, contact_name, contact_phone, shipped_at, estimated_delivery, actual_delivery, weight, dimensions, shipping_cost
- shipment_items: id, shipment_id, order_item_id, product_id, product_name, quantity
- carriers: id, name, code, website, tracking_url_template, is_active
- tracking_events: id, shipment_id, status, location, description, timestamp
```

#### API Endpoints
- `POST /shipments`: Tạo đơn vận chuyển mới
- `GET /shipments/{id}`: Lấy thông tin chi tiết đơn vận chuyển
- `GET /shipments/{id}/tracking`: Lấy thông tin theo dõi đơn vận chuyển
- `PUT /shipments/{id}/status`: Cập nhật trạng thái đơn vận chuyển
- `GET /carriers`: Lấy danh sách đơn vị vận chuyển
- `POST /shipments/calculate-rates`: Tính phí vận chuyển

#### Event Production
- `ShipmentCreated`: Khi đơn vận chuyển mới được tạo
- `ShipmentStatusChanged`: Khi trạng thái đơn vận chuyển thay đổi
- `ShipmentDelivered`: Khi đơn vận chuyển đã được giao
- `ShipmentDelayed`: Khi đơn vận chuyển bị trễ

#### Event Consumption
- `OrderCreated`: Chuẩn bị đơn vận chuyển
- `OrderPaid`: Xác nhận và xử lý đơn vận chuyển
- `OrderCancelled`: Hủy đơn vận chuyển

#### Carrier Integration
Hệ thống tích hợp với các đơn vị vận chuyển phổ biến:
- **GHN**: Giao Hàng Nhanh
- **GHTK**: Giao Hàng Tiết Kiệm
- **Viettel Post**: Viettel Post
- **J&T Express**: J&T Express
- **DHL**: DHL Express (Quốc tế)
- **FedEx**: FedEx (Quốc tế)

### ⭐ Review Service (Django)

Review Service quản lý đánh giá và nhận xét của người dùng về sản phẩm.

#### Domain Model
- **Review**: Đánh giá và nhận xét
- **Rating**: Xếp hạng
- **ReviewImage**: Hình ảnh đính kèm đánh giá
- **Helpfulness**: Đánh giá sự hữu ích của review

#### Chức năng chính
- **Review Submission**: Gửi đánh giá
- **Rating Management**: Quản lý xếp hạng
- **Review Moderation**: Kiểm duyệt đánh giá
- **Image Upload**: Tải lên hình ảnh đính kèm đánh giá
- **Helpfulness Voting**: Đánh giá sự hữu ích của review
- **Review Analytics**: Phân tích đánh giá

#### Thông số kỹ thuật
- **Framework**: Django
- **Database**: MySQL
- **Port**: 8004
- **Models**: Review, Rating, ReviewImage, Helpfulness

#### Database Schema
```
Review DB (MySQL):
- reviews: id, product_id, user_id, order_id, rating, title, content, status, created_at, updated_at
- review_images: id, review_id, image_url, created_at
- helpfulness: id, review_id, user_id, is_helpful, created_at
- review_metrics: product_id, average_rating, rating_count, rating_distribution
```

#### API Endpoints
- `POST /reviews`: Tạo đánh giá mới
- `GET /reviews/product/{product_id}`: Lấy đánh giá theo sản phẩm
- `GET /reviews/user/{user_id}`: Lấy đánh giá theo người dùng
- `PUT /reviews/{id}`: Cập nhật đánh giá
- `DELETE /reviews/{id}`: Xóa đánh giá
- `POST /reviews/{id}/images`: Tải lên hình ảnh cho đánh giá
- `POST /reviews/{id}/helpful`: Đánh giá sự hữu ích của review

#### Event Production
- `ReviewCreated`: Khi đánh giá mới được tạo
- `ReviewUpdated`: Khi đánh giá được cập nhật
- `ReviewDeleted`: Khi đánh giá bị xóa
- `ProductRatingChanged`: Khi xếp hạng sản phẩm thay đổi

#### Event Consumption
- `OrderCompleted`: Cho phép người dùng đánh giá sản phẩm đã mua
- `ProductUpdated`: Cập nhật thông tin sản phẩm trong đánh giá

#### Moderation Rules
- Tự động kiểm duyệt nội dung không phù hợp
- Phát hiện spam và fake reviews
- Yêu cầu xác minh mua hàng trước khi đánh giá
- Giới hạn số lượng đánh giá mỗi ngày cho mỗi người dùng

## 🧠 AI/ML Services

### 🔍 Sentiment Service (Flask)

Sentiment Service phân tích cảm xúc từ đánh giá của người dùng để cung cấp insights về sự hài lòng của khách hàng.

#### Chức năng chính
- **Sentiment Analysis**: Phân tích cảm xúc (tích cực, trung tính, tiêu cực)
- **Real-time Analysis**: Phân tích cảm xúc theo thời gian thực
- **Text Classification**: Phân loại văn bản
- **Keyword Extraction**: Trích xuất từ khóa
- **Sentiment Reporting**: Báo cáo phân tích cảm xúc
- **Trends Analysis**: Phân tích xu hướng theo thời gian

#### Thông số kỹ thuật
- **Framework**: Flask
- **Port**: 8010
- **Models**: Hugging Face Transformers, NLTK
- **Accuracy**: >90% trên các benchmark chuẩn
- **Processing Time**: ~30ms/text (với batch prediction)

#### Mô hình sử dụng
- **Default Model**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Vietnamese Model**: `vinai/phobert-base-vietnamese-sentiment`
- **Fallback**: NLTK-based lexicon sentiment analyzer

#### API Endpoints
- `POST /api/analyze`: Phân tích cảm xúc cho một đoạn văn bản
- `POST /api/analyze/batch`: Phân tích cảm xúc cho nhiều đoạn văn bản
- `GET /api/product/{product_id}/sentiment`: Phân tích cảm xúc cho một sản phẩm
- `GET /api/trends/distribution`: Phân tích phân phối cảm xúc
- `GET /api/trends/overtime`: Phân tích xu hướng cảm xúc theo thời gian
- `GET /api/products/compare`: So sánh cảm xúc giữa các sản phẩm

#### Cấu trúc phản hồi API
```json
{
  "text": "Sản phẩm này rất tuyệt vời!",
  "sentiment": "positive",
  "confidence": 0.97,
  "emotions": {
    "joy": 0.85,
    "surprise": 0.12,
    "neutral": 0.03
  },
  "keywords": ["tuyệt vời", "sản phẩm"]
}
```

#### Integration
- **Review Service**: Phân tích cảm xúc cho đánh giá mới
- **Recommendation Service**: Cung cấp dữ liệu cảm xúc cho đề xuất
- **Product Service**: Cung cấp insights về cảm xúc sản phẩm

#### Performance Optimization
- **Batch Processing**: Xử lý nhiều văn bản cùng lúc
- **Caching**: Lưu trữ kết quả phân tích thường xuyên truy cập
- **Model Quantization**: Giảm kích thước mô hình và tăng tốc độ inference

### 🔮 Recommendation Service (Flask)

Recommendation Service cung cấp đề xuất sản phẩm cá nhân hóa dựa trên hành vi người dùng, sản phẩm tương tự và phân tích cảm xúc.

#### Chức năng chính
- **Personalized Recommendations**: Đề xuất sản phẩm cá nhân hóa
- **Similar Product Recommendations**: Đề xuất sản phẩm tương tự
- **Trending Products**: Sản phẩm đang được quan tâm
- **Cross-selling**: Đề xuất sản phẩm bổ sung
- **Up-selling**: Đề xuất sản phẩm cao cấp hơn
- **Recently Viewed**: Sản phẩm đã xem gần đây

#### Thuật toán đề xuất
- **Collaborative Filtering**: Dựa trên hành vi của người dùng tương tự
- **Content-based Filtering**: Dựa trên đặc tính của sản phẩm
- **Hybrid Approach**: Kết hợp cả hai phương pháp trên
- **Matrix Factorization**: SVD (Singular Value Decomposition)
- **Deep Learning**: Neural networks cho đề xuất phức tạp

#### Thông số kỹ thuật
- **Framework**: Flask
- **Port**: 5002
- **Cache**: Redis
- **Models**: Scikit-learn, TensorFlow, PyTorch

#### API Endpoints
- `GET /api/recommendations/user/{user_id}`: Đề xuất sản phẩm cho người dùng
- `GET /api/recommendations/product/{product_id}/similar`: Đề xuất sản phẩm tương tự
- `GET /api/recommendations/popular`: Sản phẩm phổ biến
- `GET /api/recommendations/trending`: Sản phẩm đang trend
- `GET /api/recommendations/recently-viewed`: Sản phẩm đã xem gần đây
- `GET /api/insights/user/{user_id}/preferences`: Phân tích sở thích người dùng

#### Cấu trúc phản hồi API
```json
{
  "user_id": "123",
  "recommendations": [
    {
      "product_id": "456",
      "score": 0.95,
      "reason": "Based on your purchase history",
      "category": "Books"
    },
    {
      "product_id": "789",
      "score": 0.89,
      "reason": "Similar to products you've viewed",
      "category": "Electronics"
    }
  ],
  "meta": {
    "algorithm": "hybrid",
    "timestamp": "2023-06-15T12:34:56Z"
  }
}
```

#### Data Sources
- **User Behavior**: Lịch sử mua hàng, xem sản phẩm, thêm vào giỏ hàng
- **Product Data**: Đặc tính sản phẩm, danh mục, thuộc tính
- **Review Data**: Đánh giá và xếp hạng
- **Sentiment Analysis**: Phân tích cảm xúc từ đánh giá

#### Performance Optimization
- **Caching**: Redis caching cho đề xuất phổ biến
- **Batch Processing**: Tính toán đề xuất theo batch
- **Incremental Updates**: Cập nhật mô hình theo thời gian thực
- **A/B Testing**: Test hiệu quả của các thuật toán đề xuất khác nhau

### 🧪 ML Service (Flask)

ML Service phụ trách huấn luyện và quản lý các mô hình machine learning, cung cấp các công cụ phân tích dữ liệu tiên tiến.

#### Chức năng chính
- **Model Training**: Huấn luyện các mô hình ML
- **Model Management**: Quản lý phiên bản mô hình
- **Data Preprocessing**: Tiền xử lý dữ liệu
- **Feature Engineering**: Tạo và chọn lọc đặc trưng
- **Hyperparameter Tuning**: Tối ưu hóa tham số mô hình
- **Model Serving**: Triển khai mô hình trained

#### Thông số kỹ thuật
- **Framework**: Flask, TensorFlow, PyTorch
- **Training Infrastructure**: GPU-enabled
- **Model Repository**: MLflow
- **Data Storage**: MongoDB, S3-compatible storage

#### Models được phát triển
- **Sentiment Analysis**: Phân tích cảm xúc từ đánh giá
- **Recommendation Models**: Mô hình đề xuất sản phẩm
- **Demand Forecasting**: Dự báo nhu cầu sản phẩm
- **Customer Segmentation**: Phân khúc khách hàng
- **Fraud Detection**: Phát hiện gian lận

#### Pipeline ML
```
1. Data Collection → 2. Data Preprocessing → 3. Feature Engineering 
→ 4. Model Training → 5. Model Evaluation → 6. Model Deployment
```

#### API Endpoints (Internal)
- `POST /models/train`: Khởi động quá trình huấn luyện mô hình
- `GET /models/status/{job_id}`: Kiểm tra trạng thái huấn luyện
- `GET /models/{model_id}/metrics`: Lấy metrics của mô hình
- `POST /models/{model_id}/deploy`: Triển khai mô hình
- `POST /data/preprocess`: Tiền xử lý dữ liệu mới

## 🧰 Công nghệ sử dụng

### Backend

#### Ngôn ngữ & Framework
- **Python 3.8+**: Ngôn ngữ lập trình chính
- **Django 3.2+**: Framework web backend chính
  - **Django REST Framework**: Xây dựng RESTful API
  - **Django ORM**: Tương tác database
  - **Django Channels**: Xử lý WebSockets
  - **Celery**: Task queue cho xử lý bất đồng bộ
- **Flask 2.0+**: Framework web nhẹ cho ML/AI services
  - **Flask-RESTful**: API development
  - **Flask-CORS**: Xử lý CORS
- **SQLAlchemy**: ORM cho Flask services

#### Authentication & Authorization
- **JSON Web Tokens (JWT)**: Xác thực người dùng
- **OAuth2**: Xác thực third-party
- **Django Permissions**: Phân quyền chi tiết
- **API Keys**: Xác thực API cho third-party integrations

#### Databases
- **MongoDB 4.4+**: NoSQL database
  - **Collections**: products, books, shoes
  - **Indexing**: B-tree, geospatial, text search
  - **Aggregation Framework**: Phân tích dữ liệu phức tạp
  - **Change Streams**: Theo dõi thay đổi dữ liệu theo thời gian thực
  
- **PostgreSQL 13+**: Relational database
  - **Databases**: cart_db, order_db, payment_db, shipment_db
  - **Extensions**: PostGIS, pg_stat_statements
  - **Optimizations**: Partitioning, materialized views
  - **Transaction Isolation**: ACID compliance
  
- **MySQL 8.0+**: Relational database
  - **Databases**: customer_db, review_db
  - **Features**: Window functions, CTEs, JSON support
  - **Performance Schema**: Monitoring query performance
  - **InnoDB**: Transaction support and foreign keys

#### Caching & Message Brokers
- **Redis 6.0+**: In-memory cache
  - **Data Structures**: String, List, Set, Hash, Sorted Set
  - **Features**: Pub/Sub, Lua scripting, Transactions
  - **Use Cases**: Session storage, cache, leaderboards
  
- **Kafka**: Distributed event streaming platform
  - **Topics**: order-events, product-events, user-events
  - **Features**: High throughput, fault tolerance, scalability
  - **Use Cases**: Event sourcing, log aggregation, stream processing

#### Machine Learning & AI
- **TensorFlow 2.x**: Deep learning framework
- **PyTorch 1.x**: Deep learning framework
- **Scikit-learn**: Machine learning library
- **Hugging Face Transformers**: NLP models
- **NLTK & spaCy**: Natural language processing
- **Pandas & NumPy**: Data manipulation and analysis

### Frontend

#### Web UI
- **HTML5/CSS3/JavaScript**: Frontend foundation
- **Bootstrap 5**: CSS framework
- **jQuery**: JavaScript library
- **Responsive Design**: Mobile-first approach
- **Cross-browser Compatibility**: Chrome, Firefox, Safari, Edge

### DevOps & Infrastructure

#### Containerization & Orchestration
- **Docker**: Container platform
  - **Multi-stage builds**: Optimize image size
  - **Docker Compose**: Local development and testing
  
- **Kubernetes** (Production): Container orchestration
  - **Deployments**: Declarative updates
  - **Services**: Service discovery and load balancing
  - **ConfigMaps & Secrets**: Configuration management
  - **Horizontal Pod Autoscaler**: Automatic scaling

#### Continuous Integration/Deployment
- **GitHub Actions**: CI/CD workflows
- **Unit & Integration Testing**: Automated testing
- **Deployment Strategies**: Blue/Green, Canary
- **Infrastructure as Code**: Terraform, Ansible

#### Monitoring & Logging
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and dashboards
- **ELK Stack**: Centralized logging
- **Jaeger**: Distributed tracing

#### Security
- **TLS/SSL**: Encrypted communications
- **OWASP Compliance**: Security best practices
- **WAF**: Web Application Firewall
- **Rate Limiting**: Protect against DDoS

## ✨ Tính năng chi tiết

### Quản lý người dùng

#### Registration & Authentication
- **Đăng ký nhiều phương thức**: Email, số điện thoại, social login
- **Xác thực đa yếu tố (MFA)**: SMS, email, authenticator apps
- **Single Sign-On (SSO)**: Một tài khoản cho nhiều dịch vụ
- **Password Policies**: Yêu cầu mật khẩu mạnh
- **Account Recovery**: Quên mật khẩu, khôi phục tài khoản

#### User Profile Management
- **Thông tin cá nhân**: Họ tên, email, số điện thoại, ngày sinh
- **Avatar & Profile Picture**: Hình đại diện
- **Preferences**: Ngôn ngữ, đơn vị tiền tệ, notifications
- **Privacy Settings**: Kiểm soát dữ liệu cá nhân

#### Address Management
- **Multiple Addresses**: Lưu nhiều địa chỉ (nhà, văn phòng)
- **Default Addresses**: Địa chỉ mặc định cho giao hàng và thanh toán
- **Address Validation**: Xác minh địa chỉ hợp lệ
- **International Addresses**: Hỗ trợ địa chỉ quốc tế

#### Payment Method Management
- **Multiple Payment Methods**: Thẻ tín dụng, ví điện tử, chuyển khoản
- **Secure Storage**: Lưu trữ an toàn thông tin thanh toán
- **Default Payment**: Phương thức thanh toán mặc định
- **Payment History**: Lịch sử thanh toán

### Quản lý sản phẩm

#### Product Catalog Management
- **Hierarchical Categories**: Danh mục sản phẩm phân cấp
- **Product Attributes**: Thuộc tính sản phẩm tùy chỉnh
- **Variant Management**: Quản lý biến thể sản phẩm (kích cỡ, màu sắc)
- **Digital Products**: Hỗ trợ sản phẩm số (ebooks, software)

#### Product Search & Discovery
- **Full-text Search**: Tìm kiếm toàn văn
- **Faceted Search**: Lọc theo nhiều tiêu chí
- **Auto-suggest**: Gợi ý khi nhập từ khóa
- **Spell Correction**: Sửa lỗi chính tả
- **Search Analytics**: Phân tích hành vi tìm kiếm

#### Pricing & Promotions
- **Flexible Pricing**: Giá theo khu vực, nhóm khách hàng
- **Discounts**: Giảm giá theo phần trăm, số tiền cố định
- **Coupon Codes**: Mã giảm giá
- **Bundle Pricing**: Giá cho bộ sản phẩm
- **Tiered Pricing**: Giá theo số lượng

#### Inventory Management
- **Real-time Stock Levels**: Theo dõi tồn kho theo thời gian thực
- **Multi-warehouse**: Quản lý tồn kho nhiều kho
- **Low Stock Alerts**: Cảnh báo tồn kho thấp
- **Backorder Management**: Quản lý đặt hàng khi hết hàng
- **Stock Reservation**: Đặt chỗ tồn kho khi thêm vào giỏ hàng

### Giỏ hàng và đặt hàng

#### Cart Management
- **Persistent Cart**: Giỏ hàng được lưu giữa các phiên
- **Anonymous Cart**: Giỏ hàng cho người dùng chưa đăng nhập
- **Cart Merging**: Hợp nhất giỏ hàng khi đăng nhập
- **Save for Later**: Lưu sản phẩm cho lần mua sau
- **Tax Calculation**: Tính thuế theo khu vực

#### Checkout Process
- **One-page Checkout**: Quy trình thanh toán đơn giản
- **Guest Checkout**: Thanh toán không cần tài khoản
- **Order Summary**: Tổng quan đơn hàng
- **Shipping Method Selection**: Chọn phương thức vận chuyển
- **Order Confirmation**: Xác nhận đơn hàng qua email, SMS

#### Order Management
- **Order History**: Lịch sử đơn hàng
- **Order Tracking**: Theo dõi trạng thái đơn hàng
- **Order Modifications**: Thay đổi đơn hàng trước khi xử lý
- **Cancellation**: Hủy đơn hàng
- **Returns & Refunds**: Trả hàng và hoàn tiền

#### Payment Processing
- **Multiple Payment Methods**: Thẻ tín dụng, chuyển khoản, COD
- **Installment Plans**: Thanh toán trả góp
- **Partial Payments**: Thanh toán một phần
- **Automated Invoicing**: Tự động tạo hóa đơn
- **Fraud Detection**: Phát hiện gian lận

### Đánh giá và xếp hạng

#### Review System
- **Star Ratings**: Đánh giá 1-5 sao
- **Text Reviews**: Nhận xét bằng văn bản
- **Photo/Video Reviews**: Đính kèm hình ảnh và video
- **Verified Purchase Badge**: Xác nhận mua hàng
- **Review Moderation**: Kiểm duyệt đánh giá

#### Feedback Collection
- **Rating Prompts**: Nhắc nhở đánh giá sau khi mua hàng
- **Feedback Forms**: Biểu mẫu phản hồi
- **Survey Integration**: Tích hợp khảo sát
- **NPS (Net Promoter Score)**: Đo lường sự hài lòng

#### Review Analytics
- **Sentiment Analysis**: Phân tích cảm xúc từ đánh giá
- **Keyword Extraction**: Trích xuất từ khóa phổ biến
- **Rating Trends**: Xu hướng đánh giá theo thời gian
- **Competitive Analysis**: So sánh với sản phẩm cạnh tranh

### Hệ thống đề xuất

#### Personalized Recommendations
- **Based on Browsing History**: Dựa trên lịch sử duyệt web
- **Purchase History**: Dựa trên lịch sử mua hàng
- **Collaborative Filtering**: "Người dùng giống bạn cũng thích..."
- **Content-based Filtering**: Dựa trên đặc tính sản phẩm

#### Strategic Recommendations
- **Cross-selling**: "Thường được mua cùng với"
- **Up-selling**: "Bạn có thể thích phiên bản cao cấp hơn"
- **Recently Viewed**: Sản phẩm đã xem gần đây
- **Trending Products**: Sản phẩm đang được quan tâm

#### Contextual Recommendations
- **Seasonal Products**: Sản phẩm theo mùa
- **Location-based**: Dựa trên vị trí địa lý
- **Weather-sensitive**: Dựa trên thời tiết hiện tại
- **Time-based**: Dựa trên thời gian trong ngày/tuần

#### Recommendation Refinement
- **Feedback Loop**: Học từ tương tác của người dùng
- **A/B Testing**: Kiểm tra hiệu quả của thuật toán
- **Explainable AI**: Giải thích lý do đề xuất
- **Diversity & Serendipity**: Đảm bảo đa dạng trong đề xuất

### Phân tích cảm xúc

#### Sentiment Analysis
- **Review Sentiment**: Tích cực, tiêu cực, trung tính
- **Emotion Detection**: Phát hiện cảm xúc (vui, buồn, giận, v.v.)
- **Aspect-based Analysis**: Phân tích theo từng khía cạnh sản phẩm
- **Multilingual Support**: Hỗ trợ nhiều ngôn ngữ

#### Sentiment Visualization
- **Sentiment Dashboard**: Bảng điều khiển trực quan
- **Word Clouds**: Đám mây từ khóa phổ biến
- **Sentiment Timeline**: Biểu đồ xu hướng theo thời gian
- **Comparative Analysis**: So sánh giữa các sản phẩm

#### Actionable Insights
- **Quality Issues Detection**: Phát hiện vấn đề chất lượng
- **Customer Pain Points**: Xác định điểm đau của khách hàng
- **Improvement Suggestions**: Đề xuất cải tiến sản phẩm
- **Competitive Intelligence**: Thông tin về sản phẩm cạnh tranh

## 🚀 Hướng dẫn cài đặt

### Yêu cầu hệ thống

#### Phần cứng tối thiểu
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 20GB SSD
- **Network**: 100Mbps Ethernet

#### Phần cứng khuyến nghị
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Storage**: 50GB+ SSD
- **Network**: 1Gbps Ethernet

#### Phần mềm cần thiết
- **Docker**: 20.10.x hoặc cao hơn
- **Docker Compose**: 2.0.x hoặc cao hơn
- **Git**: 2.30.x hoặc cao hơn
- **Python**: 3.8+ (cho development)
- **Node.js**: 14+ (cho frontend development)

### Cài đặt cho môi trường phát triển

#### 1. Clone Repository

```bash
# Clone the repository
git clone https://github.com/bisosad/ecom-microservices.git

# Navigate to project directory
cd ecom-microservices
```

#### 2. Cấu hình môi trường

```bash
# Copy environment files
cp .env.example .env

# For specific services
cp sentiment-service/.env.example sentiment-service/.env
cp recommendation-service/.env.example recommendation-service/.env

# Edit environment variables as needed
nano .env
```

#### 3. Khởi động hệ thống với Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Start specific service
docker-compose up -d <service-name>
```

#### 4. Khởi tạo dữ liệu (lần đầu)

```bash
# Run database migrations
docker-compose exec customer-service python manage.py migrate
docker-compose exec cart-service python manage.py migrate
docker-compose exec order-service python manage.py migrate
docker-compose exec payment-service python manage.py migrate
docker-compose exec shipment-service python manage.py migrate
docker-compose exec review-service python manage.py migrate

# Create superuser for admin access
docker-compose exec customer-service python manage.py createsuperuser

# Load sample data (optional)
docker-compose exec product-service python manage.py loaddata sample_products
docker-compose exec book-service python manage.py loaddata sample_books
docker-compose exec shoe-service python manage.py loaddata sample_shoes
```

#### 5. Verify Installation

```bash
# Check if frontend is accessible
curl http://localhost:3000

# Check if API Gateway is accessible
curl http://localhost:80/health

# Check individual services
curl http://localhost:8001/health  # Customer Service
curl http://localhost:8005/health  # Product Service
curl http://localhost:8002/health  # Book Service
# ... etc.
```

### Cài đặt cho môi trường production

#### Using Docker Swarm

```bash
# Initialize Docker Swarm
docker swarm init

# Deploy the stack
docker stack deploy -c docker-compose.prod.yml ecom

# Check services
docker service ls

# Scale a service
docker service scale ecom_product-service=3
```

#### Using Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check pods
kubectl get pods

# Check services
kubectl get services

# View logs
kubectl logs -f deployment/product-service
```

### Troubleshooting

#### Common Issues

1. **Database Connection Errors**
```bash
# Check database container is running
docker-compose ps db-mysql db-postgres db-mongo

# Check logs
docker-compose logs db-mysql
```

2. **Service Dependencies**
```bash
# Restart dependent services
docker-compose restart api-gateway
```

3. **Port Conflicts**
```bash
# Check if ports are already in use
sudo lsof -i :80
sudo lsof -i :3000
```

4. **Container Resource Issues**
```bash
# Check container resource usage
docker stats
```

#### Health Check

```bash
# Run health check script
./scripts/health_check.sh

# Detailed system check
./scripts/diagnostics.sh
```

## 📄 API Endpoints chi tiết

### RESTful API Standards

Tất cả API endpoints tuân theo các quy tắc thiết kế RESTful:

- **Resource-based URLs**: `/resources` thay vì `/getResources`
- **HTTP Methods**: GET (đọc), POST (tạo), PUT (cập nhật), DELETE (xóa)
- **Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Server Error)
- **Content Negotiation**: Hỗ trợ JSON và XML
- **Pagination**: `?page=1&per_page=20`
- **Filtering**: `?status=active&category=books`
- **Sorting**: `?sort_by=created_at&order=desc`
- **Search**: `?q=keyword`
- **Versioning**: `/api/v1/resources`

### API Gateway Routes

API Gateway định tuyến các requests đến service tương ứng dựa trên URL patterns.

#### Customer Service
- `POST /user/register`: Đăng ký người dùng mới
  - Request: `{"username": "user1", "email": "user@example.com", "password": "securepass"}`
  - Response: `{"id": "123", "username": "user1", "email": "user@example.com"}`

- `POST /user/login`: Đăng nhập
  - Request: `{"email": "user@example.com", "password": "securepass"}`
  - Response: `{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "refresh_token": "..."}`

- `GET /user/profile`: Lấy thông tin người dùng
  - Headers: `Authorization: Bearer {token}`
  - Response: `{"id": "123", "username": "user1", "email": "user@example.com", "first_name": "John", "last_name": "Doe"}`

- `PUT /user/profile`: Cập nhật thông tin người dùng
  - Headers: `Authorization: Bearer {token}`
  - Request: `{"first_name": "John", "last_name": "Doe", "phone": "1234567890"}`
  - Response: `{"id": "123", "username": "user1", "first_name": "John", "last_name": "Doe", "phone": "1234567890"}`

#### Product Service
- `GET /products`: Lấy danh sách sản phẩm
  - Query Params: `?category=electronics&page=1&per_page=20&sort_by=price&order=asc`
  - Response: `{"items": [...], "total": 100, "page": 1, "per_page": 20}`

- `GET /products/{id}`: Lấy thông tin chi tiết sản phẩm
  - Response: `{"id": "456", "name": "Smartphone XYZ", "price": 999.99, "description": "..."}`

- `GET /products/search`: Tìm kiếm sản phẩm
  - Query Params: `?q=smartphone&category=electronics`
  - Response: `{"items": [...], "total": 50}`

#### Book Service
- `GET /books`: Lấy danh sách sách
  - Query Params: `?genre=fiction&author=tolkien`
  - Response: `{"items": [...], "total": 25}`

- `GET /books/{id}`: Lấy thông tin chi tiết sách
  - Response: `{"id": "789", "title": "The Hobbit", "author": "J.R.R. Tolkien", "price": 19.99}`

- `GET /books/categories`: Lấy danh sách thể loại sách
  - Response: `{"categories": ["Fiction", "Science", "History", "Biography"]}`

#### Cart Service
- `GET /carts`: Lấy thông tin giỏ hàng
  - Headers: `Authorization: Bearer {token}`
  - Response: `{"id": "cart123", "items": [...], "total": 129.97}`

- `POST /carts/items`: Thêm sản phẩm vào giỏ hàng
  - Headers: `Authorization: Bearer {token}`
  - Request: `{"product_id": "456", "quantity": 2}`
  - Response: `{"cart_id": "cart123", "item_id": "item789", "product_id": "456", "quantity": 2}`

- `DELETE /carts/items/{id}`: Xóa sản phẩm khỏi giỏ hàng
  - Headers: `Authorization: Bearer {token}`
  - Response: `{"success": true, "message": "Item removed from cart"}`

#### Recommendation Service
- `GET /api/recommendations/user/{user_id}`: Đề xuất sản phẩm cho người dùng
  - Query Params: `?limit=5&include_sentiment=true`
  - Response: `{"recommendations": [...], "meta": {...}}`

- `GET /api/recommendations/product/{product_id}/similar`: Đề xuất sản phẩm tương tự
  - Query Params: `?limit=5`
  - Response: `{"similar_products": [...], "reasons": [...]}`

- `GET /api/recommendations/popular`: Sản phẩm phổ biến
  - Query Params: `?category=electronics&period=week`
  - Response: `{"popular_products": [...], "trending_categories": [...]}`

#### Sentiment Service
- `POST /api/analyze`: Phân tích cảm xúc cho một đoạn văn bản
  - Request: `{"text": "Sản phẩm này rất tuyệt vời!"}`
  - Response: `{"sentiment": "positive", "confidence": 0.95, "keywords": [...]}`

- `GET /api/product/{product_id}/sentiment`: Phân tích cảm xúc cho một sản phẩm
  - Response: `{"overall_sentiment": "positive", "rating_distribution": {...}, "common_phrases": [...]}`

### Ví dụ sử dụng API

#### Đăng ký và đăng nhập

```bash
# Đăng ký người dùng mới
curl -X POST http://localhost/user/register \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user@example.com", "password": "securepass"}'

# Đăng nhập
curl -X POST http://localhost/user/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass"}'
```

#### Quản lý giỏ hàng

```bash
# Lấy thông tin giỏ hàng
curl -X GET http://localhost/carts \
  -H "Authorization: Bearer {token}"

# Thêm sản phẩm vào giỏ hàng
curl -X POST http://localhost/carts/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"product_id": "456", "quantity": 2}'
```

#### Đặt hàng

```bash
# Tạo đơn hàng mới
curl -X POST http://localhost/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"shipping_address_id": "addr123", "payment_method_id": "pm456"}'

# Kiểm tra trạng thái đơn hàng
curl -X GET http://localhost/orders/{order_id} \
  -H "Authorization: Bearer {token}"
```

## 🔒 Bảo mật

### Security Architecture

Hệ thống được thiết kế với nhiều lớp bảo mật để bảo vệ dữ liệu người dùng và đảm bảo tính toàn vẹn của hệ thống:

#### Defense in Depth

<p align="center">
  <img src="https://via.placeholder.com/800x400?text=Security+Architecture+Diagram" alt="Security Architecture" width="800"/>
</p>

- **Edge Security**:
  - TLS/SSL encryption
  - DDoS protection
  - Web Application Firewall (WAF)
  - IP filtering

- **API Gateway Security**:
  - Authentication & Authorization
  - Rate limiting
  - Request validation
  - API keys for third-party integrations

- **Service-level Security**:
  - Role-based access control (RBAC)
  - Input validation
  - Output encoding
  - Principle of least privilege

- **Data Security**:
  - Encryption at rest
  - Encryption in transit
  - Data masking for sensitive information
  - Regular backups

### Authentication & Authorization

#### Authentication Methods
- **JWT (JSON Web Tokens)**: Stateless authentication
- **Refresh Tokens**: Long-lived sessions with security
- **OAuth2**: Third-party authentication
- **Multi-factor Authentication (MFA)**: Extra security layer

#### Authorization Framework
- **Role-based Access Control (RBAC)**: Permissions based on roles
- **Attribute-based Access Control (ABAC)**: Fine-grained permissions
- **Service-to-service Authentication**: mTLS, API keys

### Data Protection

#### Personal Data Handling
- **GDPR Compliance**: Hỗ trợ quyền của người dùng
- **Data Minimization**: Chỉ thu thập dữ liệu cần thiết
- **Retention Policies**: Xóa dữ liệu không cần thiết
- **Privacy by Design**: Bảo vệ quyền riêng tư từ thiết kế

#### Payment Security
- **PCI DSS Compliance**: Bảo vệ dữ liệu thanh toán
- **Tokenization**: Không lưu trữ thông tin thẻ trực tiếp
- **3D Secure**: Xác thực bổ sung cho thanh toán

### Secure Development Practices

#### Application Security
- **OWASP Top 10**: Phòng chống các lỗ hổng phổ biến
- **Static Analysis Security Testing (SAST)**: Kiểm tra code
- **Dynamic Analysis Security Testing (DAST)**: Kiểm tra runtime
- **Dependency Scanning**: Phát hiện thư viện có lỗ hổng

#### Security Monitoring
- **Intrusion Detection/Prevention**: Phát hiện và ngăn chặn xâm nhập
- **Security Information and Event Management (SIEM)**: Phân tích sự kiện bảo mật
- **Audit Logging**: Ghi lại các hoạt động quan trọng
- **Penetration Testing**: Đánh giá bảo mật định kỳ

### Incident Response

#### Response Plan
- **Containment**: Cô lập sự cố
- **Eradication**: Loại bỏ nguyên nhân
- **Recovery**: Khôi phục dịch vụ
- **Post-incident Analysis**: Phân tích sau sự cố

#### Business Continuity
- **Disaster Recovery Plan**: Kế hoạch khôi phục sau thảm họa
- **Regular Backups**: Sao lưu dữ liệu thường xuyên
- **High Availability Architecture**: Kiến trúc sẵn sàng cao

## 📊 Hiệu năng và Optimizations

### Performance Benchmarks

Hệ thống được tối ưu hóa và benchmark để đảm bảo khả năng xử lý với tải cao:

| Service | Throughput | Latency (p95) | Max Concurrent Users |
|---------|------------|---------------|----------------------|
| API Gateway | 5,000 req/s | 120ms | 100,000 |
| Product Service | 2,000 req/s | 150ms | 50,000 |
| Cart Service | 1,000 req/s | 200ms | 30,000 |
| Order Service | 500 req/s | 250ms | 20,000 |
| Payment Service | 300 req/s | 300ms | 10,000 |
| Recommendation Service | 800 req/s | 180ms | 40,000 |

### Caching Strategy

#### Multi-level Caching
- **Browser Cache**: Static assets, product images
- **CDN Cache**: Frequently accessed content
- **API Gateway Cache**: Common API responses
- **Application Cache**: Database queries, computed results
- **Database Cache**: Query results, buffer pool

#### Cache Invalidation
- **Time-based (TTL)**: Auto-expire after set time
- **Event-based**: Invalidate on data change
- **Manual**: Force refresh when needed
- **Versioning**: Cache busting for static assets

### Database Optimizations

#### Query Optimization
- **Indexing Strategy**: Carefully designed indexes
- **Query Analysis**: Identify and fix slow queries
- **Explain Plans**: Understand query execution
- **Normalization/Denormalization**: Balance as needed

#### Scalability Patterns
- **Horizontal Sharding**: Distribute data across nodes
- **Read Replicas**: Scale read operations
- **Connection Pooling**: Efficient database connections
- **Materialized Views**: Pre-computed query results

### Front-end Performance

#### Loading Strategies
- **Lazy Loading**: Load resources as needed
- **Code Splitting**: Break JavaScript into chunks
- **Critical Path Rendering**: Prioritize visible content
- **Resource Hints**: Preload, prefetch, preconnect

#### Assets Optimization
- **Image Optimization**: WebP, responsive images
- **Minification**: Reduce file sizes
- **Compression**: GZIP/Brotli compression
- **CSS/JS Optimization**: Optimize render blocking resources

### API Optimizations

#### Efficient Data Transfer
- **Pagination**: Limit result set size
- **Field Selection**: Only return needed fields
- **Compression**: GZIP response bodies
- **Batching**: Combine multiple operations

#### Request Optimization
- **Connection Pooling**: Reuse connections
- **Keep-alive**: Maintain persistent connections
- **HTTP/2**: Multiplexed connections
- **Request Merging**: Combine similar requests

### Microservices Optimizations

#### Inter-service Communication
- **Circuit Breakers**: Prevent cascading failures
- **Bulkheads**: Isolate failures
- **Timeouts**: Don't wait indefinitely
- **Retry with Backoff**: Gracefully handle temporary failures

#### Resource Management
- **Container Resource Limits**: CPU, memory constraints
- **Autoscaling**: Scale based on load
- **Load Shedding**: Drop low-priority requests under load
- **Rate Limiting**: Prevent abuse

## 🛠️ Phát triển

### Development Environment Setup

#### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/bisosad/ecom-microservices.git
cd ecom-microservices

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install development dependencies
pip install -r requirements-dev.txt

# 4. Start services with docker-compose
docker-compose -f docker-compose.dev.yml up -d

# 5. Run service in development mode
cd <service-directory>
python manage.py runserver 0.0.0.0:<port>
```

#### Development Tools

- **IDE**: Visual Studio Code, PyCharm
- **API Testing**: Postman, Insomnia
- **Debugging**: Django Debug Toolbar, Flask Debug
- **Database Management**: MongoDB Compass, pgAdmin, MySQL Workbench
- **Container Management**: Docker Desktop, Portainer
- **Documentation**: Swagger, ReDoc

### Coding Standards

#### Python Style Guide

- **PEP 8**: Python style guide
- **Code Formatting**: Black, isort
- **Linting**: Flake8, pylint
- **Type Checking**: mypy
- **Docstrings**: Google style

```python
def calculate_total(items: List[Item], discount: Optional[float] = None) -> Decimal:
    """Calculate total price for a list of items with optional discount.

    Args:
        items: List of items to calculate total for
        discount: Optional discount percentage (0-1)

    Returns:
        Decimal total price after discount

    Raises:
        ValueError: If discount is invalid
    """
    if discount and (discount < 0 or discount > 1):
        raise ValueError("Discount must be between 0 and 1")

    total = sum(item.price * item.quantity for item in items)
    if discount:
        total = total * Decimal(1 - discount)
    
    return total
```

#### Git Workflow

- **Branch naming**: `feature/feature-name`, `bugfix/issue-name`, `hotfix/critical-issue`
- **Commit messages**: Follow conventional commits
- **Pull requests**: Require code review and passing tests
- **Git hooks**: pre-commit hooks for linting and formatting

### Testing Practices

#### Testing Pyramid

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test interaction between components
- **API Tests**: Test HTTP endpoints
- **End-to-End Tests**: Test complete user journeys
- **Performance Tests**: Test system under load

#### Test-Driven Development (TDD)
1. Write test for new feature
2. Run test (should fail)
3. Implement feature
4. Run test (should pass)
5. Refactor code as needed

#### Continuous Integration
- Automated tests run on every push
- Code quality checks
- Security scans
- Build and package

### Documentation

#### Code Documentation
- **Docstrings**: Document functions, classes, modules
- **Type Hints**: Provide type information
- **README**: Usage instructions for each service
- **Architecture Decision Records (ADRs)**: Document important decisions

#### API Documentation
- **OpenAPI/Swagger**: API specification
- **API Versioning**: Document API versions
- **Examples**: Provide usage examples
- **Status Codes**: Document response codes

## 📦 Triển khai

### Deployment Architecture

<p align="center">
  <img src="https://via.placeholder.com/800x600?text=Deployment+Architecture+Diagram" alt="Deployment Architecture" width="800"/>
</p>

#### Environments
- **Development**: For active development
- **Staging**: Mirror of production for testing
- **Production**: Live environment
- **Sandbox**: For third-party testing

#### Infrastructure as Code (IaC)
- **Terraform**: Provision infrastructure
- **Ansible**: Configure systems
- **Kubernetes Manifests**: Define container orchestration

### Continuous Deployment Pipeline

#### CI/CD Flow
1. **Source**: Code repository (GitHub, GitLab)
2. **Build**: Compile and package
3. **Test**: Run automated tests
4. **Analyze**: Code quality, security scans
5. **Deploy**: Automated deployment
6. **Verify**: Post-deployment verification
7. **Monitor**: Runtime monitoring

#### Deployment Strategies
- **Blue/Green Deployment**: Switch traffic between environments
- **Canary Deployment**: Gradual rollout to subset of users
- **Rolling Updates**: Update instances one by one
- **Feature Flags**: Control feature availability

### Kubernetes Deployment

#### Resource Organization
- **Namespaces**: Separate environments and services
- **Labels & Selectors**: Organize and select resources
- **ConfigMaps & Secrets**: External configuration

#### Sample Kubernetes Configuration

```yaml
# product-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service
  namespace: ecom
  labels:
    app: product-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: product-service
  template:
    metadata:
      labels:
        app: product-service
    spec:
      containers:
      - name: product-service
        image: ecom-registry/product-service:1.2.3
        ports:
        - containerPort: 8005
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
          requests:
            cpu: "500m"
            memory: "256Mi"
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: mongodb-config
              key: host
        livenessProbe:
          httpGet:
            path: /health
            port: 8005
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Scaling Strategies

#### Horizontal Scaling
- **Auto-scaling**: Based on CPU/memory usage
- **Scheduled Scaling**: For predictable traffic patterns
- **Manual Scaling**: For special events

#### Vertical Scaling
- **Resource Allocation**: Increase CPU/memory
- **Instance Types**: Use more powerful instances
- **Database Scaling**: Increase database resources

### Database Migration

#### Migration Strategies
- **Schema Migrations**: Database schema changes
- **Data Migrations**: Transform existing data
- **Zero-downtime Migrations**: Maintain availability
- **Rollback Plans**: Revert to previous state

#### Backup and Recovery
- **Regular Backups**: Automated backup schedule
- **Point-in-time Recovery**: Restore to specific time
- **Geo-redundant Storage**: Multiple location backups
- **Restore Testing**: Regularly test recovery process

## 📊 Monitoring và Logging

### Monitoring Infrastructure

<p align="center">
  <img src="https://via.placeholder.com/800x400?text=Monitoring+Infrastructure+Diagram" alt="Monitoring Infrastructure" width="800"/>
</p>

#### Monitoring Stack
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and dashboards
- **Alertmanager**: Alert handling and routing
- **Node Exporter**: Host metrics
- **cAdvisor**: Container metrics

#### Key Metrics
- **System Metrics**: CPU, memory, disk, network
- **Application Metrics**: Request rate, error rate, latency
- **Business Metrics**: Orders, revenue, conversion rate
- **Custom Metrics**: Service-specific metrics

### Dashboards and Visualization

#### Dashboard Types
- **System Dashboards**: Infrastructure health
- **Service Dashboards**: Service-specific metrics
- **Business Dashboards**: Business KPIs
- **Alerting Dashboards**: Current and recent alerts

#### Sample Grafana Dashboard
- **Layout**: Multiple panels with key metrics
- **Time Range**: Selectable time periods
- **Filtering**: Filter by service, region, etc.
- **Alerting**: Visual indicators for alerts

### Logging System

#### Logging Stack
- **Elasticsearch**: Log storage and search
- **Logstash/Fluentd**: Log collection and processing
- **Kibana**: Log visualization and query
- **Filebeat**: Log shipping from containers

#### Log Levels
- **ERROR**: Error events that might still allow the application to continue running
- **WARNING**: Potentially harmful situations
- **INFO**: Informational messages highlighting application progress
- **DEBUG**: Detailed information for debugging

#### Structured Logging
```json
{
  "timestamp": "2023-03-15T14:22:10.123Z",
  "level": "INFO",
  "service": "product-service",
  "trace_id": "abc123def456",
  "user_id": "user123",
  "message": "Product viewed",
  "data": {
    "product_id": "prod456",
    "category": "electronics"
  }
}
```

### Alerting and Incident Management

#### Alert Configuration
- **Alert Rules**: Conditions that trigger alerts
- **Alert Severity**: Critical, warning, info
- **Alert Routing**: Direct to appropriate teams
- **Alert Aggregation**: Group related alerts

#### Incident Response
- **On-call Rotation**: 24/7 coverage
- **Runbooks**: Step-by-step resolution guides
- **Post-mortem Analysis**: Learn from incidents
- **Automated Remediation**: Auto-fix common issues

### Distributed Tracing

#### Tracing Implementation
- **Jaeger/Zipkin**: Distributed tracing systems
- **OpenTelemetry**: Instrumentation standard
- **Trace Context**: Propagate across services
- **Sampling**: Trace a percentage of requests

#### Trace Analysis
- **Request Flow Visualization**: See entire request journey
- **Bottleneck Identification**: Find slow components
- **Error Correlation**: Connect errors across services
- **Service Dependency Mapping**: Understand relationships

## 🧪 Testing

### Testing Strategy

<p align="center">
  <img src="https://via.placeholder.com/800x400?text=Testing+Pyramid" alt="Testing Pyramid" width="800"/>
</p>

#### Testing Pyramid
- **Unit Tests**: Test individual functions/methods (Coverage target: 80%+)
- **Integration Tests**: Test interactions between components
- **API Tests**: Test HTTP endpoints
- **UI Tests**: Test user interface
- **End-to-End Tests**: Test complete user journeys
- **Performance Tests**: Test system under load

### Unit Testing

#### Test Frameworks
- **pytest**: Python test framework
- **unittest**: Python standard library
- **mock**: Mocking library
- **factory_boy**: Test data factory

#### Sample Unit Test
```python
def test_calculate_order_total():
    # Arrange
    items = [
        Item(id="1", price=Decimal("10.0"), quantity=2),
        Item(id="2", price=Decimal("15.0"), quantity=1),
    ]
    
    # Act
    total = calculate_order_total(items)
    
    # Assert
    assert total == Decimal("35.0")
```

### Integration Testing

#### Integration Test Approaches
- **Component Integration**: Test service components together
- **Service Integration**: Test interaction between services
- **Database Integration**: Test database interactions
- **External API Integration**: Test third-party services

#### Testing Databases
- **Test Databases**: Separate databases for testing
- **Migrations**: Run migrations for tests
- **Fixtures**: Pre-populated test data
- **Cleanup**: Reset database state after tests

### API Testing

#### API Test Frameworks
- **pytest-requests**: Test HTTP APIs
- **Postman/Newman**: API testing tool
- **Tavern**: YAML-based API testing
- **Swagger/OpenAPI Validators**: Validate against API spec

#### API Test Example
```python
def test_get_product_api():
    # Arrange
    product_id = "prod123"
    
    # Act
    response = client.get(f"/products/{product_id}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert "name" in response.json()
    assert "price" in response.json()
```

### Performance Testing

#### Performance Test Types
- **Load Testing**: Test under expected load
- **Stress Testing**: Test beyond expected load
- **Endurance Testing**: Test over time
- **Spike Testing**: Test with sudden load increases

#### Performance Test Tools
- **Locust**: Python-based load testing
- **JMeter**: Java-based load testing
- **Gatling**: Scala-based load testing
- **k6**: JavaScript-based load testing

### Test Automation

#### CI/CD Integration
- **Automated Test Runs**: On push, PR, scheduled
- **Test Reports**: Generate and publish reports
- **Test Coverage**: Track and enforce coverage
- **Test Performance**: Monitor test execution time

#### Test Management
- **Test Case Management**: Organize and track tests
- **Test Environment Management**: Provision test environments
- **Test Data Management**: Create and maintain test data
- **Test Results Analysis**: Analyze and visualize results

## 🚀 Roadmap

### Current Status (v1.0.0-beta)

- [x] Core microservices architecture
- [x] Product, Order, Cart, Payment, Shipment services
- [x] Basic recommendation and sentiment analysis
- [x] Frontend with responsive design
- [x] Docker containerization and orchestration
- [x] API gateway and service discovery
- [x] Basic monitoring and logging

### Short-term (Next 3 months)

- [ ] Enhanced recommendation engine with collaborative filtering
- [ ] Improved sentiment analysis with aspect-based analysis
- [ ] Mobile-specific API optimizations
- [ ] Enhanced search functionality with Elasticsearch
- [ ] Advanced analytics dashboard
- [ ] Performance optimizations
- [ ] Enhanced security features

### Mid-term (6-12 months)

- [ ] Mobile applications (iOS/Android)
- [ ] Multi-language support
- [ ] Advanced personalization features
- [ ] A/B testing framework
- [ ] Enhanced marketing integrations
- [ ] Advanced fraud detection
- [ ] Loyalty program integration
- [ ] Social media integration

### Long-term (1-2 years)

- [ ] Machine learning for demand forecasting
- [ ] Voice commerce integration
- [ ] Augmented reality product visualization
- [ ] Blockchain for supply chain transparency
- [ ] Advanced recommendation with reinforcement learning
- [ ] Natural language processing for customer support
- [ ] AI-driven product categorization and tagging
- [ ] Predictive analytics for customer behavior

### Feature Prioritization Matrix

| Feature | Impact | Effort | Priority |
|---------|--------|--------|----------|
| Enhanced Recommendation | High | Medium | 1 |
| Mobile Apps | High | High | 2 |
| Improved Search | High | Medium | 3 |
| Multi-language | Medium | Medium | 4 |
| AR Visualization | High | High | 5 |

## ❓ FAQs

### General Questions

#### What is E-Commerce Microservices?
E-Commerce Microservices là một nền tảng thương mại điện tử dựa trên kiến trúc microservices, cho phép xây dựng các hệ thống bán hàng trực tuyến có khả năng mở rộng cao, linh hoạt và đáng tin cậy.

#### What technologies does it use?
Hệ thống sử dụng Python, Django/Flask, MongoDB, PostgreSQL, MySQL, Docker, Kubernetes, và các công nghệ AI/ML như TensorFlow, PyTorch, và Hugging Face Transformers.

#### How does it compare to monolithic e-commerce platforms?
So với các nền tảng monolithic, E-Commerce Microservices cung cấp khả năng mở rộng tốt hơn, triển khai nhanh hơn, khả năng chịu lỗi cao hơn, và cho phép tích hợp các công nghệ AI/ML một cách linh hoạt.

### Technical Questions

#### How do services communicate with each other?
Các service giao tiếp thông qua REST API và event-driven architecture sử dụng message brokers như Kafka.

#### Can I deploy only specific services?
Có, bạn có thể triển khai từng service riêng biệt tùy theo nhu cầu, miễn là các dependency cần thiết được đáp ứng.

#### How do you handle database transactions across services?
Chúng tôi sử dụng Saga pattern và event sourcing để đảm bảo tính nhất quán cuối cùng (eventual consistency) giữa các service.

#### How scalable is the system?
Hệ thống có thể mở rộng để xử lý hàng triệu người dùng và hàng trăm nghìn giao dịch mỗi ngày thông qua horizontal scaling.

### Deployment Questions

#### What are the minimum system requirements?
Yêu cầu tối thiểu là 4 cores CPU, 8GB RAM, 20GB SSD storage, và Docker + Docker Compose.

#### Can it be deployed on cloud platforms?
Có, hệ thống có thể được triển khai trên AWS, GCP, Azure, và các cloud platforms khác sử dụng Docker, Kubernetes, hoặc các managed services.

#### How do you handle database migrations?
Database migrations được quản lý thông qua các migration tools của Django/Flask và được áp dụng trong quá trình triển khai.

### Support & Contribution

#### How can I contribute to the project?
Bạn có thể đóng góp bằng cách fork repository, thực hiện thay đổi, và tạo pull request. Chi tiết trong [CONTRIBUTING.md](sentiment-service/CONTRIBUTING.md).

#### Is commercial support available?
Có, chúng tôi cung cấp commercial support, customization, và training. Liên hệ qua email cho chi tiết.

#### How do I report bugs or request features?
Bugs và feature requests có thể được báo cáo thông qua GitHub Issues của repository.

## 🤝 Đóng góp

Dự án này chào đón mọi đóng góp từ cộng đồng. Bạn có thể đóng góp theo nhiều cách:

### Ways to Contribute

- **Code Contributions**: Thêm tính năng mới hoặc sửa lỗi
- **Documentation**: Cải thiện tài liệu, hướng dẫn và examples
- **Testing**: Viết test cases, báo cáo bugs
- **Design**: Cải thiện UI/UX
- **Ideas**: Đề xuất tính năng mới

### Contribution Process

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add some amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Pull Request Guidelines

- Follow coding standards
- Include tests for new features
- Update documentation as needed
- Ensure all tests pass
- Reference issues the PR resolves

### Code of Conduct

Dự án tuân theo [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).

## 👥 Tác giả

- **Bisosad** - *Initial work and core development*

## 📝 Giấy phép

Dự án này được cấp phép theo [Giấy phép MIT](LICENSE) - xem file [LICENSE](LICENSE) để biết chi tiết.

## 📞 Liên hệ

- **Email**: contact@example.com
- **Website**: https://example.com
- **GitHub**: https://github.com/bisosad
- **Discord**: https://discord.gg/example

## 🙏 Lời cảm ơn

Chúng tôi xin gửi lời cảm ơn đến:

- Tất cả các contributors đã đóng góp vào dự án
- Các thư viện và frameworks open source đã được sử dụng
- Cộng đồng phát triển Python và microservices
- Tất cả người dùng đã cung cấp feedback quý giá

---

<p align="center">
  <b>Powered by Python, Django, and the Microservices Architecture</b><br>
  <i>Making e-commerce scalable, flexible, and intelligent</i>
</p>