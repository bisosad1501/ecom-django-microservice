# CHAPTER 1: REQUIREMENTS OF E-COMMERCE

## 1.1 Determine Requirements

Xác định yêu cầu là bước đầu tiên và có tính quyết định trong việc phát triển hệ thống thương mại điện tử. Quá trình này đòi hỏi sự phân tích kỹ lưỡng để đảm bảo hệ thống cuối cùng đáp ứng được cả mục tiêu kinh doanh và nhu cầu của người dùng.

### Quy trình xác định yêu cầu

1. **Thu thập thông tin**
   - Phỏng vấn các bên liên quan (stakeholders)
   - Khảo sát thị trường và đối tượng khách hàng mục tiêu
   - Nghiên cứu các hệ thống tương tự
   - Phân tích quy trình kinh doanh hiện tại

2. **Phân tích thông tin**
   - Phân loại yêu cầu thành các nhóm (chức năng, phi chức năng)
   - Đánh giá tính khả thi và ưu tiên
   - Xác định các ràng buộc (thời gian, ngân sách, công nghệ)
   - Giải quyết xung đột giữa các yêu cầu

3. **Tài liệu hóa**
   - Tạo tài liệu đặc tả yêu cầu (SRS - Software Requirements Specification)
   - Xây dựng các use cases và user stories
   - Thiết kế wireframes và prototypes
   - Xác định các chỉ số đo lường hiệu suất (KPIs)

4. **Xác nhận và kiểm tra**
   - Đánh giá với các bên liên quan
   - Kiểm tra tính đầy đủ và nhất quán
   - Quản lý thay đổi yêu cầu
   - Theo dõi trạng thái yêu cầu

### Các loại yêu cầu

1. **Yêu cầu chức năng (Functional Requirements)**
   - Mô tả các chức năng cụ thể mà hệ thống phải thực hiện
   - Xác định hành vi của hệ thống trong các tình huống cụ thể
   - Ví dụ: xử lý đơn hàng, quản lý tài khoản, thanh toán trực tuyến

2. **Yêu cầu phi chức năng (Non-functional Requirements)**
   - Hiệu suất: thời gian phản hồi, throughput, tài nguyên sử dụng
   - Bảo mật: xác thực, phân quyền, mã hóa dữ liệu
   - Khả năng mở rộng: hỗ trợ tăng trưởng người dùng, dữ liệu
   - Khả năng sử dụng: giao diện thân thiện, dễ học, dễ sử dụng
   - Độ tin cậy: khả năng phục hồi, tần suất lỗi
   - Tính sẵn sàng: uptime, thời gian downtime

3. **Yêu cầu nghiệp vụ (Business Requirements)**
   - Mục tiêu tổng thể của doanh nghiệp
   - Các KPI cần đạt được
   - Quy trình kinh doanh cần hỗ trợ

4. **Yêu cầu kỹ thuật (Technical Requirements)**
   - Công nghệ sử dụng
   - Kiến trúc hệ thống
   - Tiêu chuẩn coding và thiết kế
   - Tích hợp với hệ thống hiện có

### 1.1.1 Actors

Actors là các thực thể bên ngoài tương tác với hệ thống thương mại điện tử. Họ có thể là con người, hệ thống khác hoặc thiết bị ngoại vi. Việc xác định chính xác các actors và vai trò của họ là nền tảng để xây dựng use cases và yêu cầu chức năng của hệ thống.

#### Phân loại Actors trong hệ thống thương mại điện tử microservices

1. **Actors chính (Primary Actors)**
   - Actors trực tiếp sử dụng hệ thống để đạt mục tiêu của họ
   - Khởi tạo các use cases chính của hệ thống
   - Ví dụ: Khách hàng, Quản trị viên, Người bán

2. **Actors phụ (Secondary Actors)**
   - Actors hỗ trợ hệ thống hoàn thành các use cases
   - Thường là các hệ thống bên ngoài hoặc dịch vụ
   - Ví dụ: Hệ thống thanh toán, Dịch vụ vận chuyển, Hệ thống email

3. **Actors kỹ thuật (Technical Actors)**
   - Actors tương tác với các dịch vụ kỹ thuật nội bộ
   - Thường không nhìn thấy đối với người dùng cuối
   - Ví dụ: Dịch vụ phân tích cảm xúc, Dịch vụ gợi ý, Dịch vụ cache

#### Actors chính trong hệ thống thương mại điện tử microservices

1. **Khách hàng không đăng ký (Guest Customer)**
   - **Mô tả**: Người dùng truy cập hệ thống mà không đăng nhập
   - **Tương tác với microservices**:
     - Product Service: Xem thông tin sản phẩm, tìm kiếm, so sánh
     - Book Service: Xem thông tin sách, tìm kiếm, so sánh
     - Shoe Service: Xem thông tin giày, tìm kiếm, so sánh
     - Cart Service: Thêm sản phẩm vào giỏ hàng tạm thời (lưu trong session/cookie)
     - Auth Service: Đăng ký tài khoản mới
     - Review Service: Xem đánh giá sản phẩm
   - **Quyền hạn**:
     - Duyệt danh mục sản phẩm (sách, giày...)
     - Xem thông tin chi tiết sản phẩm
     - Tìm kiếm sản phẩm
     - Xem đánh giá và xếp hạng
     - Thêm sản phẩm vào giỏ hàng tạm thời
     - Đăng ký tài khoản mới
   - **Hạn chế**:
     - Không thể hoàn tất đơn hàng
     - Không thể lưu thông tin cá nhân
     - Không thể theo dõi đơn hàng
     - Không thể viết đánh giá sản phẩm
   - **Luồng dữ liệu**: Session ID → API Gateway → Microservice tương ứng

2. **Khách hàng đã đăng ký (Registered Customer)**
   - **Mô tả**: Người dùng đã đăng ký và đăng nhập vào hệ thống với vai trò CUSTOMER
   - **Phân loại khách hàng**:
     - Khách hàng Đồng (Bronze)
     - Khách hàng Bạc (Silver) 
     - Khách hàng Vàng (Gold)
     - Khách hàng Bạch Kim (Platinum)
   - **Tương tác với microservices**:
     - Auth Service: Đăng nhập, quản lý thông tin tài khoản
     - Customer Service: Quản lý thông tin cá nhân, địa chỉ
     - Product Service: Xem thông tin sản phẩm, tìm kiếm
     - Book Service: Xem thông tin và mua sách
     - Shoe Service: Xem thông tin và mua giày
     - Cart Service: Quản lý giỏ hàng
     - Order Service: Đặt hàng, xem lịch sử đơn hàng
     - Payment Service: Thanh toán, quản lý phương thức thanh toán
     - Shipment Service: Theo dõi đơn hàng
     - Review Service: Viết và quản lý đánh giá
     - Recommendation Service: Nhận gợi ý sản phẩm cá nhân hóa
   - **Quyền hạn**:
     - Tất cả quyền của khách không đăng ký
     - Quản lý thông tin cá nhân và địa chỉ
     - Quản lý phương thức thanh toán
     - Xem lịch sử đơn hàng
     - Theo dõi trạng thái đơn hàng
     - Hoàn tất quy trình đặt hàng
     - Viết đánh giá sản phẩm
     - Lưu sản phẩm vào danh sách yêu thích
     - Nhận thông báo và khuyến mãi cá nhân hóa
     - Tích lũy và sử dụng điểm thưởng (loyalty points)
     - Nhận các đặc quyền theo cấp độ khách hàng
   - **Hạn chế**:
     - Không thể truy cập tính năng quản trị
     - Không thể quản lý sản phẩm và người dùng khác
   - **Luồng dữ liệu**: JWT Token → API Gateway → Auth Service (xác thực) → Microservice tương ứng

