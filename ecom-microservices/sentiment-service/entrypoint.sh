#!/bin/sh

# Chờ dịch vụ review-service sẵn sàng
echo "⌛ Đang chờ review-service khởi động tại $REVIEW_SERVICE_URL..."
while ! curl -s "$REVIEW_SERVICE_URL/health-check" > /dev/null; do
  echo "Đợi review-service..."
  sleep 3
done

echo "✅ Đã kết nối thành công tới review-service!"

# Tạo thư mục cần thiết
mkdir -p /app/reports/sentiment_analysis

# Tải dữ liệu NLTK nếu cần
echo "🔄 Đảm bảo dữ liệu NLTK đã được tải..."
python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True)"

echo "🚀 Khởi động Sentiment Analysis Service..."
exec python -m src.app
