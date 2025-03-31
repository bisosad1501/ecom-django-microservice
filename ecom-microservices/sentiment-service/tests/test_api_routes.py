import unittest
import json
from unittest.mock import patch, MagicMock
from flask import Flask
from src.api.routes import api_bp
from src.services.sentiment_analyzer import SentimentAnalyzer

class TestAPIRoutes(unittest.TestCase):
    def setUp(self):
        """Thiết lập cho mỗi test case"""
        # Tạo ứng dụng Flask test
        self.app = Flask(__name__)
        self.app.register_blueprint(api_bp, url_prefix='/api')
        self.client = self.app.test_client()
        
        # Mock SentimentAnalyzer
        self.patcher = patch('src.api.routes.sentiment_analyzer')
        self.mock_analyzer = self.patcher.start()
        
    def tearDown(self):
        """Kết thúc sau mỗi test case"""
        self.patcher.stop()
    
    def test_health_check(self):
        """Test endpoint kiểm tra sức khỏe"""
        response = self.client.get('/api/health')
        
        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['service'], 'sentiment-service')
    
    def test_analyze_text(self):
        """Test endpoint phân tích cảm xúc văn bản"""
        # Mock kết quả phân tích
        self.mock_analyzer.analyze_text.return_value = {
            'text': 'I love this product!',
            'sentiment': 'positive',
            'score': 0.95
        }
        
        # Gửi request
        response = self.client.post('/api/analyze', 
                                   data=json.dumps({'text': 'I love this product!'}),
                                   content_type='application/json')
        
        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['sentiment'], 'positive')
        self.assertEqual(data['score'], 0.95)
        self.assertEqual(data['text'], 'I love this product!')
        
        # Kiểm tra analyzer được gọi đúng
        self.mock_analyzer.analyze_text.assert_called_once_with('I love this product!')
    
    def test_analyze_text_missing_parameter(self):
        """Test endpoint phân tích cảm xúc với thiếu tham số"""
        # Gửi request thiếu tham số text
        response = self.client.post('/api/analyze', 
                                   data=json.dumps({}),
                                   content_type='application/json')
        
        # Kiểm tra lỗi
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_analyze_batch(self):
        """Test endpoint phân tích nhiều văn bản"""
        # Mock kết quả
        self.mock_analyzer.analyze_batch.return_value = [
            {'text': 'Great!', 'sentiment': 'positive', 'score': 0.9},
            {'text': 'Terrible!', 'sentiment': 'negative', 'score': 0.8},
            {'text': 'Okay.', 'sentiment': 'neutral', 'score': 0.6}
        ]
        
        # Gửi request
        response = self.client.post('/api/analyze/batch', 
                                   data=json.dumps({'texts': ['Great!', 'Terrible!', 'Okay.']}),
                                   content_type='application/json')
        
        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 3)
        self.assertEqual(data['results'][0]['sentiment'], 'positive')
        self.assertEqual(data['results'][1]['sentiment'], 'negative')
        self.assertEqual(data['results'][2]['sentiment'], 'neutral')
        
        # Kiểm tra analyzer được gọi đúng
        self.mock_analyzer.analyze_batch.assert_called_once_with(['Great!', 'Terrible!', 'Okay.'])
    
    def test_analyze_batch_invalid_parameter(self):
        """Test endpoint phân tích nhiều văn bản với tham số không hợp lệ"""
        # Gửi request với tham số không phải list
        response = self.client.post('/api/analyze/batch', 
                                   data=json.dumps({'texts': 'not a list'}),
                                   content_type='application/json')
        
        # Kiểm tra lỗi
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_analyze_product_reviews(self):
        """Test endpoint phân tích cảm xúc đánh giá sản phẩm"""
        # Mock kết quả
        product_id = 'p1'
        mock_result = {
            'product_id': product_id,
            'total_reviews': 3,
            'sentiment_score': 0.7,
            'sentiment_distribution': {'positive': 2, 'neutral': 1, 'negative': 0},
            'analyzed_reviews': [{'id': 'r1', 'sentiment': {'label': 'positive'}}]
        }
        self.mock_analyzer.analyze_product_reviews.return_value = mock_result
        
        # Gửi request
        response = self.client.get(f'/api/product/{product_id}/sentiment?limit=10')
        
        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['product_id'], product_id)
        self.assertEqual(data['total_reviews'], 3)
        self.assertIn('sentiment_distribution', data)
        self.assertIn('analyzed_reviews', data)
        
        # Kiểm tra analyzer được gọi đúng
        self.mock_analyzer.analyze_product_reviews.assert_called_once_with(product_id, limit=10)
    
    def test_analyze_reviews(self):
        """Test endpoint phân tích danh sách reviews"""
        # Mock data
        reviews = [
            {'id': 'r1', 'comment': 'Great!'},
            {'id': 'r2', 'comment': 'Terrible!'}
        ]
        
        # Mock kết quả
        analyzed_reviews = [
            {'id': 'r1', 'comment': 'Great!', 'sentiment': {'label': 'positive', 'score': 0.9}},
            {'id': 'r2', 'comment': 'Terrible!', 'sentiment': {'label': 'negative', 'score': 0.8}}
        ]
        self.mock_analyzer.analyze_reviews.return_value = analyzed_reviews
        
        # Gửi request
        response = self.client.post('/api/reviews/sentiment', 
                                   data=json.dumps({'reviews': reviews}),
                                   content_type='application/json')
        
        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 2)
        
        # Kiểm tra analyzer được gọi đúng
        self.mock_analyzer.analyze_reviews.assert_called_once_with(reviews)
    
    @patch('src.api.routes.subprocess.run')
    def test_generate_sentiment_report(self, mock_subprocess):
        """Test endpoint tạo báo cáo phân tích cảm xúc"""
        # Mock kết quả subprocess
        mock_subprocess.return_value = MagicMock(stdout="Report generated", stderr="")
        
        # Gửi request
        response = self.client.post('/api/reports/generate', 
                                   data=json.dumps({
                                       'product_ids': ['p1', 'p2'],
                                       'use_sample': True,
                                       'limit': 50
                                   }),
                                   content_type='application/json')
        
        # Kiểm tra kết quả
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('report_path', data)
        
        # Kiểm tra subprocess được gọi với tham số đúng
        mock_subprocess.assert_called_once()
        args = mock_subprocess.call_args[0][0]
        self.assertIn('--product-ids=p1,p2', args)
        self.assertIn('--use-sample', args)
        self.assertIn('--limit=50', args)

if __name__ == '__main__':
    unittest.main() 