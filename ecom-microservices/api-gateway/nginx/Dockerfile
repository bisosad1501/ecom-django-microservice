FROM nginx:1.25-alpine

# Xóa các file mặc định
RUN rm -rf /etc/nginx/conf.d/*

# Copy file cấu hình chính
COPY nginx.conf /etc/nginx/nginx.conf

# Tạo thư mục log
RUN mkdir -p /var/log/nginx

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