3. **Người bán (Seller)**
   - **Mô tả**: Người dùng đã đăng ký và được cấp quyền SELLER trong hệ thống
   - **Tương tác với microservices**:
     - Auth Service: Đăng nhập hệ thống, quản lý tài khoản
     - Customer Service: Quản lý thông tin người bán
     - Product Service: Quản lý danh mục và sản phẩm
     - Book Service: Quản lý sách (nếu kinh doanh sách)
     - Shoe Service: Quản lý giày (nếu kinh doanh giày)
     - Order Service: Quản lý đơn hàng của cửa hàng
     - Payment Service: Xem báo cáo thanh toán
     - Shipment Service: Quản lý vận chuyển
   - **Quyền hạn**:
     - Quản lý thông tin cửa hàng
     - Thêm, sửa, xóa sản phẩm
     - Quản lý danh mục sản phẩm 
     - Quản lý tồn kho
     - Xử lý đơn hàng từ khách hàng
     - Xem báo cáo doanh số
     - Trả lời đánh giá của khách hàng
   - **Hạn chế**:
     - Không thể truy cập tính năng quản trị hệ thống
     - Chỉ quản lý được sản phẩm của cửa hàng mình
   - **Luồng dữ liệu**: Seller JWT Token → API Gateway → Auth Service (xác thực + phân quyền) → Microservice tương ứng

4. **Quản trị viên (Administrator)**
   - **Mô tả**: Người quản lý hệ thống với quyền ADMIN
   - **Tương tác với microservices**:
     - Auth Service: Quản lý người dùng và phân quyền
     - Customer Service: Quản lý thông tin khách hàng
     - Product Service: Quản lý danh mục và sản phẩm toàn hệ thống
     - Book Service: Quản lý sách toàn hệ thống
     - Shoe Service: Quản lý giày toàn hệ thống 
     - Order Service: Quản lý đơn hàng toàn hệ thống
     - Payment Service: Xem báo cáo thanh toán
     - Shipment Service: Quản lý vận chuyển
     - Review Service: Quản lý đánh giá
     - Recommendation Service: Cấu hình hệ thống gợi ý
     - Sentiment Service: Xem báo cáo phân tích cảm xúc
   - **Quyền hạn**:
     - Quản lý người dùng (tạo, sửa, xóa, phân quyền)
     - Quản lý danh mục sản phẩm (sách, giày...)
     - Quản lý sản phẩm (thêm, sửa, xóa)
     - Quản lý đơn hàng (xem, cập nhật trạng thái, hủy)
     - Quản lý khuyến mãi và mã giảm giá
     - Xem báo cáo và thống kê
     - Cấu hình hệ thống
     - Quản lý nội dung (banner, trang tĩnh, blog)
     - Phê duyệt yêu cầu đăng ký người bán
   - **Hạn chế**:
     - Giới hạn bởi chính sách và quy định của doanh nghiệp
   - **Luồng dữ liệu**: Admin JWT Token → API Gateway → Auth Service (xác thực + phân quyền) → Microservice tương ứng

5. **Đối tác thanh toán (Payment Gateway)**
   - **Mô tả**: Cổng thanh toán xử lý giao dịch
   - **Tương tác với microservices**:
     - Payment Service: Xử lý giao dịch, thông báo kết quả
   - **Quyền hạn**:
     - Nhận và xử lý thông tin thanh toán
     - Xác thực giao dịch
     - Thông báo kết quả thanh toán
   - **Hạn chế**:
     - Chỉ truy cập thông tin cần thiết cho việc thanh toán
     - Tuân thủ các tiêu chuẩn bảo mật (PCI DSS)
   - **Luồng dữ liệu**: API Key/Webhook → API Gateway → Payment Service

6. **Đối tác vận chuyển (Shipping Partner)**
   - **Mô tả**: Đơn vị vận chuyển đơn hàng đến khách hàng
   - **Tương tác với microservices**:
     - Shipment Service: Nhận thông tin vận chuyển, cập nhật trạng thái
   - **Quyền hạn**:
     - Nhận thông tin đơn hàng cần giao
     - Cập nhật trạng thái vận chuyển
     - Xác nhận giao hàng thành công/thất bại
   - **Hạn chế**:
     - Chỉ truy cập thông tin cần thiết cho việc giao hàng
     - Không thể thay đổi thông tin đơn hàng
   - **Luồng dữ liệu**: API Key → API Gateway → Shipment Service

7. **Dịch vụ phân tích cảm xúc (Sentiment Analysis Service)**
   - **Mô tả**: Hệ thống phân tích cảm xúc từ đánh giá của khách hàng
   - **Tương tác với microservices**:
     - Review Service: Lấy dữ liệu đánh giá để phân tích
   - **Quyền hạn**:
     - Truy cập dữ liệu đánh giá
     - Phân tích cảm xúc từ đánh giá
     - Cung cấp báo cáo phân tích
   - **Hạn chế**:
     - Chỉ đọc dữ liệu, không thay đổi
   - **Luồng dữ liệu**: Internal API → Review Service → Sentiment Service

8. **Dịch vụ gợi ý (Recommendation Service)**
   - **Mô tả**: Hệ thống cung cấp gợi ý sản phẩm dựa trên hành vi người dùng
   - **Tương tác với microservices**:
     - Product Service: Lấy thông tin sản phẩm
     - Book Service: Lấy thông tin sách
     - Shoe Service: Lấy thông tin giày
     - Review Service: Lấy dữ liệu đánh giá
     - Sentiment Service: Lấy kết quả phân tích cảm xúc
   - **Quyền hạn**:
     - Truy cập dữ liệu sản phẩm
     - Truy cập dữ liệu người dùng
     - Tạo và cung cấp gợi ý sản phẩm
   - **Hạn chế**:
     - Chỉ đọc dữ liệu, không thay đổi
   - **Luồng dữ liệu**: Internal API → Microservices liên quan → Recommendation Service

#### Mối quan hệ giữa Actors và Microservices

| Actor | Microservices | Tương tác chính |
|-------|---------------|-----------------|
| Guest Customer | Product Service, Book Service, Shoe Service, Cart Service, Review Service | Xem sản phẩm, thêm vào giỏ hàng tạm thời |
| Registered Customer | Product Service, Book Service, Shoe Service, Cart Service, Order Service, Payment Service, Shipment Service, Review Service, Recommendation Service | Mua sắm, thanh toán, theo dõi đơn hàng, đánh giá |
| Seller | Product Service, Book Service, Shoe Service, Order Service, Shipment Service | Quản lý sản phẩm, xử lý đơn hàng, quản lý tồn kho |
| Administrator | Tất cả microservices | Quản lý hệ thống, người dùng, cấu hình |
| Payment Gateway | Payment Service | Xử lý giao dịch, thông báo kết quả |
| Shipping Partner | Shipment Service | Nhận và cập nhật thông tin vận chuyển |
| Sentiment Analysis Service | Review Service | Phân tích cảm xúc từ đánh giá |
| Recommendation Service | Product Service, Book Service, Shoe Service, Review Service, Sentiment Service | Tạo gợi ý sản phẩm |

#### Ảnh hưởng của kiến trúc microservices đến Actors

1. **Phân chia trách nhiệm rõ ràng**
   - Mỗi actor tương tác với các microservices cụ thể
   - Giảm sự phụ thuộc và tăng tính module hóa

2. **Xác thực và phân quyền phức tạp hơn**
   - Cần cơ chế xác thực tập trung (JWT, OAuth2)
   - Phân quyền theo từng microservice

3. **Quản lý phiên và trạng thái**
   - Thách thức trong việc duy trì trạng thái xuyên suốt các microservices
   - Sử dụng cache phân tán, message broker

4. **Tương tác không đồng bộ**
   - Các actor cần xử lý phản hồi không đồng bộ
   - Sử dụng webhook, event sourcing, message queue

5. **Tính nhất quán dữ liệu**
   - Đảm bảo actor thấy dữ liệu nhất quán giữa các microservices
   - Sử dụng saga pattern, event sourcing

#### Tác động của Actors đến thiết kế API

1. **API Gateway**
   - Điểm vào duy nhất cho tất cả actors
   - Xử lý authentication, rate limiting, routing

2. **Backend for Frontend (BFF)**
   - API được tối ưu hóa cho từng loại actor
   - Ví dụ: BFF cho mobile, BFF cho web, BFF cho admin

