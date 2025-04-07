#!/bin/sh

# Khởi động service recommendation
echo "🚀 Đang khởi động Recommendation Service..."

# Kiểm tra và đảm bảo biến môi trường đã được thiết lập
echo "✅ Kiểm tra cấu hình môi trường..."
echo "    - PRODUCT_SERVICE_URL: $PRODUCT_SERVICE_URL"
echo "    - BOOK_SERVICE_URL: $BOOK_SERVICE_URL"
echo "    - SHOE_SERVICE_URL: $SHOE_SERVICE_URL"

# Khởi động ứng dụng Python
echo "🚀 Khởi động Flask application..."
exec python -m src.app
