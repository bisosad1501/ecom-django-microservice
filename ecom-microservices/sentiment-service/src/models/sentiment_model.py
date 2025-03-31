import os
import json
import numpy as np
from typing import Dict, Any, List, Optional
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
import torch
import logging
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import re
from langdetect import detect

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize transformers variables
TRANSFORMER_AVAILABLE = False
try:
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    import torch
    from langdetect import detect
    TRANSFORMER_AVAILABLE = True
except ImportError:
    logging.warning("Transformers or torch not available. Using fallback model.")

# Model paths
ENGLISH_MODEL_PATH = os.getenv("SENTIMENT_MODEL_PATH", "distilbert-base-uncased-finetuned-sst-2-english")
MULTILINGUAL_MODEL_PATH = os.getenv("MULTILINGUAL_MODEL_PATH", "nlptown/bert-base-multilingual-uncased-sentiment")

class SentimentModel:
    """
    Mô hình phân tích cảm xúc sử dụng transformer hoặc rule-based
    """
    
    def __init__(self, model_path: Optional[str] = None, batch_size: int = 16):
        """
        Khởi tạo mô hình phân tích cảm xúc
        
        Args:
            model_path: Đường dẫn đến mô hình transformer, mặc định sẽ sử dụng mô hình tiếng Anh
            batch_size: Kích thước batch cho việc xử lý nhiều văn bản cùng lúc
        """
        # Thiết lập tham số
        self.batch_size = batch_size
        self.stopwords = set(stopwords.words('english')) if nltk.data.find('corpora/stopwords') else set()
        
        # Mô hình và tokenizer mặc định cho tiếng Anh
        self.en_model_path = model_path or ENGLISH_MODEL_PATH
        
        # Mô hình và tokenizer đa ngôn ngữ (hỗ trợ tiếng Việt)
        self.multilingual_model_path = MULTILINGUAL_MODEL_PATH
        
        # Thiết lập thiết bị (CPU/GPU)
        self.device = 'cuda' if torch.cuda.is_available() and os.environ.get('USE_GPU', 'False').lower() == 'true' else 'cpu'
        logger.info(f"Using device: {self.device.upper()}")
        
        # Khởi tạo mô hình transformer (nếu có thể)
        self.en_tokenizer = None
        self.en_model = None
        self.multilingual_tokenizer = None
        self.multilingual_model = None
        
        if TRANSFORMER_AVAILABLE:
            try:
                # Tải mô hình tiếng Anh
                logger.info(f"Loading English sentiment model: {self.en_model_path}")
                self.en_tokenizer = AutoTokenizer.from_pretrained(self.en_model_path)
                self.en_model = AutoModelForSequenceClassification.from_pretrained(self.en_model_path)
                self.en_model = self.en_model.to(self.device)
                
                # Tải mô hình đa ngôn ngữ (lazy loading - chỉ tải khi cần)
                if os.environ.get('PRELOAD_MULTILINGUAL_MODEL', 'False').lower() == 'true':
                    self._load_multilingual_model()
            except Exception as e:
                logger.error(f"Error loading transformer model: {str(e)}")
                if os.environ.get('USE_FALLBACK_MODEL', 'True').lower() == 'true':
                    logger.warning("Using fallback rule-based model")
                else:
                    raise
    
    def _load_multilingual_model(self):
        """Tải mô hình đa ngôn ngữ khi cần"""
        if self.multilingual_model is None:
            logger.info(f"Loading multilingual sentiment model: {self.multilingual_model_path}")
            self.multilingual_tokenizer = AutoTokenizer.from_pretrained(self.multilingual_model_path)
            self.multilingual_model = AutoModelForSequenceClassification.from_pretrained(self.multilingual_model_path)
            self.multilingual_model = self.multilingual_model.to(self.device)
    
    def _detect_language(self, text: str) -> str:
        """
        Phát hiện ngôn ngữ của văn bản
        
        Args:
            text: Văn bản cần phát hiện ngôn ngữ
            
        Returns:
            str: Mã ngôn ngữ (ví dụ: 'en', 'vi')
        """
        try:
            return detect(text)
        except:
            # Mặc định trả về tiếng Anh nếu không thể phát hiện
            return 'en'
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Phân tích cảm xúc của một đoạn văn bản
        
        Args:
            text: Đoạn văn bản cần phân tích
            
        Returns:
            Dict[str, Any]: Kết quả phân tích cảm xúc
        """
        # Phát hiện ngôn ngữ
        lang = self._detect_language(text)
        
        # Sử dụng transformer nếu có thể
        if TRANSFORMER_AVAILABLE and (self.en_model is not None or self.multilingual_model is not None):
            if lang != 'en':
                # Đảm bảo mô hình đa ngôn ngữ đã được tải
                if self.multilingual_model is None:
                    self._load_multilingual_model()
                
                # Nếu phát hiện ngôn ngữ khác tiếng Anh và có mô hình đa ngôn ngữ
                if self.multilingual_model is not None:
                    return self._analyze_with_transformer(text, self.multilingual_tokenizer, self.multilingual_model)
                else:
                    # Fallback về mô hình tiếng Anh nếu không có mô hình đa ngôn ngữ
                    logger.warning(f"Multilingual model not available, using English model for {lang} text")
            
            # Sử dụng mô hình tiếng Anh
            if self.en_model is not None:
                return self._analyze_with_transformer(text, self.en_tokenizer, self.en_model)
                
        # Fallback về phương pháp rule-based
        return self._analyze_with_rules(text)
    
    def _analyze_with_transformer(self, text: str, tokenizer, model) -> Dict[str, Any]:
        """
        Phân tích cảm xúc sử dụng mô hình transformer
        
        Args:
            text: Đoạn văn bản cần phân tích
            tokenizer: Tokenizer tương ứng với mô hình
            model: Mô hình transformer đã tải
            
        Returns:
            Dict[str, Any]: Kết quả phân tích cảm xúc
        """
        # Chuẩn bị input
        max_length = int(os.environ.get('MAX_LENGTH', 512))
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Dự đoán
        with torch.no_grad():
            outputs = model(**inputs)
            scores = outputs.logits.softmax(dim=1)
            
            # Lấy nhãn và điểm số
            # Mô hình đa ngôn ngữ 'nlptown/bert-base-multilingual-uncased-sentiment' trả về 5 lớp (1-5 sao)
            # trong khi DistilBERT trả về 2 lớp (negative/positive)
            num_labels = scores.shape[1]
            
            if num_labels == 2:
                # Mô hình binary (negative/positive)
                negative_idx = 0
                positive_idx = 1
                
                # Kiểm tra nếu positive score cao hơn
                if scores[0, positive_idx] > scores[0, negative_idx]:
                    return {
                        "text": text,
                        "sentiment": "positive",
                        "score": float(scores[0, positive_idx])
                    }
                else:
                    return {
                        "text": text,
                        "sentiment": "negative", 
                        "score": float(scores[0, negative_idx])
                    }
            elif num_labels == 3:
                # Mô hình 3 lớp (negative/neutral/positive)
                negative_idx = 0
                neutral_idx = 1
                positive_idx = 2
                
                # Lấy index của điểm cao nhất
                max_score_idx = scores[0].argmax().item()
                
                if max_score_idx == positive_idx:
                    return {
                        "text": text,
                        "sentiment": "positive",
                        "score": float(scores[0, positive_idx])
                    }
                elif max_score_idx == negative_idx:
                    return {
                        "text": text,
                        "sentiment": "negative",
                        "score": float(scores[0, negative_idx])
                    }
                else:
                    return {
                        "text": text,
                        "sentiment": "neutral",
                        "score": float(scores[0, neutral_idx])
                    }
            elif num_labels == 5:
                # Mô hình 5 sao (như bert-base-multilingual-uncased-sentiment)
                # Điểm từ 1-5 sao, chuyển đổi thành positive/negative
                # Lấy index của điểm cao nhất (0=1 sao, 4=5 sao)
                star_rating = scores[0].argmax().item() + 1  # +1 vì index bắt đầu từ 0
                score = float(scores[0, star_rating - 1])  # Độ tin cậy
                
                # Coi 1-2 sao là tiêu cực, 3 là trung tính, 4-5 là tích cực
                if star_rating >= 4:
                    sentiment = "positive"
                    # Chuẩn hóa về thang điểm 0-1, với 4 sao = 0.8, 5 sao = 1.0
                    normalized_score = 0.6 + (star_rating - 3) * 0.2
                elif star_rating <= 2:
                    sentiment = "negative"
                    # Chuẩn hóa về thang điểm 0-1, với 1 sao = 0.2, 2 sao = 0.4
                    normalized_score = star_rating * 0.2
                else:  # 3 sao
                    sentiment = "neutral"
                    normalized_score = 0.5
                
                return {
                    "text": text,
                    "sentiment": sentiment,
                    "score": normalized_score,
                    "star_rating": star_rating
                }
            else:
                # Mặc định, giả sử negative là nhãn đầu tiên và positive là nhãn thứ hai
                negative_idx = 0
                positive_idx = 1 if num_labels > 1 else 0
                
                # Kiểm tra nếu positive score cao hơn
                if scores[0, positive_idx] > scores[0, negative_idx]:
                    return {
                        "text": text,
                        "sentiment": "positive",
                        "score": float(scores[0, positive_idx])
                    }
                else:
                    return {
                        "text": text,
                        "sentiment": "negative", 
                        "score": float(scores[0, negative_idx])
                    }
    
    def _analyze_with_rules(self, text: str) -> Dict[str, Any]:
        """
        Phân tích cảm xúc sử dụng phương pháp rule-based đơn giản
        
        Args:
            text: Đoạn văn bản cần phân tích
            
        Returns:
            Dict[str, Any]: Kết quả phân tích cảm xúc
        """
        # Các từ tích cực và tiêu cực (tiếng Anh)
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'best', 'love', 'awesome', 
                         'happy', 'satisfied', 'perfect', 'recommended', 'positive', 'beautiful', 'nice', 'fan'}
        negative_words = {'bad', 'worst', 'terrible', 'awful', 'disappointing', 'horrible', 'poor', 'waste',
                         'not', 'never', 'problem', 'issues', 'faulty', 'negative', 'broken', 'uncomfortable', 'useless'}
        
        # Các từ tích cực và tiêu cực (tiếng Việt)
        vi_positive_words = {'tốt', 'hay', 'tuyệt', 'vời', 'xuất sắc', 'đẹp', 'thích', 'yêu', 'hài lòng', 
                           'tuyệt vời', 'tốt nhất', 'tuyệt hảo', 'hoàn hảo', 'giỏi', 'hấp dẫn', 'tiện lợi'}
        vi_negative_words = {'tệ', 'kém', 'xấu', 'dở', 'chán', 'thất vọng', 'không', 'chẳng', 'không thích', 
                           'không hài lòng', 'không tốt', 'hỏng', 'lỗi', 'vấn đề', 'khó chịu', 'gãy', 'hư'}
        
        # Kết hợp từ điển dựa vào ngôn ngữ phát hiện
        lang = self._detect_language(text)
        if lang == 'vi':
            positive_words.update(vi_positive_words)
            negative_words.update(vi_negative_words)
        
        # Tiền xử lý văn bản
        text = text.lower()
        words = re.findall(r'\w+', text)
        words = [word for word in words if word not in self.stopwords]
        
        # Đếm từ tích cực và tiêu cực
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        # Phân loại cảm xúc
        if positive_count > negative_count:
            sentiment = "positive"
            score = 0.5 + min(0.5, (positive_count - negative_count) / len(words) if words else 0)
        elif negative_count > positive_count:
            sentiment = "negative"
            score = 0.5 + min(0.5, (negative_count - positive_count) / len(words) if words else 0)
        else:
            # Nếu số lượng bằng nhau, xét thêm các từ ngữ phủ định
            negation_count = sum(1 for i in range(len(words)-1) if words[i] in {'not', 'no', 'never', 'không', 'chẳng'})
            if negation_count > 0:
                sentiment = "negative"
                score = 0.5 + min(0.4, negation_count / len(words) if words else 0)
            else:
                sentiment = "neutral"
                score = 0.5
                
        return {
            "text": text,
            "sentiment": sentiment,
            "score": score
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Phân tích cảm xúc cho một danh sách văn bản
        
        Args:
            texts: Danh sách văn bản cần phân tích
            
        Returns:
            List[Dict[str, Any]]: Kết quả phân tích cảm xúc cho mỗi văn bản
        """
        results = []
        
        # Nhóm văn bản theo ngôn ngữ để xử lý batch hiệu quả hơn
        en_texts = []
        non_en_texts = []
        text_indices = {}  # Lưu vị trí gốc của mỗi văn bản
        
        for i, text in enumerate(texts):
            lang = self._detect_language(text)
            if lang == 'en':
                text_indices[f"en_{len(en_texts)}"] = i
                en_texts.append(text)
            else:
                text_indices[f"non_en_{len(non_en_texts)}"] = i
                non_en_texts.append(text)
        
        # Kết quả sẽ chứa None cho mỗi văn bản, sẽ được cập nhật sau
        results = [None] * len(texts)
        
        # Xử lý văn bản tiếng Anh
        if en_texts and TRANSFORMER_AVAILABLE and self.en_model is not None:
            en_results = self._analyze_batch_with_transformer(en_texts, self.en_tokenizer, self.en_model)
            for i, res in enumerate(en_results):
                original_idx = text_indices[f"en_{i}"]
                results[original_idx] = res
        else:
            # Fallback về phương pháp rule-based
            for i, text in enumerate(en_texts):
                original_idx = text_indices[f"en_{i}"]
                results[original_idx] = self._analyze_with_rules(text)
        
        # Xử lý văn bản không phải tiếng Anh
        if non_en_texts and TRANSFORMER_AVAILABLE:
            # Tải mô hình đa ngôn ngữ nếu cần
            if self.multilingual_model is None:
                self._load_multilingual_model()
                
            if self.multilingual_model is not None:
                non_en_results = self._analyze_batch_with_transformer(non_en_texts, self.multilingual_tokenizer, self.multilingual_model)
                for i, res in enumerate(non_en_results):
                    original_idx = text_indices[f"non_en_{i}"]
                    results[original_idx] = res
            else:
                # Fallback nếu không có mô hình đa ngôn ngữ
                for i, text in enumerate(non_en_texts):
                    original_idx = text_indices[f"non_en_{i}"]
                    results[original_idx] = self._analyze_with_rules(text)
        else:
            # Fallback về phương pháp rule-based
            for i, text in enumerate(non_en_texts):
                original_idx = text_indices[f"non_en_{i}"]
                results[original_idx] = self._analyze_with_rules(text)
        
        return results
    
    def _analyze_batch_with_transformer(self, texts: List[str], tokenizer, model) -> List[Dict[str, Any]]:
        """
        Phân tích cảm xúc cho một batch văn bản sử dụng transformer
        
        Args:
            texts: Danh sách văn bản cần phân tích
            tokenizer: Tokenizer tương ứng với mô hình
            model: Mô hình transformer đã tải
            
        Returns:
            List[Dict[str, Any]]: Kết quả phân tích cảm xúc cho mỗi văn bản
        """
        results = []
        max_length = int(os.environ.get('MAX_LENGTH', 512))
        
        # Xử lý theo batch
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            
            # Tokenize batch
            inputs = tokenizer(batch_texts, padding=True, truncation=True, 
                               return_tensors="pt", max_length=max_length)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Dự đoán
            with torch.no_grad():
                outputs = model(**inputs)
                scores = outputs.logits.softmax(dim=1)
                
                # Xác định số lớp đầu ra của mô hình
                num_labels = scores.shape[1]
                
                for j, text in enumerate(batch_texts):
                    if num_labels == 2:
                        # Mô hình binary (negative/positive)
                        negative_idx = 0
                        positive_idx = 1
                        
                        if scores[j, positive_idx] > scores[j, negative_idx]:
                            results.append({
                                "text": text,
                                "sentiment": "positive",
                                "score": float(scores[j, positive_idx])
                            })
                        else:
                            results.append({
                                "text": text,
                                "sentiment": "negative",
                                "score": float(scores[j, negative_idx])
                            })
                    elif num_labels == 3:
                        # Mô hình 3 lớp (negative/neutral/positive)
                        negative_idx = 0
                        neutral_idx = 1
                        positive_idx = 2
                        
                        max_score_idx = scores[j].argmax().item()
                        
                        if max_score_idx == positive_idx:
                            results.append({
                                "text": text,
                                "sentiment": "positive",
                                "score": float(scores[j, positive_idx])
                            })
                        elif max_score_idx == negative_idx:
                            results.append({
                                "text": text,
                                "sentiment": "negative",
                                "score": float(scores[j, negative_idx])
                            })
                        else:
                            results.append({
                                "text": text,
                                "sentiment": "neutral",
                                "score": float(scores[j, neutral_idx])
                            })
                    elif num_labels == 5:
                        # Mô hình 5 sao (như bert-base-multilingual-uncased-sentiment)
                        # Điểm từ 1-5 sao, chuyển đổi thành positive/negative
                        # Lấy index của điểm cao nhất (0=1 sao, 4=5 sao)
                        star_rating = scores[j].argmax().item() + 1  # +1 vì index bắt đầu từ 0
                        score = float(scores[j, star_rating - 1])  # Độ tin cậy
                        
                        # Coi 1-2 sao là tiêu cực, 3 là trung tính, 4-5 là tích cực
                        if star_rating >= 4:
                            sentiment = "positive"
                            normalized_score = 0.6 + (star_rating - 3) * 0.2
                        elif star_rating <= 2:
                            sentiment = "negative"
                            normalized_score = star_rating * 0.2
                        else:  # 3 sao
                            sentiment = "neutral"
                            normalized_score = 0.5
                        
                        results.append({
                            "text": text,
                            "sentiment": sentiment,
                            "score": normalized_score,
                            "star_rating": star_rating
                        })
                    else:
                        # Mặc định, giả sử negative là nhãn đầu tiên và positive là nhãn thứ hai
                        negative_idx = 0
                        positive_idx = 1 if num_labels > 1 else 0
                        
                        if scores[j, positive_idx] > scores[j, negative_idx]:
                            results.append({
                                "text": text,
                                "sentiment": "positive",
                                "score": float(scores[j, positive_idx])
                            })
                        else:
                            results.append({
                                "text": text,
                                "sentiment": "negative",
                                "score": float(scores[j, negative_idx])
                            })
        
        return results
    
    def analyze_reviews(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Phân tích cảm xúc cho danh sách reviews
        
        Args:
            reviews: Danh sách reviews, mỗi review là một dict có trường 'comment'
            
        Returns:
            List[Dict[str, Any]]: Danh sách reviews đã được phân tích cảm xúc
        """
        # Chuẩn bị văn bản để phân tích
        texts = []
        for review in reviews:
            if 'comment' in review and review['comment']:
                texts.append(review['comment'])
            else:
                texts.append('')  # Văn bản rỗng cho những review không có comment
        
        # Phân tích cảm xúc
        sentiment_results = self.analyze_batch(texts)
        
        # Kết hợp kết quả vào reviews
        for i, review in enumerate(reviews):
            if i < len(sentiment_results) and sentiment_results[i]:
                review['sentiment'] = sentiment_results[i]['sentiment']
                review['sentiment_score'] = sentiment_results[i]['score']
                # Thêm star_rating nếu có
                if 'star_rating' in sentiment_results[i]:
                    review['star_rating'] = sentiment_results[i]['star_rating']
            else:
                review['sentiment'] = 'neutral'
                review['sentiment_score'] = 0.5
        
        return reviews
    
    def analyze_product_reviews(self, product_id: str, limit: int = 100) -> Dict[str, Any]:
        """
        Phân tích cảm xúc cho reviews của một sản phẩm
        
        Args:
            product_id: ID của sản phẩm
            limit: Số lượng reviews tối đa
            
        Returns:
            Dict[str, Any]: Kết quả phân tích cảm xúc
        """
        from src.services.review_client import ReviewClient
        
        # Lấy reviews từ review service
        review_client = ReviewClient()
        review_data = review_client.get_product_reviews(product_id, limit=limit)
        
        # Trích xuất reviews từ cấu trúc dữ liệu
        verified_reviews = review_data.get('verified_reviews', [])
        general_reviews = review_data.get('general_reviews', [])
        reviews = verified_reviews + general_reviews
        
        # Nếu không có reviews, trả về kết quả trống
        if not reviews:
            return {
                "product_id": product_id,
                "reviews": [],
                "sentiment_distribution": {
                    "positive": 0,
                    "neutral": 0, 
                    "negative": 0
                },
                "overall_sentiment": "neutral",
                "overall_score": 0.5
            }
        
        # Phân tích cảm xúc
        analyzed_reviews = self.analyze_reviews(reviews)
        
        # Tính toán phân phối cảm xúc
        positive_count = sum(1 for r in analyzed_reviews if r.get('sentiment') == 'positive')
        neutral_count = sum(1 for r in analyzed_reviews if r.get('sentiment') == 'neutral')
        negative_count = sum(1 for r in analyzed_reviews if r.get('sentiment') == 'negative')
        
        # Tính điểm số tổng thể
        total_score = sum(r.get('sentiment_score', 0.5) for r in analyzed_reviews)
        avg_score = total_score / len(analyzed_reviews) if analyzed_reviews else 0.5
        
        # Tính điểm sao trung bình nếu có
        star_ratings = [r.get('star_rating') for r in analyzed_reviews if 'star_rating' in r]
        avg_stars = sum(star_ratings) / len(star_ratings) if star_ratings else None
        
        # Xác định cảm xúc tổng thể
        if positive_count > negative_count:
            overall_sentiment = "positive"
        elif negative_count > positive_count:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"
        
        # Thông tin thống kê từ review service
        stats = review_data.get('stats', {})
        average_rating = stats.get('average_rating', 0.0)
        total_reviews = stats.get('total_reviews', len(reviews))
        
        # Thông tin sản phẩm
        product_info = review_data.get('product', {})
        
        result = {
            "product_id": product_id,
            "product_info": product_info,
            "reviews": analyzed_reviews,
            "review_stats": {
                "total_reviews": total_reviews,
                "average_rating": average_rating
            },
            "sentiment_distribution": {
                "positive": positive_count,
                "neutral": neutral_count,
                "negative": negative_count
            },
            "overall_sentiment": overall_sentiment,
            "overall_score": avg_score
        }
        
        # Thêm điểm sao trung bình nếu có
        if avg_stars is not None:
            result["average_star_rating"] = avg_stars
            
        return result
