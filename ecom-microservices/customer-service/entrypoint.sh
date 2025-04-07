#!/bin/sh

# Chờ MySQL sẵn sàng (sử dụng biến môi trường từ compose)
echo "⌛ Đang chờ MySQL khởi động tại $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "✅ Đã kết nối thành công tới MySQL!"

# Kiểm tra trạng thái migration hiện tại
echo "🔍 Kiểm tra trạng thái migration..."
python manage.py showmigrations

# Tạo migrations
echo "🔄 Đang tạo migrations..."
python manage.py makemigrations --noinput -v 3

# Áp dụng migrations
echo "🔄 Đang áp dụng migrations..."
python manage.py migrate --noinput

echo "🚀 Khởi động Django server..."
exec python manage.py runserver 0.0.0.0:8001
