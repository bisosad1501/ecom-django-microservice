#!/usr/bin/env python
"""
Script để kiểm tra mô hình transformer
"""

import sys
import os
import time

# Thêm thư mục gốc vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.sentiment_model import SentimentModel

def test_model():
    """
    Test mô hình transformer với một số câu đánh giá mẫu
    """
    print("Initializing sentiment model...")
    model = SentimentModel()
    
    # Kiểm tra mô hình đã load chưa
    if model.model_loaded and not model.use_fallback:
        print(f"Transformer model loaded successfully: {model.model_name}")
    else:
        print("Warning: Using fallback rule-based model")
    
    # Một số đánh giá mẫu tích cực, tiêu cực và trung tính
    test_texts = [
        "This product is amazing, I absolutely love it!",
        "The quality is terrible, I'm very disappointed.",
        "It's okay, not great but not terrible either.",
        "Best purchase I've ever made, highly recommend it!",
        "Waste of money, don't buy this product.",
        "Shipping was fast but the product is average.",
        "I've been using this for a month and it works well.",
        "The customer service was unhelpful and rude.",
        "This is exactly what I expected, no complaints.",
        "Not worth the price, there are better alternatives."
    ]
    
    # Phân tích cảm xúc hàng loạt
    print("\nBatch prediction:")
    start_time = time.time()
    batch_results = model.batch_predict(test_texts)
    batch_time = time.time() - start_time
    
    # Hiển thị kết quả
    for i, result in enumerate(batch_results):
        text = test_texts[i]
        sentiment = result['sentiment']
        score = result['score']
        
        # Hiển thị với màu sắc (nếu có thể)
        if sentiment == 'positive':
            sentiment_display = f"\033[92m{sentiment}\033[0m"  # green
        elif sentiment == 'negative':
            sentiment_display = f"\033[91m{sentiment}\033[0m"  # red
        else:
            sentiment_display = f"\033[93m{sentiment}\033[0m"  # yellow
        
        print(f"Text: \"{text}\"")
        print(f"Sentiment: {sentiment_display}")
        print(f"Confidence: {score:.4f}")
        print("-" * 80)
    
    print(f"\nBatch processing time: {batch_time:.4f} seconds for {len(test_texts)} texts")
    print(f"Average time per text: {batch_time/len(test_texts):.4f} seconds")
    
    # So sánh kết quả với phân tích từng câu
    print("\nComparing with individual analysis...")
    start_time = time.time()
    individual_results = [model.predict(text) for text in test_texts]
    individual_time = time.time() - start_time
    
    print(f"Individual processing time: {individual_time:.4f} seconds")
    print(f"Batch processing is {individual_time/batch_time:.2f}x faster")

if __name__ == "__main__":
    test_model() 