#!/bin/sh

# Chờ MongoDB sẵn sàng (sử dụng biến môi trường từ compose)
echo "⌛ Đang chờ MongoDB khởi động tại $DB_HOST:$DB_PORT..."
while ! python -c "import socket; s = socket.socket(); s.connect(('$DB_HOST', $DB_PORT))"; do
  sleep 1
done

echo "✅ Đã kết nối thành công tới MongoDB!"

# Tạo và áp dụng migrations
echo "🔄 Đang tạo migrations..."
python manage.py makemigrations --noinput

echo "🔄 Đang áp dụng migrations..."
python manage.py migrate --noinput

echo "🚀 Khởi động Django server..."
exec python manage.py runserver 0.0.0.0:8005