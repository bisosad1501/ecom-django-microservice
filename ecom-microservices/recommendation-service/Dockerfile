FROM python:3.9-slim

WORKDIR /app

# First install Werkzeug to ensure compatible version
RUN pip install werkzeug==2.0.3 flask==2.0.1 flask-cors==3.0.10

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Đảm bảo entrypoint.sh có quyền thực thi
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose the service port
EXPOSE 5000

# Set entrypoint to use absolute path
ENTRYPOINT ["/app/entrypoint.sh"] 