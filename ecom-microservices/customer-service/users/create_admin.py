#!/usr/bin/env python
import os
import django

# Thiết lập Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')
django.setup()

from users.models import User

# Thử tìm user hiện có
try:
    admin = User.objects.get(username='admin')
    print("User admin đã tồn tại, cập nhật thành quyền admin")
    admin.role = 'admin'
    admin.is_staff = True
    admin.is_superuser = True
    admin.status = 'active'
    admin.is_verified = True
    admin.save()
except User.DoesNotExist:
    # Tạo user admin mới
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role='admin'
    )
    print("Đã tạo user admin mới")

print(f"Thông tin admin: {admin.username}, {admin.email}, role={admin.role}")
print("Đăng nhập với tài khoản: admin / admin123") 