3. **CQRS (Command Query Responsibility Segregation)**
   - Tách biệt đọc và ghi để tối ưu hóa trải nghiệm cho từng actor
   - Actors như Admin cần view phức tạp, trong khi Customer cần update nhanh

4. **Event-Driven APIs**
   - Actors nhận thông báo về các sự kiện quan trọng
   - Ví dụ: webhook cho Payment Gateway, real-time update cho Customer

5. **Versioning API**
   - Hỗ trợ nhiều phiên bản API cho các actors khác nhau
   - Đảm bảo khả năng tương thích ngược

#### Tương tác giữa Actors và Business Processes

1. **Quy trình đặt hàng**
   - Actors: Customer → Order Service → Payment Gateway → Warehouse Staff → Shipping Partner
   - Business Process: Tạo đơn hàng → Thanh toán → Xử lý đơn hàng → Giao hàng

2. **Quy trình hoàn tiền**
   - Actors: Customer → Sales Staff → Payment Gateway
   - Business Process: Yêu cầu hoàn tiền → Xét duyệt → Xử lý hoàn tiền

3. **Quy trình quản lý sản phẩm**
   - Actors: Administrator → Warehouse Staff
   - Business Process: Thêm sản phẩm → Cập nhật tồn kho → Điều chỉnh giá

4. **Quy trình gợi ý sản phẩm**
   - Actors: Customer → ML Service → Product Service
   - Business Process: Hành vi người dùng → Phân tích → Gợi ý sản phẩm

#### Yêu cầu phi chức năng liên quan đến Actors

1. **Hiệu suất (Performance)**
   - Customer: Thời gian tải trang < 2 giây
   - Payment Gateway: Xử lý giao dịch < 5 giây
   - Administrator: Tải báo cáo < 10 giây

2. **Tính sẵn sàng (Availability)**
   - Customer-facing services: 99.99% uptime
   - Internal-facing services: 99.9% uptime
   - Scheduled maintenance: 2-4 giờ/tháng

3. **Bảo mật (Security)**
   - Customer: HTTPS, mã hóa password, session timeout
   - Administrator: Xác thực 2 yếu tố, IP whitelisting
   - Payment Gateway: Tuân thủ PCI DSS, mã hóa đầu-cuối

4. **Khả năng mở rộng (Scalability)**
   - Xử lý 1000+ Customer đồng thời
   - Hỗ trợ tăng trưởng 20% mỗi quý
   - Auto-scaling dựa trên tải

#### Tài liệu hóa yêu cầu Actor

1. **User Stories**
   - Format: "Là [Actor], tôi muốn [hành động] để [mục tiêu/lợi ích]"
   - Ví dụ: "Là Registered Customer, tôi muốn theo dõi đơn hàng để biết khi nào hàng sẽ được giao"

2. **Use Case Diagram**
   - Biểu diễn mối quan hệ giữa actors và các use case
   - Giúp hiểu tổng quan về chức năng hệ thống

3. **Activity Diagram**
   - Mô tả quy trình đi qua nhiều actors và microservices
   - Xác định các điểm quyết định và xử lý lỗi

4. **User Interface Mockups**
   - Giao diện cụ thể cho từng actor
   - Wireframes và prototypes tương tác

5. **API Documentation**
   - OpenAPI/Swagger spec cho từng microservice
   - Mô tả endpoints, parameters, responses

#### Kết luận

Việc xác định và phân tích chi tiết các actors trong hệ thống thương mại điện tử microservices là bước đầu tiên và quan trọng nhất trong quá trình phát triển. Hiểu rõ các actors giúp chúng ta:

- Thiết kế kiến trúc microservices phù hợp
- Xác định và ưu tiên các yêu cầu chức năng
- Tối ưu hóa trải nghiệm người dùng cho từng đối tượng
- Xây dựng hệ thống bảo mật và có khả năng mở rộng
- Đảm bảo tính nhất quán trong trải nghiệm xuyên suốt hệ thống

Các microservices của dự án (Product, Order, Payment, Shipment, v.v.) đã được thiết kế để phục vụ các actors khác nhau với các nhu cầu cụ thể, tạo nên một hệ thống linh hoạt, có khả năng mở rộng và dễ bảo trì.

### 1.1.2 Functions with respect to actors

Các chức năng (functions) trong hệ thống thương mại điện tử cần được xác định dựa trên nhu cầu và tương tác của các actors. Mỗi actor sẽ có một tập hợp các chức năng riêng để hỗ trợ họ đạt được mục tiêu khi tương tác với hệ thống.

#### Phân loại chức năng theo tương tác với actors

1. **Chức năng dành cho Khách hàng (Customer-Facing Functions)**
   - Tập trung vào trải nghiệm người dùng và quy trình mua sắm
   - Giao diện thân thiện, đơn giản, dễ sử dụng
   - Ví dụ: xem sản phẩm, đặt hàng, thanh toán

2. **Chức năng dành cho Quản trị (Administration Functions)**
   - Tập trung vào quản lý và vận hành hệ thống
   - Giao diện đầy đủ thông tin, tính năng chuyên sâu
   - Ví dụ: quản lý sản phẩm, báo cáo doanh thu, phân quyền người dùng

3. **Chức năng tích hợp hệ thống (Integration Functions)**
   - Tập trung vào giao tiếp với các hệ thống bên ngoài
   - Chuẩn hóa dữ liệu, xử lý không đồng bộ, bảo mật
   - Ví dụ: tích hợp thanh toán, vận chuyển, thông báo

4. **Chức năng kỹ thuật và hạ tầng (Technical & Infrastructure Functions)**
   - Tập trung vào vận hành và quản lý hệ thống
   - Hiệu suất, bảo mật, khả năng mở rộng
   - Ví dụ: monitoring, logging, authentication, caching

#### Chức năng chi tiết theo từng actor

##### 1. Guest Customer (Khách hàng không đăng ký)

| Function | Description | Microservice | Priority |
|----------|-------------|--------------|----------|
| **Duyệt sản phẩm** | Xem danh sách các sản phẩm theo danh mục, bộ lọc hoặc sắp xếp | Product Service | High |
| **Tìm kiếm sản phẩm** | Tìm sản phẩm theo từ khóa, có gợi ý tự động và bộ lọc nâng cao | Product Service, Search Service | High |
| **Xem chi tiết sản phẩm** | Xem thông tin chi tiết của sản phẩm, hình ảnh, mô tả, giá cả | Product Service | High |
| **Xem đánh giá sản phẩm** | Xem đánh giá và xếp hạng của khách hàng khác | Review Service | Medium |
| **Thêm vào giỏ hàng** | Thêm sản phẩm vào giỏ hàng tạm thời | Cart Service | High |
| **Đăng ký tài khoản** | Tạo tài khoản mới với thông tin cá nhân | Auth Service | High |
| **Kiểm tra tồn kho** | Xem tình trạng tồn kho của sản phẩm | Product Service | Medium |
| **Xem thông tin cửa hàng** | Xem thông tin liên hệ, chính sách, FAQ | Content Service | Low |

##### 2. Registered Customer (Khách hàng đã đăng ký)

