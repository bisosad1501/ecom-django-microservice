FROM python:3.11-slim

# Add necessary dependencies for build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose the port used by the review service (8004)
EXPOSE 8004

# Use the entrypoint script to start the service
ENTRYPOINT ["/app/entrypoint.sh"]