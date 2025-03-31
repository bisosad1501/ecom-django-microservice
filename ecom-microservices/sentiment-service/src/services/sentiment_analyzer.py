import os
import json
from typing import List, Dict, Any, Optional
import requests
from src.models.sentiment_model import SentimentModel
from src.utils.text_preprocessing import preprocess_text
from src.services.review_client import ReviewClient

class SentimentAnalyzer:
    """
    Dịch vụ phân tích cảm xúc cho reviews
    """
    
    def __init__(self, model_path=None):
        """
        Khởi tạo dịch vụ phân tích cảm xúc
        
        Args:
            model_path (str, optional): Đường dẫn đến mô hình. Mặc định sẽ sử dụng đường dẫn từ biến môi trường.
        """
        self.model = SentimentModel(model_path)
        self.review_client = ReviewClient()
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Phân tích cảm xúc của một đoạn văn bản
        
        Args:
            text (str): Văn bản cần phân tích
            
        Returns:
            Dict[str, Any]: Kết quả phân tích cảm xúc bao gồm nhãn và độ tin cậy
        """
        # Tiền xử lý văn bản
        processed_text = preprocess_text(text)
        
        # Phân tích cảm xúc
        result = self.model.analyze_text(processed_text)
        
        return result
    
    def analyze_reviews(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Phân tích cảm xúc cho một danh sách các reviews
        
        Args:
            reviews (List[Dict[str, Any]]): Danh sách các review cần phân tích
            
        Returns:
            List[Dict[str, Any]]: Danh sách review đã được phân tích cảm xúc
        """
        # Trích xuất nội dung review từ danh sách review
        texts = []
        for review in reviews:
            # Kiểm tra xem nội dung review ở trường nào
            if 'comment' in review and review['comment']:
                texts.append(review['comment'])
            elif 'content' in review and review['content']:
                texts.append(review['content']) 
            elif 'text' in review and review['text']:
                texts.append(review['text'])
            else:
                texts.append('') # Thêm chuỗi rỗng nếu không tìm thấy nội dung
        
        # Tiền xử lý văn bản nếu cần
        processed_texts = [preprocess_text(text) for text in texts]
        
        # Phân tích cảm xúc cho mỗi văn bản
        sentiment_results = self.model.analyze_batch(processed_texts)
        
        # Cập nhật kết quả vào các review
        analyzed_reviews = []
        for i, review in enumerate(reviews):
            # Tạo bản sao của review để không thay đổi dữ liệu gốc
            analyzed_review = review.copy()
            
            # Thêm thông tin phân tích nếu có kết quả
            if i < len(sentiment_results) and sentiment_results[i]:
                analyzed_review['sentiment'] = sentiment_results[i]['sentiment'] 
                analyzed_review['sentiment_score'] = sentiment_results[i]['score']
                if 'star_rating' in sentiment_results[i]:
                    analyzed_review['star_rating'] = sentiment_results[i]['star_rating']
            else:
                # Giá trị mặc định nếu không phân tích được
                analyzed_review['sentiment'] = 'neutral'
                analyzed_review['sentiment_score'] = 0.5
                
            analyzed_reviews.append(analyzed_review)
            
        return analyzed_reviews
    
    def analyze_product_reviews(self, product_id: str, limit: int = 100) -> Dict[str, Any]:
        """
        Phân tích cảm xúc cho reviews của một sản phẩm
        
        Args:
            product_id (str): ID của sản phẩm
            limit (int, optional): Số lượng reviews tối đa. Mặc định là 100.
            
        Returns:
            Dict[str, Any]: Kết quả phân tích bao gồm phân phối cảm xúc và danh sách reviews đã phân tích
        """
        # Sử dụng trực tiếp phương thức analyze_product_reviews của model
        return self.model.analyze_product_reviews(product_id, limit=limit)
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Phân tích cảm xúc cho một danh sách văn bản
        
        Args:
            texts (List[str]): Danh sách văn bản cần phân tích
            
        Returns:
            List[Dict[str, Any]]: Kết quả phân tích cho từng văn bản
        """
        # Tiền xử lý các văn bản
        processed_texts = [preprocess_text(text) for text in texts]
        
        # Sử dụng phương thức analyze_batch của model
        return self.model.analyze_batch(processed_texts)

def analyze_sentiment(reviews):
    """
    Helper function để phân tích cảm xúc của một danh sách reviews
    
    Args:
        reviews (List[Dict]): Danh sách reviews cần phân tích
        
    Returns:
        Dict: Kết quả phân tích bao gồm phân phối cảm xúc và danh sách reviews đã phân tích
    """
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_reviews(reviews)

def fetch_reviews_from_service(service_url):
    response = requests.get(service_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch reviews from the review service.")