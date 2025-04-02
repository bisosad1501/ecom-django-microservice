#!/bin/bash
set -e

# Đợi MySQL khởi động
until mysqladmin ping -h"localhost" -P"3306" -u"root" -p"$MYSQL_ROOT_PASSWORD" --silent; do
    sleep 1
done

# Tạo database nếu chưa tồn tại
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS review_db;" 