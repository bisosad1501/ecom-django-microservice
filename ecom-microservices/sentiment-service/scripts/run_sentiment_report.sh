#!/bin/bash

# Script chạy báo cáo phân tích cảm xúc
# Cách sử dụng: ./run_sentiment_report.sh [--use-sample] [--product-ids=id1,id2,id3] [--output=thư_mục]

# Đường dẫn tới thư mục gốc
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${BASE_DIR}/reports/sentiment_analysis"
USE_SAMPLE=""
PRODUCT_IDS=""
LIMIT="100"

# Xử lý tham số dòng lệnh
for arg in "$@"; do
  case $arg in
    --use-sample)
      USE_SAMPLE="--use-sample"
      ;;
    --output=*)
      OUTPUT_DIR="${arg#*=}"
      ;;
    --product-ids=*)
      PRODUCT_IDS="--product-ids=${arg#*=}"
      ;;
    --limit=*)
      LIMIT="--limit=${arg#*=}"
      ;;
    *)
      echo "Tham số không được hỗ trợ: $arg"
      echo "Sử dụng: ./run_sentiment_report.sh [--use-sample] [--product-ids=id1,id2,id3] [--output=thư_mục] [--limit=100]"
      exit 1
      ;;
  esac
done

# Hiển thị thông tin
echo "Bắt đầu tạo báo cáo phân tích cảm xúc..."
echo "- Thư mục đầu ra: $OUTPUT_DIR"
if [ -n "$PRODUCT_IDS" ]; then
  echo "- Phân tích cho sản phẩm: ${PRODUCT_IDS#*=}"
fi
if [ -n "$USE_SAMPLE" ]; then
  echo "- Sử dụng dữ liệu mẫu: Có"
fi

# Tạo thư mục đầu ra nếu chưa tồn tại
mkdir -p "$OUTPUT_DIR"

# Chạy script Python
cd "$BASE_DIR" && python -m scripts.sentiment_report \
  --output="$OUTPUT_DIR" \
  $USE_SAMPLE \
  $PRODUCT_IDS \
  $LIMIT

# Kiểm tra kết quả
if [ $? -eq 0 ]; then
  echo "Báo cáo đã được tạo thành công!"
  echo "Bạn có thể xem báo cáo tại: $OUTPUT_DIR/index.html"
else
  echo "Đã xảy ra lỗi khi tạo báo cáo."
  exit 1
fi 