| Function | Description | Microservice | Priority |
|----------|-------------|--------------|----------|
| **Đăng nhập** | Xác thực người dùng với username/password | Auth Service | High |
| **Quản lý thông tin cá nhân** | Cập nhật thông tin cá nhân, mật khẩu, ảnh đại diện | Customer Service | Medium |
| **Quản lý địa chỉ** | Thêm, sửa, xóa địa chỉ giao hàng | Customer Service | Medium |
| **Quản lý phương thức thanh toán** | Thêm, sửa, xóa thẻ tín dụng hoặc phương thức thanh toán | Payment Service | Medium |
| **Đặt hàng** | Hoàn tất quy trình đặt hàng với sản phẩm trong giỏ | Order Service | High |
| **Thanh toán** | Xử lý thanh toán cho đơn hàng | Payment Service | High |
| **Theo dõi đơn hàng** | Xem trạng thái và thông tin vận chuyển đơn hàng | Order Service, Shipment Service | High |
| **Xem lịch sử đơn hàng** | Xem tất cả đơn hàng đã đặt và chi tiết | Order Service | Medium |
| **Đánh giá sản phẩm** | Viết đánh giá và xếp hạng cho sản phẩm đã mua | Review Service | Medium |
| **Yêu cầu hoàn tiền/đổi trả** | Tạo yêu cầu hoàn tiền hoặc đổi trả sản phẩm | Order Service | Medium |
| **Lưu sản phẩm yêu thích** | Thêm sản phẩm vào danh sách yêu thích | Customer Service | Low |
| **Nhận thông báo** | Nhận email, push notification về đơn hàng, khuyến mãi | Notification Service | Low |
| **Sử dụng mã giảm giá** | Áp dụng mã giảm giá vào đơn hàng | Promotion Service | Medium |
| **Xem sản phẩm gợi ý** | Xem các sản phẩm được gợi ý dựa trên lịch sử mua hàng | ML Service, Product Service | Low |

##### 3. Administrator (Quản trị viên)

| Function | Description | Microservice | Priority |
|----------|-------------|--------------|----------|
| **Quản lý người dùng** | Tạo, sửa, xóa, phân quyền tài khoản người dùng | Auth Service | High |
| **Quản lý danh mục** | Tạo, sửa, xóa danh mục sản phẩm | Product Service | High |
| **Quản lý sản phẩm** | Thêm, sửa, xóa sản phẩm và thông tin chi tiết | Product Service | High |
| **Quản lý đơn hàng** | Xem, cập nhật trạng thái, hủy đơn hàng | Order Service | High |
| **Quản lý tồn kho** | Xem, cập nhật số lượng tồn kho sản phẩm | Product Service | High |
| **Quản lý khuyến mãi** | Tạo, sửa, xóa chương trình khuyến mãi, mã giảm giá | Promotion Service | Medium |
| **Xem báo cáo bán hàng** | Xem báo cáo doanh thu, sản phẩm bán chạy | Analytics Service | Medium |
| **Quản lý đánh giá** | Duyệt, xóa đánh giá của khách hàng | Review Service | Medium |
| **Cấu hình hệ thống** | Thay đổi cài đặt hệ thống, tham số kỹ thuật | Configuration Service | Medium |
| **Quản lý nội dung** | Thêm, sửa, xóa banner, trang tĩnh, blog | Content Service | Medium |
| **Quản lý vận chuyển** | Cấu hình phương thức vận chuyển, chi phí | Shipment Service | Medium |
| **Quản lý thanh toán** | Cấu hình phương thức thanh toán | Payment Service | Medium |
| **Xem log hệ thống** | Xem nhật ký hoạt động, lỗi hệ thống | Logging Service | Low |
| **Cấu hình ML** | Cấu hình các tham số cho hệ thống gợi ý | ML Service | Low |

##### 4. Sales Staff (Nhân viên bán hàng)

| Function | Description | Microservice | Priority |
|----------|-------------|--------------|----------|
| **Xem danh sách đơn hàng** | Xem tất cả đơn hàng và tìm kiếm | Order Service | High |
| **Xử lý đơn hàng** | Cập nhật trạng thái, ghi chú đơn hàng | Order Service | High |
| **Xem thông tin khách hàng** | Xem thông tin liên hệ, lịch sử mua hàng | Customer Service | High |
| **Tạo đơn hàng mới** | Tạo đơn hàng thay cho khách hàng | Order Service | Medium |
| **Xử lý hoàn tiền/đổi trả** | Xác nhận và xử lý yêu cầu hoàn tiền, đổi trả | Order Service, Payment Service | Medium |
| **Trả lời khách hàng** | Phản hồi câu hỏi, giải quyết vấn đề của khách | Support Service | Medium |
| **Áp dụng khuyến mãi** | Áp dụng khuyến mãi đặc biệt cho khách hàng | Promotion Service | Low |
| **Kiểm tra tồn kho** | Xem tình trạng tồn kho, kiểm tra sản phẩm | Product Service | Medium |

##### 5. Warehouse Staff (Nhân viên kho hàng)

| Function | Description | Microservice | Priority |
|----------|-------------|--------------|----------|
| **Xem đơn hàng cần xử lý** | Xem danh sách đơn hàng cần đóng gói, giao hàng | Order Service | High |
| **Cập nhật tồn kho** | Cập nhật số lượng tồn kho sản phẩm | Product Service | High |
| **Cập nhật trạng thái đơn hàng** | Đánh dấu đơn hàng đã đóng gói, sẵn sàng giao hàng | Order Service | High |
| **Tạo thông tin vận chuyển** | Tạo thông tin vận chuyển, in hóa đơn/phiếu giao hàng | Shipment Service | High |
| **Quản lý trả hàng** | Xử lý sản phẩm được trả lại | Order Service | Medium |
| **Kiểm kho** | Thực hiện kiểm kê kho định kỳ | Product Service | Medium |
| **Báo cáo sự cố** | Báo cáo vấn đề về sản phẩm, tồn kho | Support Service | Low |

##### 6. Shipping Partner (Đối tác vận chuyển)

| Function | Description | Microservice | Priority |
|----------|-------------|--------------|----------|
| **Nhận thông tin đơn hàng** | Lấy danh sách đơn hàng cần giao | Shipment Service | High |
| **Cập nhật trạng thái giao hàng** | Cập nhật thông tin vận chuyển (đang giao, đã giao) | Shipment Service | High |
| **Xác nhận giao hàng** | Xác nhận đơn hàng đã giao thành công | Shipment Service | High |
| **Báo cáo sự cố giao hàng** | Báo cáo khi không thể giao hàng | Shipment Service | Medium |
| **Truy xuất thông tin liên hệ** | Xem thông tin liên hệ của người nhận | Shipment Service | Medium |

##### 7. Payment Gateway (Cổng thanh toán)

| Function | Description | Microservice | Priority |
|----------|-------------|--------------|----------|
| **Xử lý thanh toán** | Xử lý giao dịch thanh toán từ khách hàng | Payment Service | High |
| **Xác thực giao dịch** | Xác thực tính hợp lệ của thông tin thanh toán | Payment Service | High |
| **Thông báo kết quả thanh toán** | Gửi thông báo kết quả giao dịch | Payment Service | High |
| **Xử lý hoàn tiền** | Hoàn tiền cho khách hàng khi được yêu cầu | Payment Service | Medium |
| **Tạo báo cáo giao dịch** | Cung cấp báo cáo về các giao dịch | Payment Service | Low |

#### Mối quan hệ giữa chức năng và microservices

Hệ thống thương mại điện tử microservices được thiết kế để phân chia các chức năng thành các dịch vụ nhỏ, độc lập. Mỗi microservice sẽ chịu trách nhiệm cho một tập hợp các chức năng cụ thể:

1. **API Gateway**
   - Định tuyến yêu cầu đến các microservices
   - Xác thực và phân quyền ban đầu
   - Xử lý rate limiting, caching
   - Tổng hợp dữ liệu từ nhiều microservices

2. **Auth Service**
   - Đăng ký, đăng nhập
   - Xác thực người dùng (JWT, OAuth)
   - Quản lý phiên làm việc
   - Phân quyền chi tiết

3. **Customer Service**
   - Quản lý thông tin cá nhân
   - Quản lý địa chỉ
   - Danh sách yêu thích
   - Lịch sử hoạt động

4. **Product Service**
   - Quản lý danh mục
   - Quản lý sản phẩm
   - Quản lý tồn kho
   - Thông tin giá cả

5. **Cart Service**
   - Thêm/xóa sản phẩm khỏi giỏ hàng
   - Cập nhật số lượng
   - Lưu trữ thông tin giỏ hàng
   - Kiểm tra tính hợp lệ của giỏ hàng

6. **Order Service**
   - Tạo đơn hàng
   - Quản lý trạng thái đơn hàng
   - Lịch sử đơn hàng
   - Xử lý đổi/trả

