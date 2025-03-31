import unittest
from src.models.sentiment_model import SentimentModel
from unittest.mock import patch, MagicMock

class TestSentimentModel(unittest.TestCase):
    def setUp(self):
        """Thiết lập cho mỗi test case"""
        self.model = SentimentModel()
        # Đảm bảo model được tải
        self.model.model_loaded = True

    def test_rule_based_sentiment_positive(self):
        """Test phân tích cảm xúc tích cực với rule-based"""
        test_texts = [
            "This product is excellent!",
            "I love this, it's amazing and fantastic.",
            "Great quality and very helpful customer service."
        ]
        
        for text in test_texts:
            result = self.model._rule_based_sentiment(text)
            self.assertEqual(result['sentiment'], 'positive')
            self.assertGreaterEqual(result['score'], 0.5)

    def test_rule_based_sentiment_negative(self):
        """Test phân tích cảm xúc tiêu cực với rule-based"""
        test_texts = [
            "This product is terrible!",
            "I hate this, it's awful and disappointing.",
            "Poor quality and very frustrating experience."
        ]
        
        for text in test_texts:
            result = self.model._rule_based_sentiment(text)
            self.assertEqual(result['sentiment'], 'negative')
            self.assertGreaterEqual(result['score'], 0.5)

    def test_rule_based_sentiment_neutral(self):
        """Test phân tích cảm xúc trung tính với rule-based"""
        test_texts = [
            "This product is okay.",
            "It works as expected.",
            "I received the package yesterday."
        ]
        
        for text in test_texts:
            result = self.model._rule_based_sentiment(text)
            self.assertEqual(result['sentiment'], 'neutral')
            self.assertGreaterEqual(result['score'], 0.5)

    def test_negation_handling(self):
        """Test khả năng xử lý phủ định"""
        # Cụm từ tích cực nhưng có phủ định -> tiêu cực
        result = self.model._rule_based_sentiment("I don't like this product.")
        self.assertEqual(result['sentiment'], 'negative')
        
        # Cụm từ tiêu cực nhưng có phủ định -> tích cực
        result = self.model._rule_based_sentiment("This is not bad at all.")
        self.assertEqual(result['sentiment'], 'positive')

    def test_intensifier_handling(self):
        """Test khả năng xử lý từ tăng cường"""
        # Không có từ tăng cường
        regular = self.model._rule_based_sentiment("This is good.")
        
        # Có từ tăng cường
        intensified = self.model._rule_based_sentiment("This is very good.")
        
        # Điểm tin cậy của câu có từ tăng cường cao hơn
        self.assertGreater(intensified['score'], regular['score'])

    def test_predict_function(self):
        """Test chức năng dự đoán"""
        # Patch _rule_based_sentiment để kiểm tra
        with patch.object(self.model, '_rule_based_sentiment', return_value={'sentiment': 'positive', 'score': 0.9}) as mock_method:
            result = self.model.predict("Test text")
            
            # Kiểm tra _rule_based_sentiment được gọi
            mock_method.assert_called_once_with("Test text")
            
            # Kiểm tra kết quả
            self.assertEqual(result['sentiment'], 'positive')
            self.assertEqual(result['score'], 0.9)

    def test_batch_predict(self):
        """Test dự đoán theo lô"""
        texts = ["Text 1", "Text 2", "Text 3"]
        
        # Patch predict để kiểm tra
        with patch.object(self.model, 'predict', side_effect=[
            {'sentiment': 'positive', 'score': 0.9},
            {'sentiment': 'neutral', 'score': 0.6},
            {'sentiment': 'negative', 'score': 0.8}
        ]) as mock_method:
            results = self.model.batch_predict(texts)
            
            # Kiểm tra predict được gọi 3 lần
            self.assertEqual(mock_method.call_count, 3)
            
            # Kiểm tra kết quả
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0]['sentiment'], 'positive')
            self.assertEqual(results[1]['sentiment'], 'neutral')
            self.assertEqual(results[2]['sentiment'], 'negative')

    def test_error_handling(self):
        """Test xử lý lỗi"""
        # Patch _rule_based_sentiment để raise exception
        with patch.object(self.model, '_rule_based_sentiment', side_effect=Exception("Test error")):
            # Không nên raise exception
            result = self.model.predict("Test text")
            
            # Kiểm tra kết quả fallback
            self.assertIn(result['sentiment'], ['positive', 'neutral', 'negative'])
            self.assertGreaterEqual(result['score'], 0.5)
            self.assertLessEqual(result['score'], 1.0)

    def test_model_loading(self):
        """Test tải mô hình"""
        # Tạo model mới, chưa tải
        model = SentimentModel()
        self.assertFalse(model.model_loaded)
        
        # Gọi predict sẽ tải mô hình
        with patch.object(model, '_load_model') as mock_load:
            model.predict("Test text")
            mock_load.assert_called_once()

if __name__ == '__main__':
    unittest.main() 