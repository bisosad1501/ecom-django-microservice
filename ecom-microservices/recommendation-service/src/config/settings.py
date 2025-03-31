"""
Configuration settings for the recommendation service
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API settings
    API_VERSION = os.getenv("API_VERSION", "1.0.0")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Recommendation settings
    DEFAULT_RECOMMENDATIONS = int(os.getenv("DEFAULT_RECOMMENDATIONS", "10"))
    MAX_RECOMMENDATIONS = int(os.getenv("MAX_RECOMMENDATIONS", "50"))
    
    # Cache settings
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    CACHE_TYPE = os.getenv("CACHE_TYPE", "simple")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour
    USER_RECOMMENDATIONS_TTL = int(os.getenv("USER_RECOMMENDATIONS_TTL", "3600"))  # 1 hour
    PRODUCT_SIMILARITY_TTL = int(os.getenv("PRODUCT_SIMILARITY_TTL", "7200"))  # 2 hours
    SENTIMENT_RECOMMENDATIONS_TTL = int(os.getenv("SENTIMENT_RECOMMENDATIONS_TTL", "1800"))  # 30 minutes
    POPULAR_PRODUCTS_TTL = int(os.getenv("POPULAR_PRODUCTS_TTL", "3600"))  # 1 hour
    
    # External services URLs
    PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8000")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8003")
    SENTIMENT_SERVICE_URL = os.getenv("SENTIMENT_SERVICE_URL", "http://sentiment-service:5000/api")
    REVIEW_SERVICE_URL = os.getenv("REVIEW_SERVICE_URL", "http://review-service:8004")
    BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://book-service:8002")
    SHOE_SERVICE_URL = os.getenv("SHOE_SERVICE_URL", "http://shoe-service:8010")
    
    # Timeouts (in seconds)
    DEFAULT_REQUEST_TIMEOUT = int(os.getenv("DEFAULT_REQUEST_TIMEOUT", "5"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Recommendation algorithm weights
    COLLABORATIVE_FILTERING_WEIGHT = float(os.getenv("COLLABORATIVE_FILTERING_WEIGHT", "0.5"))
    CONTENT_BASED_WEIGHT = float(os.getenv("CONTENT_BASED_WEIGHT", "0.3"))
    SENTIMENT_WEIGHT = float(os.getenv("SENTIMENT_WEIGHT", "0.2"))
    COLLABORATION_WEIGHT = float(os.getenv("COLLABORATION_WEIGHT", "0.7"))
    
    # Feature flags
    ENABLE_SENTIMENT_ANALYSIS = os.getenv("ENABLE_SENTIMENT_ANALYSIS", "True").lower() == "true"
    ENABLE_USER_HISTORY = os.getenv("ENABLE_USER_HISTORY", "True").lower() == "true"
    ENABLE_CATEGORY_FILTERING = os.getenv("ENABLE_CATEGORY_FILTERING", "True").lower() == "true"
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", "100"))  # requests per minute
    
    # CORS settings
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Model settings
    MODEL_DIR = os.getenv("MODEL_DIR", "/app/models") 