7. **Payment Service**
   - Tích hợp với cổng thanh toán
   - Xử lý thanh toán
   - Quản lý phương thức thanh toán
   - Xử lý hoàn tiền

8. **Shipment Service**
   - Tích hợp với đối tác vận chuyển
   - Theo dõi đơn hàng
   - Quản lý thông tin vận chuyển
   - Tính phí vận chuyển

9. **Review Service**
   - Quản lý đánh giá sản phẩm
   - Xếp hạng sản phẩm
   - Duyệt đánh giá
   - Thống kê đánh giá

10. **Promotion Service**
    - Quản lý khuyến mãi
    - Quản lý mã giảm giá
    - Áp dụng quy tắc khuyến mãi
    - Tích hợp với loyalty program

11. **ML Service**
    - Gợi ý sản phẩm
    - Phân tích hành vi
    - Dự đoán xu hướng
    - Phân tích giỏ hàng

12. **Notification Service**
    - Gửi email
    - Gửi push notification
    - Gửi SMS
    - Quản lý mẫu thông báo

#### Phân tích luồng chức năng chính

##### 1. Quy trình đặt hàng

1. **Duyệt và thêm sản phẩm vào giỏ hàng**
   - Actor: Guest/Registered Customer
   - Services: Product Service → Cart Service
   - Functions: Xem sản phẩm, Thêm vào giỏ hàng

2. **Đăng nhập hoặc đăng ký (nếu là khách)**
   - Actor: Guest Customer
   - Services: Auth Service → Customer Service
   - Functions: Đăng ký, Đăng nhập

3. **Tiến hành thanh toán**
   - Actor: Registered Customer
   - Services: Cart Service → Order Service → Payment Service
   - Functions: Checkout, Chọn địa chỉ giao hàng, Chọn phương thức thanh toán, Thanh toán

4. **Theo dõi đơn hàng**
   - Actor: Registered Customer
   - Services: Order Service → Shipment Service
   - Functions: Xem trạng thái đơn hàng, Theo dõi vận chuyển

5. **Đánh giá sản phẩm**
   - Actor: Registered Customer
   - Services: Order Service → Review Service
   - Functions: Viết đánh giá, Xếp hạng sản phẩm

##### 2. Quy trình quản lý sản phẩm

1. **Tạo/cập nhật danh mục**
   - Actor: Administrator
   - Services: Product Service
   - Functions: Quản lý danh mục

2. **Thêm/sửa/xóa sản phẩm**
   - Actor: Administrator
   - Services: Product Service
   - Functions: Quản lý sản phẩm, Upload hình ảnh

3. **Cập nhật tồn kho**
   - Actor: Administrator/Warehouse Staff
   - Services: Product Service
   - Functions: Quản lý tồn kho

4. **Tạo khuyến mãi cho sản phẩm**
   - Actor: Administrator
   - Services: Product Service → Promotion Service
   - Functions: Quản lý khuyến mãi

##### 3. Quy trình xử lý đơn hàng

1. **Xem đơn hàng mới**
   - Actor: Sales Staff
   - Services: Order Service
   - Functions: Xem danh sách đơn hàng

2. **Xác nhận đơn hàng**
   - Actor: Sales Staff
   - Services: Order Service → Notification Service
   - Functions: Xử lý đơn hàng, Gửi thông báo xác nhận

3. **Chuẩn bị đơn hàng**
   - Actor: Warehouse Staff
   - Services: Order Service → Product Service
   - Functions: Cập nhật tồn kho, Cập nhật trạng thái đơn hàng

4. **Tạo thông tin vận chuyển**
   - Actor: Warehouse Staff
   - Services: Order Service → Shipment Service
   - Functions: Tạo thông tin vận chuyển

5. **Giao hàng**
   - Actor: Shipping Partner
   - Services: Shipment Service → Notification Service
   - Functions: Cập nhật trạng thái giao hàng, Gửi thông báo

#### Kiến trúc chức năng trong Microservices

Việc phân chia chức năng trong kiến trúc microservices tuân theo một số nguyên tắc:

1. **Phân chia theo Domain (Domain-Driven Design)**
   - Mỗi microservice tập trung vào một domain nghiệp vụ cụ thể
   - Ví dụ: Product, Order, Payment là các bounded context riêng biệt

2. **Nguyên tắc "Single Responsibility"**
   - Mỗi microservice chỉ chịu trách nhiệm cho một nhóm chức năng liên quan
   - Tránh chồng chéo chức năng giữa các service

3. **API Design**
   - RESTful API cho các tương tác đồng bộ
   - Event-driven cho các tương tác không đồng bộ
   - GraphQL cho các truy vấn phức tạp, tổng hợp dữ liệu

4. **Fault Tolerance**
   - Circuit breaker pattern cho các lệnh gọi giữa services
   - Fallback mechanisms khi service không khả dụng
   - Retry policies cho các giao tiếp không ổn định

5. **Data Consistency**
   - SAGA pattern cho các transaction trải qua nhiều services
   - Event sourcing để duy trì consistency khi cập nhật dữ liệu
   - CQRS để tối ưu cho read và write operations

#### Kết luận

Việc xác định các chức năng dựa trên actors là bước quan trọng trong quá trình thiết kế hệ thống thương mại điện tử. Thông qua phân tích này, chúng ta đã xác định được:

- Các chức năng cụ thể mà mỗi actor cần
- Mối quan hệ giữa chức năng và microservices
- Luồng xử lý của các quy trình nghiệp vụ chính
- Cách tổ chức chức năng trong kiến trúc microservices

Bằng cách thiết kế chức năng theo hướng này, hệ thống thương mại điện tử không chỉ đáp ứng được nhu cầu của người dùng mà còn đảm bảo tính mô-đun, khả năng mở rộng và bảo trì dễ dàng trong tương lai.

#### Bảng tổng hợp chức năng theo actors

| Actor | Core Functions | Supporting Functions | Microservices |
|-------|---------------|---------------------|--------------|
| **Guest Customer** | - Duyệt sản phẩm<br>- Tìm kiếm sản phẩm<br>- Xem chi tiết sản phẩm<br>- Thêm vào giỏ hàng<br>- Đăng ký tài khoản | - Xem đánh giá sản phẩm<br>- Kiểm tra tồn kho<br>- Xem thông tin cửa hàng | - Product Service<br>- Book Service<br>- Shoe Service<br>- Cart Service<br>- Review Service<br>- Content Service |
| **Registered Customer** | - Đăng nhập<br>- Quản lý thông tin cá nhân<br>- Đặt hàng<br>- Thanh toán<br>- Theo dõi đơn hàng | - Đánh giá sản phẩm<br>- Yêu cầu hoàn tiền/đổi trả<br>- Lưu sản phẩm yêu thích<br>- Sử dụng mã giảm giá<br>- Xem sản phẩm gợi ý | - Auth Service<br>- Customer Service<br>- Book Service<br>- Shoe Service<br>- Cart Service<br>- Order Service<br>- Payment Service<br>- Review Service<br>- Promotion Service<br>- ML Service |
| **Seller** | - Quản lý thông tin cửa hàng<br>- Thêm, sửa, xóa sản phẩm<br>- Quản lý tồn kho<br>- Xử lý đơn hàng từ khách hàng | - Auth Service<br>- Customer Service<br>- Product Service<br>- Order Service<br>- Shipment Service | - Auth Service<br>- Customer Service<br>- Product Service<br>- Order Service<br>- Shipment Service |
| **Administrator** | - Quản lý người dùng<br>- Quản lý danh mục<br>- Quản lý sản phẩm<br>- Quản lý đơn hàng<br>- Quản lý tồn kho | - Auth Service<br>- Product Service<br>- Order Service<br>- Payment Service<br>- Analytics Service<br>- Review Service<br>- Configuration Service<br>- Content Service<br>- ML Service | - Auth Service<br>- Product Service<br>- Order Service<br>- Payment Service<br>- Analytics Service<br>- Review Service<br>- Configuration Service<br>- Content Service<br>- ML Service |
| **Payment Gateway** | - Xử lý thanh toán<br>- Xác thực giao dịch<br>- Thông báo kết quả thanh toán | - Payment Service | - Payment Service |
| **Shipping Partner** | - Nhận thông tin đơn hàng<br>- Cập nhật trạng thái giao hàng<br>- Xác nhận giao hàng | - Shipment Service | - Shipment Service |
| **Sentiment Analysis Service** | - Truy cập dữ liệu đánh giá<br>- Phân tích cảm xúc từ đánh giá | - Review Service | - Review Service |
| **Recommendation Service** | - Truy cập dữ liệu sản phẩm<br>- Truy cập dữ liệu người dùng<br>- Tạo và cung cấp gợi ý sản phẩm | - Product Service<br>- Book Service<br>- Shoe Service<br>- Review Service<br>- Sentiment Service | - Product Service<br>- Book Service<br>- Shoe Service<br>- Review Service<br>- Sentiment Service |

