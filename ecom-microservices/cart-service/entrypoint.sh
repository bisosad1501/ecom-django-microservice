#!/bin/sh

# Chờ PostgreSQL khởi động
echo "⌛ Đang chờ PostgreSQL tại $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "✅ Đã kết nối thành công tới PostgreSQL!"

# Thực hiện migration
echo "🔄 Áp dụng database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "🚀 Khởi động Django server..."
exec python manage.py runserver 0.0.0.0:8003
