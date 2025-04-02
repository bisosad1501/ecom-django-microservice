#!/bin/bash
set -e

# Đợi PostgreSQL khởi động
until pg_isready -U postgres; do
    sleep 1
done

# Tạo databases nếu chưa tồn tại
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'order_db'" | grep -q 1 || \
    psql -U postgres -c "CREATE DATABASE order_db;"

psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'payment_db'" | grep -q 1 || \
    psql -U postgres -c "CREATE DATABASE payment_db;"

psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'shipment_db'" | grep -q 1 || \
    psql -U postgres -c "CREATE DATABASE shipment_db;" 