#### Mối quan hệ giữa chức năng và microservices thông qua bảng

| Microservice | Core Functions | Actors | APIs |
|--------------|---------------|--------|------|
| **API Gateway** | - Định tuyến yêu cầu<br>- Xác thực và phân quyền ban đầu<br>- Rate limiting, caching | Tất cả actors | - /api/* (định tuyến)<br>- /auth/verify (xác thực token) |
| **Auth Service** | - Đăng ký<br>- Đăng nhập<br>- Quản lý người dùng<br>- Phân quyền | - Guest Customer<br>- Registered Customer<br>- Administrator<br>- Seller | - /auth/register<br>- /auth/login<br>- /auth/users<br>- /auth/roles<br>- /auth/permissions |
| **Customer Service** | - Quản lý thông tin cá nhân<br>- Quản lý địa chỉ<br>- Danh sách yêu thích | - Registered Customer<br>- Administrator<br>- Seller | - /customers<br>- /customers/{id}<br>- /customers/{id}/addresses<br>- /customers/{id}/wishlist |
| **Product Service** | - Quản lý danh mục<br>- Quản lý sản phẩm<br>- Quản lý tồn kho<br>- Quản lý giá cả | - Guest Customer<br>- Registered Customer<br>- Administrator<br>- Seller | - /categories<br>- /products<br>- /products/{id}<br>- /products/{id}/inventory<br>- /products/search |
| **Cart Service** | - Thêm/xóa sản phẩm<br>- Cập nhật số lượng<br>- Lưu trữ giỏ hàng | - Guest Customer<br>- Registered Customer | - /cart<br>- /cart/items<br>- /cart/checkout |
| **Order Service** | - Tạo đơn hàng<br>- Quản lý trạng thái đơn hàng<br>- Lịch sử đơn hàng<br>- Xử lý đổi/trả | - Registered Customer<br>- Administrator<br>- Seller | - /orders<br>- /orders/{id}<br>- /orders/{id}/status<br>- /orders/{id}/refund<br>- /orders/history |
| **Payment Service** | - Tích hợp với cổng thanh toán<br>- Xử lý thanh toán<br>- Quản lý phương thức thanh toán<br>- Xử lý hoàn tiền | - Registered Customer<br>- Administrator<br>- Payment Gateway | - /payments<br>- /payments/methods<br>- /payments/{id}/status<br>- /payments/{id}/refund |
| **Shipment Service** | - Tích hợp đối tác vận chuyển<br>- Theo dõi đơn hàng<br>- Quản lý thông tin vận chuyển | - Registered Customer<br>- Seller<br>- Shipping Partner | - /shipments<br>- /shipments/{id}<br>- /shipments/{id}/tracking<br>- /shipments/options |
| **Review Service** | - Quản lý đánh giá<br>- Xếp hạng sản phẩm<br>- Duyệt đánh giá | - Guest Customer<br>- Registered Customer<br>- Administrator<br>- Seller | - /reviews<br>- /products/{id}/reviews<br>- /reviews/pending |
| **Promotion Service** | - Quản lý khuyến mãi<br>- Quản lý mã giảm giá<br>- Áp dụng quy tắc khuyến mãi | - Registered Customer<br>- Administrator<br>- Seller | - /promotions<br>- /coupons<br>- /coupons/validate |
| **ML Service** | - Gợi ý sản phẩm<br>- Phân tích hành vi<br>- Dự đoán xu hướng | - Registered Customer<br>- Administrator<br>- Seller | - /recommendations<br>- /analytics/trends<br>- /analytics/user-behavior |
| **Notification Service** | - Gửi email<br>- Gửi push notification<br>- Gửi SMS<br>- Quản lý mẫu thông báo | - Registered Customer<br>- Administrator<br>- Seller | - /notifications<br>- /notifications/email<br>- /notifications/push<br>- /notifications/sms<br>- /notifications/templates |

#### Mức độ ưu tiên chức năng

| Priority | Description | Examples |
|----------|-------------|----------|
| **Critical** | Chức năng thiết yếu, hệ thống không thể hoạt động nếu thiếu | - Đăng nhập<br>- Xem sản phẩm<br>- Đặt hàng<br>- Thanh toán |
| **High** | Chức năng quan trọng, ảnh hưởng đáng kể đến trải nghiệm người dùng | - Tìm kiếm sản phẩm<br>- Quản lý giỏ hàng<br>- Theo dõi đơn hàng<br>- Quản lý tồn kho |
| **Medium** | Chức năng cần thiết, cải thiện trải nghiệm nhưng không thiết yếu | - Đánh giá sản phẩm<br>- Danh sách yêu thích<br>- Sử dụng mã giảm giá<br>- Báo cáo bán hàng |
| **Low** | Chức năng bổ sung, cung cấp giá trị thêm | - Gợi ý sản phẩm<br>- Thông báo khuyến mãi<br>- Xem thống kê chi tiết<br>- Tùy chỉnh giao diện |

#### Bảng quyền truy cập chức năng

| Function | Guest Customer | Registered Customer | Administrator | Seller |
|----------|---------------|---------------------|---------------|--------|
| **Xem sản phẩm** | ✓ | ✓ | ✓ | ✓ |
| **Đặt hàng** | ✗ | ✓ | ✓ | ✓ |
| **Thanh toán** | ✗ | ✓ | ✗ | ✗ |
| **Quản lý tài khoản** | ✗ | ✓ | ✓ | ✗ |
| **Quản lý sản phẩm** | ✗ | ✗ | ✓ | ✓ |
| **Quản lý đơn hàng** | ✗ | ✗ | ✓ | ✓ |
| **Quản lý người dùng** | ✗ | ✗ | ✓ | ✗ |
| **Xem báo cáo** | ✗ | ✗ | ✓ | ✓ |
| **Cập nhật vận chuyển** | ✗ | ✗ | ✗ | ✗ |
| **Xử lý hoàn tiền** | ✗ | ✗ | ✓ | ✓ |

## 1.2 Analyze Requirements

Sau khi xác định rõ các actor và chức năng của hệ thống thương mại điện tử, chúng ta cần phân tích các yêu cầu chi tiết để triển khai hệ thống sử dụng kiến trúc microservices với Django. Phân tích này giúp xác định cách phân chia hệ thống, cấu trúc cơ sở dữ liệu, và các giao diện liên lạc giữa các dịch vụ.

### 1.2.1 Decompose the system in microservices with Django

Để phân tách hệ thống thành các microservice sử dụng Django, chúng ta áp dụng các nguyên tắc sau:

#### Nguyên tắc phân tách

1. **Phân tách theo nghiệp vụ (Domain-Driven Design)**: Mỗi microservice chịu trách nhiệm cho một phạm vi nghiệp vụ cụ thể, có ranh giới rõ ràng.
2. **Tính độc lập**: Mỗi microservice có thể phát triển, triển khai và vận hành độc lập với các service khác.
3. **Quản lý dữ liệu phi tập trung**: Mỗi service quản lý cơ sở dữ liệu riêng, phù hợp với yêu cầu của mình.
4. **Giao tiếp thông qua API**: Các microservice giao tiếp thông qua RESTful API hoặc message queue.

#### Cấu trúc Microservices sử dụng Django và Django REST Framework

| Microservice | Mô tả | Công nghệ | Cơ sở dữ liệu |
|--------------|-------|-----------|---------------|
| **API Gateway** | Cổng điều khiển cho tất cả các request | Nginx | - |
| **Customer Service** | Quản lý người dùng, xác thực, phân quyền | Django, DRF, JWT | MySQL |
| **Product Service** | Quản lý thông tin sản phẩm chung | Django, DRF | MongoDB |
| **Book Service** | Quản lý sản phẩm sách | Django, DRF | MongoDB |
| **Shoe Service** | Quản lý sản phẩm giày | Django, DRF | MongoDB |
| **Cart Service** | Quản lý giỏ hàng | Django, DRF | PostgreSQL |
| **Order Service** | Quản lý đơn hàng | Django, DRF | PostgreSQL |
| **Payment Service** | Xử lý thanh toán | Django, DRF | PostgreSQL |
| **Shipment Service** | Quản lý vận chuyển | Django, DRF | PostgreSQL |
| **Review Service** | Quản lý đánh giá | Django, DRF | MySQL |
| **Sentiment Service** | Phân tích cảm xúc đánh giá | Flask, ML Models | Redis |
| **Recommendation Service** | Đề xuất sản phẩm | Flask, ML Models | Redis |
| **Frontend** | Giao diện người dùng | HTML, CSS, JS | - |

#### Cấu trúc thư mục của mỗi Microservice Django

Mỗi microservice sẽ có cấu trúc thư mục tiêu chuẩn của Django, với một số điều chỉnh phù hợp cho kiến trúc microservices:

```
microservice-name/
├── service/                 # Django project directory
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── app_name/                # Django app directory
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Admin interface
│   ├── apps.py              # App configuration
│   ├── models.py            # Data models
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL routing
│   └── views.py             # Views and API endpoints
├── tests/                   # Test directory
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── manage.py                # Django management script
```

#### Triển khai với Docker và Docker Compose

Sử dụng Docker Compose để điều phối các microservice:

```yaml
# Ví dụ từ docker-compose.yml
services:
  api-gateway:
    build: ./api-gateway
    ports:
      - "80:80"
    depends_on:
      - customer-service
      - product-service
      
  customer-service:
    build: ./customer-service
    environment:
      - DB_HOST=db-mysql
    depends_on:
      - db-mysql
      
  product-service:
    build: ./product-service
    environment:
      - DB_HOST=db-mongo
    depends_on:
      - db-mongo
```

### 1.2.2 Classes with attributes of service models (models)

Dưới đây là mô hình dữ liệu chính cho từng microservice, thể hiện bằng các class model Django:

#### Customer Service

```python
# User Model
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
    
# Profile Models
class CustomerProfile(models.Model):
    class CustomerType(models.TextChoices):
        BRONZE = "bronze", "Khách hàng Đồng"
        SILVER = "silver", "Khách hàng Bạc"
        GOLD = "gold", "Khách hàng Vàng"
        PLATINUM = "platinum", "Khách hàng Bạch Kim"
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_type = models.CharField(max_length=10, choices=CustomerType.choices, default=CustomerType.BRONZE)
    loyalty_points = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
```

#### Product Service

```python
# Product Model
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    inventory_count = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# Category Model
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
```

#### Book Service

```python
# Book Model
class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField()
    page_count = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Cart Service

```python
# Cart Model
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# CartItem Model
class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_id = models.CharField(max_length=128)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
```

#### Order Service

```python
# Order Model
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
    user_id = models.UUIDField(db_index=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    payment_method = models.CharField(max_length=50)
    shipping_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Payment Service

```python
# Payment Model
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('vnpay', 'VNPay'),
        ('momo', 'Momo'),
        ('bank', 'Chuyển khoản ngân hàng'),
        ('paypal', 'PayPal'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Chờ thanh toán'),
        ('completed', 'Đã thanh toán'),
        ('failed', 'Thanh toán thất bại'),
        ('refunded', 'Đã hoàn tiền'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField(db_index=True)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
```

#### Review Service

```python
# Review Model
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.CharField(max_length=128, db_index=True)
    user_id = models.UUIDField(db_index=True)
    rating = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=255)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    helpful_votes = models.PositiveIntegerField(default=0)
    not_helpful_votes = models.PositiveIntegerField(default=0)
    is_hidden = models.BooleanField(default=False)
```

### 1.2.3 Determine functions in services (views)

Dưới đây là các chức năng chính được triển khai trong mỗi service dưới dạng Django views và DRF viewsets:

#### Customer Service

```python
# User Registration and Authentication
class RegisterAPI(APIView):
    def post(self, request):
        # Tạo tài khoản người dùng mới
        
class LoginAPI(APIView):
    def post(self, request):
        # Xác thực người dùng và tạo JWT token
        
# User Management
class UserViewSet(viewsets.ModelViewSet):
    # CRUD operations cho quản lý người dùng
    
# Seller Management
class ApproveSellerAPI(APIView):
    def post(self, request, user_id):
        # Phê duyệt yêu cầu trở thành người bán
```

#### Product Service

```python
# Product Management
class ProductViewSet(viewsets.ModelViewSet):
    # CRUD operations cho sản phẩm
    
    @action(detail=True, methods=['patch'])
    def update_inventory(self, request, pk=None):
        # Cập nhật tồn kho sản phẩm
        
# Category Management
class CategoryViewSet(viewsets.ModelViewSet):
    # CRUD operations cho danh mục sản phẩm
    
# Search
class SearchAPI(APIView):
    def get(self, request):
        # Tìm kiếm sản phẩm theo nhiều tiêu chí
```

#### Cart Service

```python
# Cart Management
class CreateCartAPI(APIView):
    def post(self, request, user_id):
        # Tạo giỏ hàng mới cho người dùng
        
class AddItemToCartView(APIView):
    def post(self, request):
        # Thêm sản phẩm vào giỏ hàng
        
class RemoveItemFromCartView(APIView):
    def post(self, request):
        # Xóa sản phẩm khỏi giỏ hàng
        
class UpdateCartItemView(APIView):
    def put(self, request):
        # Cập nhật số lượng sản phẩm trong giỏ hàng
        
class GetCartView(APIView):
    def get(self, request, user_id):
        # Lấy thông tin giỏ hàng
```

#### Order Service

```python
# Order Management
class OrderViewSet(viewsets.ModelViewSet):
    # CRUD operations cho đơn hàng
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        # Cập nhật trạng thái đơn hàng
        
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        # Hủy đơn hàng
        
    @action(detail=False, methods=['get'])
    def user_orders(self, request):
        # Lấy danh sách đơn hàng của người dùng
```

#### Payment Service

```python
# Payment Management
class PaymentViewSet(viewsets.ModelViewSet):
    # CRUD operations cho thanh toán
    
    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        # Cập nhật trạng thái thanh toán
        
    @action(detail=False, methods=['get'])
    def user_payments(self, request):
        # Lấy lịch sử thanh toán của người dùng
```

#### Review Service

```python
# Review Management
class ReviewViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['GET'], url_path='product_reviews/(?P<product_id>[^/.]+)')
    def product_reviews(self, request, product_id=None):
        # Lấy đánh giá của sản phẩm
        
    @action(detail=False, methods=['GET'], url_path='user_reviews/(?P<user_id>[^/.]+)')
    def user_reviews(self, request, user_id=None):
        # Lấy đánh giá của người dùng
        
    @action(detail=False, methods=['POST'], url_path='vote/(?P<review_id>[^/.]+)')
    def vote(self, request, review_id=None):
        # Đánh giá tính hữu ích của review
```

### 1.2.4 Determine templates

Trong kiến trúc microservices, phần frontend thường được tách biệt hoàn toàn khỏi backend. Tuy nhiên, một số template có thể được sử dụng trong từng service cho mục đích debugging hoặc admin interface.

#### Admin Templates

Mỗi Django service có thể sử dụng Django Admin interface cho quản trị nội bộ:

```python
# admin.py
from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'sale_price', 'inventory_count', 'is_available')
    search_fields = ('name', 'description')
    list_filter = ('is_available', 'created_at')
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
```

#### Frontend Templates

Frontend được phát triển như một ứng dụng riêng biệt (có thể sử dụng React, Vue, Angular) giao tiếp với backend thông qua API. Cấu trúc thư mục frontend có thể như sau:

```
frontend/
├── public/
│   ├── index.html
│   └── assets/
├── src/
│   ├── components/
│   │   ├── Header/
│   │   ├── Footer/
│   │   ├── ProductCard/
│   │   ├── Cart/
│   │   └── Checkout/
│   ├── pages/
│   │   ├── Home/
│   │   ├── ProductList/
│   │   ├── ProductDetail/
│   │   ├── Cart/
│   │   ├── Checkout/
│   │   ├── UserProfile/
│   │   └── OrderHistory/
│   ├── services/
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── products.js
│   │   └── orders.js
│   ├── store/
│   │   ├── index.js
│   │   ├── auth.js
│   │   └── cart.js
│   ├── App.js
│   └── index.js
└── package.json
```

### 1.2.5 Determine REST API connecting services

Các microservice giao tiếp với nhau thông qua REST API. Dưới đây là một số API endpoint chính:

#### Customer Service API

```
# Authentication
POST /user/register/           # Đăng ký tài khoản mới
POST /user/login/              # Đăng nhập
POST /user/auth/refresh/       # Làm mới JWT token

# User Management
GET /user/list/                # Danh sách người dùng
GET /user/detail/{user_id}/    # Chi tiết người dùng
PUT /user/detail/{user_id}/    # Cập nhật thông tin người dùng
POST /user/upload-avatar/      # Tải lên avatar

# Seller Management
GET /user/sellers/             # Danh sách người bán
POST /user/seller-requests/    # Gửi yêu cầu trở thành người bán
GET /user/seller-requests/pending/  # Danh sách yêu cầu chờ xử lý
POST /user/seller-requests/approve/{user_id}/  # Phê duyệt yêu cầu
```

#### Product Service API

```
# Products
GET /products/                 # Danh sách sản phẩm
POST /products/                # Tạo sản phẩm mới
GET /products/{id}/            # Chi tiết sản phẩm
PUT /products/{id}/            # Cập nhật sản phẩm
DELETE /products/{id}/         # Xóa sản phẩm
PATCH /products/{id}/inventory/# Cập nhật tồn kho

# Categories
GET /categories/               # Danh sách danh mục
POST /categories/              # Tạo danh mục mới
GET /categories/{id}/          # Chi tiết danh mục
GET /categories/{id}/products/ # Sản phẩm trong danh mục

# Search
GET /products/search/          # Tìm kiếm sản phẩm
```

#### Cart Service API

```
# Cart Management
POST /cart/create/{user_id}/            # Tạo giỏ hàng mới
POST /cart/add-item/                    # Thêm sản phẩm vào giỏ
POST /cart/remove-item/                 # Xóa sản phẩm khỏi giỏ
PUT /cart/update-item/                  # Cập nhật số lượng sản phẩm
GET /cart/get/{user_id}/                # Lấy thông tin giỏ hàng
```

#### Order Service API

```
# Orders
GET /orders/                   # Danh sách đơn hàng
POST /orders/                  # Tạo đơn hàng mới
GET /orders/{id}/              # Chi tiết đơn hàng
PATCH /orders/{id}/status/     # Cập nhật trạng thái đơn hàng
POST /orders/{id}/cancel/      # Hủy đơn hàng
GET /orders/user/{user_id}/    # Đơn hàng của người dùng
```

#### Payment Service API

```
# Payments
GET /payments/                 # Danh sách thanh toán
POST /payments/                # Tạo thanh toán mới
GET /payments/{id}/            # Chi tiết thanh toán
PUT /payments/{id}/status/     # Cập nhật trạng thái thanh toán
GET /payments/user/{user_id}/  # Thanh toán của người dùng
```

#### Review Service API

```
# Reviews
GET /reviews/product_reviews/{product_id}/  # Đánh giá của sản phẩm
GET /reviews/user_reviews/{user_id}/        # Đánh giá của người dùng
POST /reviews/                              # Tạo đánh giá mới
POST /reviews/vote/{review_id}/             # Đánh giá tính hữu ích
```

#### Giao tiếp giữa các Service

Các microservice giao tiếp với nhau thông qua HTTP request. Ví dụ:

```python
# Cart Service gọi Product Service để lấy thông tin sản phẩm
def get_product_data(product_id):
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}{product_id}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

# Order Service gọi Cart Service để lấy thông tin giỏ hàng
def get_cart_data(user_id):
    try:
        response = requests.get(f"{CART_SERVICE_URL}/cart/get/{user_id}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None
```

## 1.3 Conclusion

Việc phân tích yêu cầu và thiết kế hệ thống thương mại điện tử microservices đã giúp chúng ta xác định rõ các thành phần và cách triển khai:

1. **Actors và Use Cases**: Xác định rõ các đối tượng sử dụng hệ thống và các chức năng mà họ có thể thực hiện, từ đó tạo nền tảng cho việc thiết kế API và giao diện người dùng.

2. **Microservices Architecture**: Phân tách hệ thống thành các dịch vụ nhỏ, độc lập, mỗi dịch vụ đảm nhận một phần chức năng cụ thể, giúp tăng tính module hóa, khả năng mở rộng và bảo trì dễ dàng trong tương lai.

3. **Data Models**: Định nghĩa các mô hình dữ liệu (Django models) cho từng service, đảm bảo tính nhất quán và phù hợp với chức năng của dịch vụ.

4. **Business Logic**: Triển khai logic nghiệp vụ trong các views và viewsets, mỗi dịch vụ xử lý riêng phần logic của mình.

5. **API Endpoints**: Thiết kế RESTful API để giao tiếp giữa các dịch vụ và với frontend, tuân thủ các nguyên tắc API design hiện đại.

6. **System Integration**: Xác định cách thức giao tiếp giữa các microservice, đảm bảo tính nhất quán dữ liệu trong hệ thống phân tán.

Kiến trúc microservices với Django cung cấp nhiều lợi ích cho hệ thống thương mại điện tử:

- **Khả năng mở rộng**: Có thể dễ dàng mở rộng từng dịch vụ riêng biệt theo nhu cầu.
- **Linh hoạt công nghệ**: Mỗi service có thể sử dụng công nghệ phù hợp nhất với chức năng của mình.
- **Phát triển song song**: Các team có thể phát triển, triển khai và vận hành các service độc lập.
- **Khả năng chịu lỗi**: Sự cố ở một service không ảnh hưởng đến toàn bộ hệ thống.
- **Đơn giản hóa phức tạp**: Chia nhỏ hệ thống lớn thành các phần dễ quản lý hơn.

Tóm lại, hệ thống thương mại điện tử với kiến trúc microservices sử dụng Django đã được thiết kế để đáp ứng các yêu cầu về tính linh hoạt, khả năng mở rộng và bảo trì, đồng thời cung cấp trải nghiệm tốt cho người dùng thông qua các chức năng đa dạng và hiệu suất cao.

Tuy nhiên, kiến trúc này cũng đặt ra các thách thức về đồng bộ dữ liệu, giao tiếp giữa các service, và độ phức tạp trong việc triển khai và giám sát. Những thách thức này cần được giải quyết thông qua việc áp dụng các pattern như SAGA, Circuit Breaker, và sử dụng công cụ monitoring phù hợp.

Tóm lại, hệ thống thương mại điện tử với kiến trúc microservices sử dụng Django đã được thiết kế để đáp ứng các yêu cầu về tính linh hoạt, khả năng mở rộng và bảo trì, đồng thời cung cấp trải nghiệm tốt cho người dùng thông qua các chức năng đa dạng và hiệu suất cao. 