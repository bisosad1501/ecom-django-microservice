# Phát triển dịch vụ phân tích cảm xúc

Tài liệu này cung cấp hướng dẫn chi tiết về cách thiết lập môi trường phát triển và các công cụ cần thiết để phát triển dịch vụ phân tích cảm xúc.

## Thiết lập môi trường phát triển

### Yêu cầu

- Python 3.8+
- Docker và Docker Compose
- Git
- IDE (khuyến nghị: Visual Studio Code hoặc PyCharm)

### Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd ecom-microservices/sentiment-service
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
```

3. Cài đặt các thư viện phụ thuộc:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Thư viện cho phát triển
```

4. Tải NLTK data:
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

## Kiến trúc dự án

### Cấu trúc thư mục

```
sentiment-service/
│
├── src/                      # Mã nguồn chính
│   ├── api/                  # API endpoints
│   ├── models/               # Mô hình phân tích cảm xúc
│   ├── services/             # Các dịch vụ
│   ├── utils/                # Tiện ích
│   └── analytics/            # Phân tích xu hướng
│
├── tests/                    # Thử nghiệm
│
├── scripts/                  # Scripts tiện ích
│
├── k8s/                      # Tệp cấu hình Kubernetes
│
├── mock_data/                # Dữ liệu mẫu cho testing
│
└── reports/                  # Thư mục chứa báo cáo
```

### Các thành phần chính

1. **API Layer** (`src/api/`):
   - Định nghĩa các REST endpoints
   - Xử lý request/response
   - Định nghĩa schemas

2. **Service Layer** (`src/services/`):
   - Phân tích cảm xúc
   - Xử lý dữ liệu
   - Tương tác với Review Service

3. **Model Layer** (`src/models/`):
   - Mô hình phân tích cảm xúc
   - Rule-based fallback

4. **Analytics Layer** (`src/analytics/`):
   - Phân tích xu hướng
   - Tạo báo cáo và trực quan hóa

## Workflow phát triển

### Branch Strategy

- Sử dụng Git Flow:
  - `main`: Mã nguồn chính, luôn ở trạng thái sẵn sàng triển khai
  - `develop`: Mã nguồn cho phát triển
  - `feature/name`: Cho phát triển tính năng mới
  - `fix/name`: Cho sửa lỗi
  - `release/version`: Chuẩn bị release

### Coding Standards

- Tuân thủ PEP 8
- Sử dụng type annotations
- Docstrings theo chuẩn Google style
- Tất cả các hàm và class phải có docstring
- Tất cả API mới phải có test

### Code Review Process

1. Tạo Pull Request từ feature branch vào develop
2. Chạy các kiểm tra tự động (tests, linting, type checking)
3. Code review bởi ít nhất 1 thành viên team
4. Squash và merge khi được chấp thuận

## Testing

### Chạy tests

```bash
# Chạy tất cả tests
pytest

# Chạy tests với coverage
pytest --cov=src tests/

# Chạy tests cụ thể
pytest tests/test_sentiment_analyzer.py
```

### Mocking Dependencies

- Sử dụng `unittest.mock` để mock các dependencies
- Mock Review Service khi test SentimentAnalyzer
- Mock SentimentModel khi test API routes

## CI/CD

### CI Pipeline

1. **Lint và Type Check**:
   - Chạy `flake8` để kiểm tra style code
   - Chạy `mypy` để kiểm tra type annotations

2. **Unit Tests**:
   - Chạy `pytest` với coverage report

3. **Build và Push Docker Image**:
   - Build Docker image 
   - Push lên Docker Registry

### CD Pipeline

1. **Deployment to Staging**:
   - Tự động khi PR được merge vào `develop`
   - Deploy lên môi trường Kubernetes staging

2. **Deployment to Production**:
   - Tự động khi PR được merge vào `main`
   - Deploy lên môi trường Kubernetes production

## Chạy dịch vụ trong quá trình phát triển

### Chạy nhanh (không Docker)

```bash
# Chạy dịch vụ với mock data
python -m src.app
```

### Chạy với Docker Compose

```bash
# Build và chạy dịch vụ
docker-compose up --build

# Chạy với biến môi trường tùy chỉnh
REVIEW_SERVICE_URL=http://localhost:5001/api docker-compose up
```

### Chạy với Kubernetes (minikube)

```bash
# Khởi động minikube
minikube start

# Apply Kubernetes manifests
kubectl apply -f k8s/

# Lấy URL để truy cập dịch vụ
minikube service sentiment-service --url
```

## Debugging

### Logs

- Log được cấu hình trong `src/app.py`
- Log level có thể điều chỉnh qua biến môi trường `LOG_LEVEL`

### Debug với VSCode

Tạo file `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Sentiment Service",
      "type": "python",
      "request": "launch",
      "module": "src.app",
      "env": {
        "DEBUG": "True",
        "PORT": "5000"
      },
      "justMyCode": false
    }
  ]
}
```

## Tài liệu tham khảo

- [Flask Documentation](https://flask.palletsprojects.com/)
- [NLTK Documentation](https://www.nltk.org/)
- [Sentiment Analysis with NLTK](https://www.nltk.org/howto/sentiment.html)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)

## Liên hệ

Với câu hỏi, hãy liên hệ nhóm phát triển qua:
- Email: [email@example.com]
- Slack: #sentiment-service-dev 