FROM nginx:alpine

# Cài đặt các công cụ cần thiết
RUN apk add --no-cache \
    gcc \
    libc-dev \
    make \
    openssl-dev \
    pcre-dev \
    zlib-dev \
    linux-headers \
    curl \
    gnupg \
    libxslt-dev \
    gd-dev \
    geoip-dev \
    perl-dev

# Tải và cài đặt headers-more-nginx-module
RUN cd /tmp && \
    curl -L -O https://github.com/openresty/headers-more-nginx-module/archive/v0.34.tar.gz && \
    tar -xzvf v0.34.tar.gz && \
    cd headers-more-nginx-module-0.34 && \
    NGINX_VERSION=$(nginx -v 2>&1 | sed 's/^[^0-9]*\([0-9.]*\).*/\1/') && \
    curl -L -O http://nginx.org/download/nginx-$NGINX_VERSION.tar.gz && \
    tar -xzvf nginx-$NGINX_VERSION.tar.gz && \
    cd nginx-$NGINX_VERSION && \
    ./configure --with-compat --add-dynamic-module=.. && \
    make modules && \
    cp objs/ngx_http_headers_more_filter_module.so /etc/nginx/modules/ && \
    cd / && \
    rm -rf /tmp/*

# Copy cấu hình Nginx
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Tạo thư mục cho modules
RUN mkdir -p /etc/nginx/modules

# Load module trong nginx.conf
RUN echo "load_module modules/ngx_http_headers_more_filter_module.so;" > /etc/nginx/modules.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
