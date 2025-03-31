# Sentiment Analysis Service

Dịch vụ phân tích cảm xúc (Sentiment Analysis) cho hệ thống thương mại điện tử. Service này nhận đánh giá sản phẩm từ người dùng và phân tích cảm xúc để cung cấp thông tin về mức độ hài lòng của khách hàng.

## Tính năng

- Phân tích cảm xúc (tích cực, trung tính, tiêu cực) cho đánh giá sản phẩm
- Đánh giá cảm xúc theo thời gian thực cho reviews mới
- API để phân tích một đoạn văn bản hoặc nhiều đoạn văn bản cùng lúc
- Đánh giá cảm xúc cho một sản phẩm cụ thể dựa trên tất cả đánh giá
- Tạo báo cáo phân tích cảm xúc chi tiết
- Xem xu hướng cảm xúc theo thời gian
- So sánh cảm xúc giữa các sản phẩm

## Công nghệ

- Python 3.9
- Flask (Web Framework)
- Hugging Face Transformers (Phân tích cảm xúc sử dụng Deep Learning)
- PyTorch (Backend cho Transformers)
- NLTK (Xử lý ngôn ngữ tự nhiên)
- Pandas & NumPy (Xử lý dữ liệu)
- Matplotlib & Seaborn (Tạo biểu đồ và trực quan hóa)
- Docker & Kubernetes
- RESTful API

## Mô hình phân tích cảm xúc

Service sử dụng mô hình transformer từ Hugging Face để phân tích cảm xúc:

- **Model mặc định**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Thời gian phân tích**: ~30ms/text (với batch prediction)
- **Độ chính xác**: >90% trên các benchmark chuẩn

Mô hình có thể được thay đổi bằng cách đặt biến môi trường `SENTIMENT_MODEL_PATH` hoặc truyền vào tham số khi khởi tạo.

Trong trường hợp không thể tải mô hình transformer (do giới hạn tài nguyên hoặc lỗi), service sẽ tự động chuyển sang sử dụng mô hình rule-based đơn giản (dựa trên từ điển cảm xúc).

## Cài đặt

### Sử dụng Docker (khuyến nghị)

```bash
docker build -t sentiment-service .
docker run -p 8010:8010 sentiment-service
```

### Sử dụng Docker Compose

```bash
docker-compose up
```

### Cài đặt trực tiếp

```bash
# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python -m src.app
```

## API Endpoints

### Health Check

```
GET /health
```

### Phân tích cảm xúc một đoạn văn bản

```
POST /api/analyze
```

Body:
```json
{
    "text": "Sản phẩm này rất tuyệt vời!"
}
```

### Phân tích hàng loạt văn bản

```
POST /api/analyze/batch
```

Body:
```json
{
    "texts": [
        "Sản phẩm này tuyệt vời!",
        "Tôi không hài lòng với chất lượng.",
        "Đúng với mô tả, tạm ổn."
    ]
}
```

### Phân tích đánh giá của một sản phẩm

```
GET /api/product/{product_id}/sentiment
```

### Phân tích xu hướng cảm xúc

```
GET /api/trends/distribution
```

### Xem xu hướng cảm xúc theo thời gian

```
GET /api/trends/overtime?time_unit=month
```

### So sánh cảm xúc giữa các sản phẩm

```
GET /api/products/compare?product_ids=1,2,3
```

## Cấu hình

Cấu hình thông qua biến môi trường (hoặc file `.env`):

| Biến | Mô tả | Mặc định |
|------|-------|----------|
| `PORT` | Cổng cho ứng dụng | `8010` |
| `HOST` | Host cho ứng dụng | `0.0.0.0` |
| `DEBUG` | Chế độ debug | `False` |
| `REVIEW_SERVICE_URL` | URL của review service | `http://review-service:8004` |
| `SENTIMENT_MODEL_PATH` | Tên hoặc đường dẫn đến mô hình sentiment | `distilbert-base-uncased-finetuned-sst-2-english` |
| `TRANSFORMERS_CACHE` | Thư mục cache cho Transformers | `/root/.cache/huggingface/` |

## Kiểm thử

### Kiểm thử đơn vị

```bash
pytest
```

### Kiểm thử mô hình Transformer

```bash
python -m scripts.test_transformer_model
```

## Triển khai lên Kubernetes

```bash
kubectl apply -f k8s/
```

## Khắc phục sự cố

### Lỗi "ImportError: cannot import name 'url_quote' from 'werkzeug.urls'"

Đảm bảo rằng bạn đang sử dụng phiên bản Werkzeug tương thích với Flask:

```bash
pip install werkzeug==2.0.3 flask==2.0.1
```

### Lỗi về GPU cho PyTorch

Kiểm tra cấu hình CUDA:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

## Hiệu năng

- **CPU Mode**: ~100ms/text
- **GPU Mode**: ~10ms/text
- **Batch Mode (16 texts)**: ~2-5ms/text

## Liên hệ

Nếu bạn có câu hỏi hoặc góp ý, vui lòng tạo Issue hoặc Pull Request.