# Tài liệu kiểm thử Postman cho Sentiment Analysis Service

Thư mục này chứa các tập tin cần thiết để kiểm thử Sentiment Analysis Service bằng Postman.

## Nội dung

- `sentiment_service_collection.json`: Bộ sưu tập các API request kiểm thử
- `environment_local.json`: Cấu hình môi trường cho kiểm thử local
- `test_data.json`: Dữ liệu mẫu để kiểm thử API

## Hướng dẫn sử dụng

1. Cài đặt [Postman](https://www.postman.com/downloads/)
2. Import collection file `sentiment_service_collection.json` vào Postman
3. Import environment file `environment_local.json` vào Postman
4. Chọn môi trường "Sentiment Service Local" từ dropdown trên góc phải
5. Chạy các request hoặc sử dụng "Collection Runner" để chạy toàn bộ collection

## Các API endpoint có sẵn

### Kiểm tra trạng thái
- `GET /api/health`: Kiểm tra trạng thái dịch vụ

### Phân tích cảm xúc văn bản
- `POST /api/analyze`: Phân tích cảm xúc cho một đoạn văn bản
  ```json
  {
    "text": "Sản phẩm này rất tốt, tôi rất hài lòng"
  }
  ```
  
- `POST /api/analyze_batch`: Phân tích cảm xúc cho nhiều đoạn văn bản cùng lúc
  ```json
  {
    "texts": [
      "Sản phẩm này rất tốt, tôi rất hài lòng",
      "Sản phẩm tạm được, không có gì đặc biệt",
      "Sản phẩm kém chất lượng, không đáng tiền"
    ]
  }
  ```

- `POST /api/reviews/sentiment`: Phân tích cảm xúc cho danh sách reviews có ID
  ```json
  {
    "reviews": [
      {
        "id": "1",
        "comment": "Sản phẩm này rất tốt, tôi rất hài lòng"
      },
      {
        "id": "2",
        "comment": "Sản phẩm kém chất lượng, không đáng tiền"
      }
    ]
  }
  ```

### Phân tích cảm xúc cho sản phẩm
- `GET /api/product/{product_id}/sentiment`: Phân tích cảm xúc cho các đánh giá của một sản phẩm
  - Query parameters:
    - `limit` (int, optional): Số lượng reviews tối đa. Mặc định là 100.

### Báo cáo và thống kê
- `GET /api/trends/distribution`: Lấy phân phối cảm xúc tổng quan của toàn bộ hệ thống

- `GET /api/products/top`: Lấy danh sách sản phẩm có cảm xúc tích cực nhất
  - Query parameters:
    - `limit` (int, optional): Số lượng sản phẩm tối đa. Mặc định là 10.

- `GET /api/products/compare`: So sánh cảm xúc giữa hai hoặc nhiều sản phẩm
  - Query parameters:
    - `product_ids` (string, required): Danh sách ID sản phẩm, phân cách bằng dấu phẩy.

## Thông tin phiên bản

- Dịch vụ chạy trên cổng `8010`
- Hỗ trợ phân tích song ngữ (Tiếng Anh và Tiếng Việt)
- Sử dụng mô hình Transformer cho kết quả chính xác cao
- Hỗ trợ phân tích theo batch với hiệu suất tối ưu
- Tích hợp hoàn chỉnh với review-service để phân tích cảm xúc các đánh giá trong hệ thống 