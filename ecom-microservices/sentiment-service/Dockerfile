# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# First install Werkzeug to ensure compatible version
RUN pip install werkzeug==2.0.3

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Create cache directory for huggingface models
RUN mkdir -p /root/.cache/huggingface/

# Download and cache the transformer model
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    model_name = 'distilbert-base-uncased-finetuned-sst-2-english'; \
    tokenizer = AutoTokenizer.from_pretrained(model_name); \
    model = AutoModelForSequenceClassification.from_pretrained(model_name)"

# Tải trước mô hình đa ngôn ngữ thay cho mô hình tiếng Việt cụ thể
ARG PRELOAD_MULTILINGUAL_MODEL=true
ENV PRELOAD_MULTILINGUAL_MODEL=${PRELOAD_MULTILINGUAL_MODEL}
RUN if [ "$PRELOAD_MULTILINGUAL_MODEL" = "true" ] ; then \
        python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
        model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'; \
        tokenizer = AutoTokenizer.from_pretrained(model_name); \
        model = AutoModelForSequenceClassification.from_pretrained(model_name)" ; \
    fi

# Create necessary directories
RUN mkdir -p /app/reports/sentiment_analysis

# Copy the application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8010 \
    TRANSFORMERS_OFFLINE=0 \
    TRANSFORMERS_CACHE=/root/.cache/huggingface/ \
    HOST=0.0.0.0 \
    REVIEW_SERVICE_URL=http://review-service:8004

# Expose the application port
EXPOSE 8010

# Set the entrypoint
CMD ["python", "-m", "src.app"]