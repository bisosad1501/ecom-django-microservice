# filepath: /sentiment-service/sentiment-service/src/api/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class SentimentRequest(BaseModel):
    """
    Schema cho yêu cầu phân tích cảm xúc của một đoạn văn bản
    """
    text: str = Field(..., description="Văn bản cần phân tích cảm xúc")

class SentimentBatchRequest(BaseModel):
    """
    Schema cho yêu cầu phân tích cảm xúc của nhiều đoạn văn bản
    """
    texts: List[str] = Field(..., description="Danh sách các văn bản cần phân tích cảm xúc")

class SentimentResult(BaseModel):
    """
    Schema cho kết quả phân tích cảm xúc
    """
    text: str = Field(..., description="Văn bản gốc")
    sentiment: str = Field(..., description="Nhãn cảm xúc: positive, neutral, negative")
    score: float = Field(..., description="Điểm tin cậy của phân loại, từ 0.0 đến 1.0")

class SentimentDistribution(BaseModel):
    """
    Schema cho phân phối cảm xúc
    """
    positive: int = Field(0, description="Số lượng đánh giá tích cực")
    neutral: int = Field(0, description="Số lượng đánh giá trung tính")
    negative: int = Field(0, description="Số lượng đánh giá tiêu cực")

class ReviewSentiment(BaseModel):
    """
    Schema cho thông tin cảm xúc của một review
    """
    label: str = Field(..., description="Nhãn cảm xúc: positive, neutral, negative")
    score: float = Field(..., description="Điểm tin cậy của phân loại, từ 0.0 đến 1.0")

class ReviewItem(BaseModel):
    """
    Schema cho một review
    """
    id: str = Field(..., description="ID của review")
    product_id: str = Field(..., description="ID của sản phẩm")
    user_id: str = Field(..., description="ID của người dùng")
    rating: int = Field(..., description="Xếp hạng từ 1-5")
    title: Optional[str] = Field(None, description="Tiêu đề review")
    comment: str = Field(..., description="Nội dung review")
    sentiment: Optional[ReviewSentiment] = Field(None, description="Thông tin cảm xúc của review")
    created_at: str = Field(..., description="Thời gian tạo review")

class ReviewsRequest(BaseModel):
    """
    Schema cho danh sách reviews cần phân tích
    """
    reviews: List[ReviewItem] = Field(..., description="Danh sách các review cần phân tích")

class ProductReviewsRequest(BaseModel):
    """
    Schema cho yêu cầu phân tích reviews của một sản phẩm
    """
    product_id: str = Field(..., description="ID của sản phẩm")
    limit: Optional[int] = Field(100, description="Số lượng reviews tối đa")

class ProductSentimentResult(BaseModel):
    """
    Schema cho kết quả phân tích cảm xúc của reviews sản phẩm
    """
    product_id: str = Field(..., description="ID của sản phẩm")
    total_reviews: int = Field(..., description="Tổng số reviews đã phân tích")
    sentiment_score: float = Field(..., description="Điểm cảm xúc tổng hợp từ 0.0 đến 1.0")
    sentiment_distribution: SentimentDistribution = Field(..., description="Phân phối cảm xúc")
    analyzed_reviews: List[ReviewItem] = Field(..., description="Danh sách reviews đã phân tích cảm xúc")

class ErrorResponse(BaseModel):
    """
    Schema cho thông báo lỗi
    """
    error: str = Field(..., description="Mô tả lỗi")
    code: Optional[int] = Field(None, description="Mã lỗi")