"""
Cấu hình cho dịch vụ phân tích cảm xúc
"""

import os
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

# Tải cấu hình từ file .env nếu có
load_dotenv()

class Settings(BaseModel):
    """
    Cấu hình ứng dụng
    """
    # Cấu hình cơ bản
    APP_NAME: str = "Sentiment Analysis Service"
    APP_VERSION: str = "1.0.0"
    API_VERSION: str = "v1"
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Cấu hình máy chủ
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "5000"))
    
    # Đường dẫn mô hình
    MODEL_PATH: Optional[str] = os.environ.get("MODEL_PATH")
    
    # Cấu hình dịch vụ Review
    REVIEW_SERVICE_URL: str = os.environ.get("REVIEW_SERVICE_URL", "http://review-service:5000/api")
    REVIEW_SERVICE_TIMEOUT: int = int(os.environ.get("REVIEW_SERVICE_TIMEOUT", "10"))
    
    # Cấu hình báo cáo
    REPORTS_DIR: str = os.environ.get("REPORTS_DIR", "reports/sentiment_analysis")
    
    # Cấu hình CORS
    CORS_ORIGINS: list = os.environ.get("CORS_ORIGINS", "*").split(",")
    
    # Cấu hình cache
    CACHE_ENABLED: bool = os.environ.get("CACHE_ENABLED", "True").lower() in ("true", "1", "t")
    CACHE_TTL: int = int(os.environ.get("CACHE_TTL", "3600"))  # 1 giờ

# Tạo đối tượng cấu hình để sử dụng trong ứng dụng
settings = Settings()

def get_settings() -> Settings:
    """
    Lấy cấu hình ứng dụng
    
    Returns:
        Settings: Đối tượng cấu hình
    """
    return settings