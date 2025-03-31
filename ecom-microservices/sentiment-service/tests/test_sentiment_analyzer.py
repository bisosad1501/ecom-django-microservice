import unittest
import os
import json
from unittest.mock import patch, MagicMock
from src.services.sentiment_analyzer import SentimentAnalyzer
from src.models.sentiment_model import SentimentModel

class TestSentimentAnalyzer(unittest.TestCase):
    """
    Test cho SentimentAnalyzer
    """
    
    def setUp(self):
        """
        Thiết lập trước mỗi test case
        """
        # Mock model để tránh tải model thực trong quá trình test
        self.model_patcher = patch('src.models.sentiment_model.SentimentModel')
        self.mock_model_class = self.model_patcher.start()
        self.mock_model = self.mock_model_class.return_value
        
        # Mock kết quả dự đoán
        self.mock_model.predict.return_value = {'sentiment': 'positive', 'score': 0.85}
        self.mock_model.batch_predict.return_value = [
            {'sentiment': 'positive', 'score': 0.85},
            {'sentiment': 'negative', 'score': 0.75}
        ]
        
        # Mock ReviewClient
        self.client_patcher = patch('src.services.review_client.ReviewClient')
        self.mock_client_class = self.client_patcher.start()
        self.mock_client = self.mock_client_class.return_value
        
        # Mock kết quả lấy reviews
        self.mock_reviews = [
            {
                'id': '1',
                'product_id': 'product123',
                'user_id': 'user456',
                'rating': 5,
                'title': 'Great product',
                'comment': 'I love this product!',
                'created_at': '2023-01-01T12:00:00Z'
            },
            {
                'id': '2',
                'product_id': 'product123',
                'user_id': 'user789',
                'rating': 1,
                'title': 'Terrible',
                'comment': 'This product is awful.',
                'created_at': '2023-01-02T12:00:00Z'
            }
        ]
        
        self.mock_client.get_product_reviews.return_value = {
            'results': self.mock_reviews,
            'count': len(self.mock_reviews)
        }
        
        # Khởi tạo SentimentAnalyzer
        self.analyzer = SentimentAnalyzer()
    
    def tearDown(self):
        """
        Dọn dẹp sau mỗi test case
        """
        self.model_patcher.stop()
        self.client_patcher.stop()
    
    def test_analyze_text(self):
        """
        Test phương thức analyze_text
        """
        text = "This is a great product!"
        result = self.analyzer.analyze_text(text)
        
        # Kiểm tra kết quả
        self.assertEqual(result['text'], text)
        self.assertEqual(result['sentiment'], 'positive')
        self.assertEqual(result['score'], 0.85)
        
        # Kiểm tra model.predict đã được gọi
        self.mock_model.predict.assert_called_once()
    
    def test_analyze_reviews(self):
        """
        Test phương thức analyze_reviews
        """
        # Đặt giá trị trả về cho mỗi lần gọi predict
        self.mock_model.predict.side_effect = [
            {'sentiment': 'positive', 'score': 0.85},
            {'sentiment': 'negative', 'score': 0.75}
        ]
        
        results = self.analyzer.analyze_reviews(self.mock_reviews)
        
        # Kiểm tra kết quả
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], '1')
        self.assertEqual(results[0]['sentiment']['label'], 'positive')
        self.assertEqual(results[0]['sentiment']['score'], 0.85)
        
        self.assertEqual(results[1]['id'], '2')
        self.assertEqual(results[1]['sentiment']['label'], 'negative')
        self.assertEqual(results[1]['sentiment']['score'], 0.75)
        
        # Kiểm tra model.predict đã được gọi đúng số lần
        self.assertEqual(self.mock_model.predict.call_count, 2)
    
    def test_analyze_product_reviews(self):
        """
        Test phương thức analyze_product_reviews
        """
        # Đặt giá trị trả về cho mỗi lần gọi predict
        self.mock_model.predict.side_effect = [
            {'sentiment': 'positive', 'score': 0.85},
            {'sentiment': 'negative', 'score': 0.75}
        ]
        
        product_id = 'product123'
        result = self.analyzer.analyze_product_reviews(product_id)
        
        # Kiểm tra review_client.get_product_reviews đã được gọi
        self.mock_client.get_product_reviews.assert_called_once_with(product_id, limit=100)
        
        # Kiểm tra kết quả
        self.assertEqual(result['product_id'], product_id)
        self.assertEqual(result['total_reviews'], 2)
        
        # Kiểm tra phân phối cảm xúc
        self.assertEqual(result['sentiment_distribution']['positive'], 1)
        self.assertEqual(result['sentiment_distribution']['negative'], 1)
        self.assertEqual(result['sentiment_distribution']['neutral'], 0)
        
        # Kiểm tra điểm cảm xúc tổng hợp: (1*1.0 + 0*0.5 + 1*0.0)/2 = 0.5
        self.assertEqual(result['sentiment_score'], 0.5)
        
        # Kiểm tra các reviews đã được phân tích
        analyzed_reviews = result['analyzed_reviews']
        self.assertEqual(len(analyzed_reviews), 2)
        self.assertEqual(analyzed_reviews[0]['sentiment']['label'], 'positive')
        self.assertEqual(analyzed_reviews[1]['sentiment']['label'], 'negative')
    
    def test_analyze_batch(self):
        """
        Test phương thức analyze_batch
        """
        texts = ["This is a great product!", "This product is terrible."]
        
        # Đặt giá trị trả về cho mỗi lần gọi predict
        self.mock_model.predict.side_effect = [
            {'sentiment': 'positive', 'score': 0.85},
            {'sentiment': 'negative', 'score': 0.75}
        ]
        
        results = self.analyzer.analyze_batch(texts)
        
        # Kiểm tra kết quả
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['text'], texts[0])
        self.assertEqual(results[0]['sentiment'], 'positive')
        self.assertEqual(results[0]['score'], 0.85)
        
        self.assertEqual(results[1]['text'], texts[1])
        self.assertEqual(results[1]['sentiment'], 'negative')
        self.assertEqual(results[1]['score'], 0.75)
        
        # Kiểm tra model.predict đã được gọi đúng số lần
        self.assertEqual(self.mock_model.predict.call_count, 2)

    def test_analyze_text_positive(self):
        """Test phân tích cảm xúc tích cực"""
        # Patch mô hình để trả về kết quả cố định
        with patch.object(SentimentModel, 'predict', return_value={'sentiment': 'positive', 'score': 0.95}):
            result = self.analyzer.analyze_text("I love this product!")
            self.assertEqual(result['sentiment'], 'positive')
            self.assertGreaterEqual(result['score'], 0.5)
            self.assertEqual(result['text'], "I love this product!")
    
    def test_analyze_text_negative(self):
        """Test phân tích cảm xúc tiêu cực"""
        with patch.object(SentimentModel, 'predict', return_value={'sentiment': 'negative', 'score': 0.85}):
            result = self.analyzer.analyze_text("This product is terrible!")
            self.assertEqual(result['sentiment'], 'negative')
            self.assertGreaterEqual(result['score'], 0.5)
            self.assertEqual(result['text'], "This product is terrible!")
    
    def test_analyze_text_neutral(self):
        """Test phân tích cảm xúc trung tính"""
        with patch.object(SentimentModel, 'predict', return_value={'sentiment': 'neutral', 'score': 0.75}):
            result = self.analyzer.analyze_text("This product is okay.")
            self.assertEqual(result['sentiment'], 'neutral')
            self.assertGreaterEqual(result['score'], 0.5)
            self.assertEqual(result['text'], "This product is okay.")
    
    def test_analyze_batch(self):
        """Test phân tích nhiều văn bản cùng lúc"""
        texts = ["Great product!", "I don't like it", "It's average"]
        expected_sentiments = ['positive', 'negative', 'neutral']
        
        # Mock kết quả cho batch_predict
        mock_results = [
            {'sentiment': 'positive', 'score': 0.9},
            {'sentiment': 'negative', 'score': 0.8},
            {'sentiment': 'neutral', 'score': 0.6}
        ]
        
        with patch.object(SentimentModel, 'batch_predict', return_value=mock_results):
            results = self.analyzer.analyze_batch(texts)
            
            self.assertEqual(len(results), 3)
            for i, result in enumerate(results):
                self.assertEqual(result['sentiment'], expected_sentiments[i])
                self.assertGreaterEqual(result['score'], 0.5)
                self.assertEqual(result['text'], texts[i])
    
    def test_analyze_reviews(self):
        """Test phân tích cảm xúc từ danh sách reviews"""
        reviews = [
            {'id': 'r1', 'product_id': 'p1', 'comment': 'Excellent product!'},
            {'id': 'r2', 'product_id': 'p1', 'comment': 'Very disappointed with this.'},
            {'id': 'r3', 'product_id': 'p1', 'comment': 'It works as expected.'}
        ]
        
        expected_sentiments = ['positive', 'negative', 'neutral']
        
        # Mock kết quả cho từng văn bản
        with patch.object(SentimentAnalyzer, 'analyze_text', side_effect=[
            {'text': reviews[0]['comment'], 'sentiment': 'positive', 'score': 0.9},
            {'text': reviews[1]['comment'], 'sentiment': 'negative', 'score': 0.8},
            {'text': reviews[2]['comment'], 'sentiment': 'neutral', 'score': 0.6}
        ]):
            results = self.analyzer.analyze_reviews(reviews)
            
            self.assertEqual(len(results), 3)
            for i, result in enumerate(results):
                self.assertEqual(result['sentiment']['label'], expected_sentiments[i])
                self.assertGreaterEqual(result['sentiment']['score'], 0.5)
                self.assertEqual(result['id'], reviews[i]['id'])
                self.assertEqual(result['product_id'], reviews[i]['product_id'])
    
    def test_analyze_product_reviews(self):
        """Test phân tích cảm xúc cho reviews của một sản phẩm"""
        product_id = 'p1'
        
        # Mock kết quả từ review_client
        mock_reviews = {
            'product_id': product_id,
            'total': 3,
            'results': [
                {'id': 'r1', 'product_id': product_id, 'comment': 'Great!'},
                {'id': 'r2', 'product_id': product_id, 'comment': 'Terrible!'},
                {'id': 'r3', 'product_id': product_id, 'comment': 'Okay.'}
            ]
        }
        
        # Mock kết quả phân tích reviews
        mock_analyzed_reviews = [
            {'id': 'r1', 'product_id': product_id, 'comment': 'Great!', 'sentiment': {'label': 'positive', 'score': 0.9}},
            {'id': 'r2', 'product_id': product_id, 'comment': 'Terrible!', 'sentiment': {'label': 'negative', 'score': 0.8}},
            {'id': 'r3', 'product_id': product_id, 'comment': 'Okay.', 'sentiment': {'label': 'neutral', 'score': 0.6}}
        ]
        
        with patch.object(self.analyzer.review_client, 'get_product_reviews', return_value=mock_reviews):
            with patch.object(self.analyzer, 'analyze_reviews', return_value=mock_analyzed_reviews):
                result = self.analyzer.analyze_product_reviews(product_id)
                
                self.assertEqual(result['product_id'], product_id)
                self.assertEqual(result['total_reviews'], 3)
                self.assertIn('sentiment_distribution', result)
                self.assertIn('sentiment_score', result)
                self.assertEqual(len(result['analyzed_reviews']), 3)
                
                # Kiểm tra phân phối cảm xúc
                self.assertEqual(result['sentiment_distribution']['positive'], 1)
                self.assertEqual(result['sentiment_distribution']['negative'], 1)
                self.assertEqual(result['sentiment_distribution']['neutral'], 1)
                
                # Kiểm tra điểm cảm xúc
                self.assertGreaterEqual(result['sentiment_score'], 0)
                self.assertLessEqual(result['sentiment_score'], 1)

if __name__ == '__main__':
    unittest.main()