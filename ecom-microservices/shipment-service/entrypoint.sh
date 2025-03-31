#!/bin/sh

# Chờ PostgreSQL khởi động
echo "⌛ Đang chờ PostgreSQL tại $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "✅ Đã kết nối thành công tới PostgreSQL!"

# Tạo và áp dụng migrations
echo "🔄 Đang tạo migrations..."
python manage.py makemigrations --noinput

echo "🔄 Đang áp dụng migrations..."
python manage.py migrate --noinput

echo "🚀 Khởi động Django server..."
exec python manage.py runserver 0.0.0.0:8007
