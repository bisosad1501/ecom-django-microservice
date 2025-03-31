import unittest
from src.app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'healthy'})

    def test_sentiment_analysis(self):
        review_data = {
            'review': 'This product is amazing!'
        }
        response = self.app.post('/analyze-sentiment', json=review_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('sentiment', response.json)

    def test_invalid_sentiment_analysis(self):
        response = self.app.post('/analyze-sentiment', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()