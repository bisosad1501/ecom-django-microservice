FROM python:3.11-slim

# Thêm các dependencies cần thiết cho build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    netcat-openbsd \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/app/entrypoint.sh"]
