FROM python:3.11-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Cài đặt system dependencies
RUN apt-get update && \
    apt-get install -y \
    netcat-openbsd \
    libpq-dev \
    gcc \
    python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8003

ENTRYPOINT ["./entrypoint.sh"]
