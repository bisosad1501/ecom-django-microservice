#!/usr/bin/env python3
"""
Script tạo dữ liệu kiểm thử cho Postman.
Tạo các file JSON có kích thước khác nhau cho việc kiểm thử hiệu năng.
"""

import json
import os
import random
import uuid
from datetime import datetime, timedelta

def generate_random_text(lang="vi", sentiment="random", length="medium"):
    """
    Tạo văn bản ngẫu nhiên với ngôn ngữ và độ dài chỉ định
    """
    # Các từ cơ bản theo ngôn ngữ và cảm xúc
    words = {
        "en": {
            "positive": ["good", "great", "excellent", "amazing", "wonderful", "best", "love", "perfect", 
                         "awesome", "fantastic", "satisfied", "happy", "recommend", "positive", "superior",
                         "outstanding", "exceptional", "remarkable", "superb", "impressive"],
            "negative": ["bad", "terrible", "awful", "horrible", "worst", "poor", "disappointing", 
                         "disappointed", "hate", "dislike", "negative", "inferior", "useless", "waste",
                         "broken", "defective", "mediocre", "subpar", "avoid", "regret"],
            "neutral": ["okay", "average", "mediocre", "passable", "acceptable", "fine", "fair", 
                        "ordinary", "regular", "standard", "common", "usual", "normal", "typical"]
        },
        "vi": {
            "positive": ["tốt", "hay", "tuyệt", "vời", "xuất sắc", "đẹp", "thích", "yêu", "hài lòng", 
                        "tuyệt vời", "tốt nhất", "tuyệt hảo", "hoàn hảo", "giỏi", "hấp dẫn", "tiện lợi"],
            "negative": ["tệ", "kém", "xấu", "dở", "chán", "thất vọng", "không", "chẳng", "không thích", 
                        "không hài lòng", "không tốt", "hỏng", "lỗi", "vấn đề", "khó chịu", "gãy", "hư"],
            "neutral": ["bình thường", "tạm được", "tạm", "ổn", "không đặc biệt", "thường", "đủ", 
                        "trung bình", "cơ bản", "thông thường"]
        }
    }
    
    # Các cụm từ theo ngôn ngữ và cảm xúc
    phrases = {
        "en": {
            "positive": [
                "I really like this product.",
                "This is exactly what I needed.",
                "The quality is excellent.",
                "I would definitely buy again.",
                "This exceeded my expectations."
            ],
            "negative": [
                "I'm disappointed with this purchase.",
                "The quality is very poor.",
                "This was a waste of money.",
                "I would not recommend this.",
                "It broke after just a few uses."
            ],
            "neutral": [
                "It's an average product.",
                "It works as expected.",
                "Nothing special about it.",
                "It's okay for the price.",
                "It does the job but nothing more."
            ]
        },
        "vi": {
            "positive": [
                "Tôi rất thích sản phẩm này.",
                "Đây đúng là thứ tôi cần.",
                "Chất lượng rất tốt.",
                "Tôi chắc chắn sẽ mua lại.",
                "Sản phẩm này vượt quá mong đợi của tôi."
            ],
            "negative": [
                "Tôi thất vọng với sản phẩm này.",
                "Chất lượng rất kém.",
                "Đây là sự lãng phí tiền bạc.",
                "Tôi không khuyên dùng sản phẩm này.",
                "Nó bị hỏng sau vài lần sử dụng."
            ],
            "neutral": [
                "Đây là một sản phẩm trung bình.",
                "Nó hoạt động như mong đợi.",
                "Không có gì đặc biệt về sản phẩm này.",
                "Nó tạm ổn với giá tiền.",
                "Nó làm được việc nhưng không có gì hơn."
            ]
        }
    }
    
    # Chọn cảm xúc nếu ngẫu nhiên
    if sentiment == "random":
        sentiment = random.choice(["positive", "neutral", "negative"])
    
    # Chọn độ dài văn bản
    lengths = {
        "short": (1, 2),
        "medium": (2, 4),
        "long": (4, 8)
    }
    
    min_sentences, max_sentences = lengths.get(length, (2, 4))
    num_sentences = random.randint(min_sentences, max_sentences)
    
    # Tạo văn bản
    text = []
    
    # Thêm một cụm từ mẫu
    sample_phrase = random.choice(phrases[lang][sentiment])
    text.append(sample_phrase)
    
    # Thêm các câu ngẫu nhiên
    for _ in range(num_sentences - 1):
        # Tạo một câu với 4-10 từ
        num_words = random.randint(4, 10)
        sentence = []
        
        # 80% từ thuộc cảm xúc đã chọn, 20% từ ngẫu nhiên
        for i in range(num_words):
            if random.random() < 0.8:
                word = random.choice(words[lang][sentiment])
            else:
                random_sentiment = random.choice(list(words[lang].keys()))
                word = random.choice(words[lang][random_sentiment])
            sentence.append(word)
        
        # Ghép các từ thành câu
        if lang == "en":
            sentence_text = " ".join(sentence).capitalize() + "."
        else:  # Vietnamese
            sentence_text = " ".join(sentence).capitalize() + "."
        
        text.append(sentence_text)
    
    return " ".join(text)

def generate_reviews(num_reviews=100, output_file="test_data.json"):
    """
    Tạo dữ liệu mẫu các đánh giá sản phẩm
    """
    # Tạo danh sách sản phẩm
    products = [f"PROD{i:03d}" for i in range(1, 16)]
    
    reviews = []
    
    for i in range(num_reviews):
        # Chọn ngẫu nhiên cảm xúc
        sentiment_weights = [0.65, 0.2, 0.15]  # positive, neutral, negative
        sentiment = random.choices(["positive", "neutral", "negative"], weights=sentiment_weights)[0]
        
        # Tạo đánh giá
        product_id = random.choice(products)
        comment = generate_random_text(lang="vi", sentiment=sentiment, length="medium")
        rating = 5 if sentiment == "positive" else (3 if sentiment == "neutral" else random.randint(1, 2))
        
        # Tạo ngày trong 6 tháng gần đây
        days_ago = random.randint(0, 180)
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        review = {
            "id": str(uuid.uuid4()),
            "product_id": product_id,
            "user_id": str(uuid.uuid4()),
            "comment": comment,
            "rating": rating,
            "date": date,
            "helpful_votes": random.randint(0, 50),
            "not_helpful_votes": random.randint(0, 10),
            "attributes": {
                "quality_rating": random.randint(1, 5),
                "value_rating": random.randint(1, 5),
                "shipping_rating": random.randint(1, 5)
            }
        }
        
        reviews.append(review)
    
    # Lưu vào file
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"reviews": reviews}, f, ensure_ascii=False, indent=2)
    
    print(f"Đã tạo {num_reviews} đánh giá và lưu vào {output_path}")
    
    return reviews

def generate_batch_test_data(sizes=None, output_dir="."):
    """
    Tạo dữ liệu kiểm thử với các kích thước khác nhau
    """
    if sizes is None:
        sizes = {
            "small": 10,
            "medium": 50,
            "large": 200,
            "xlarge": 1000
        }
    
    result_files = {}
    
    for size_name, num_texts in sizes.items():
        # Tạo các văn bản
        texts = []
        for i in range(num_texts):
            lang = "vi" if random.random() < 0.8 else "en"
            sentiment = random.choice(["positive", "neutral", "negative"])
            length = random.choice(["short", "medium", "long"])
            text = generate_random_text(lang=lang, sentiment=sentiment, length=length)
            texts.append(text)
        
        # Lưu vào file
        output_file = f"batch_test_{size_name}.json"
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"texts": texts}, f, ensure_ascii=False, indent=2)
        
        result_files[size_name] = output_path
        print(f"Đã tạo {num_texts} văn bản cho {size_name} và lưu vào {output_path}")
    
    return result_files

def generate_product_test_data(num_products=10, output_file="product_test_data.json"):
    """
    Tạo dữ liệu kiểm thử cho sản phẩm
    """
    products = []
    
    for i in range(1, num_products + 1):
        product_id = f"PROD{i:03d}"
        
        # Tạo phân bố cảm xúc ngẫu nhiên
        positive = random.randint(10, 100)
        neutral = random.randint(5, 50)
        negative = random.randint(0, 30)
        total = positive + neutral + negative
        
        # Tính điểm cảm xúc tổng thể
        sentiment_score = (positive * 1.0 + neutral * 0.5) / total if total > 0 else 0.5
        
        product = {
            "product_id": product_id,
            "name": f"Sản phẩm mẫu {i}",
            "sentiment_score": round(sentiment_score, 2),
            "sentiment_distribution": {
                "positive": positive,
                "neutral": neutral,
                "negative": negative
            },
            "total_reviews": total,
            "average_rating": round(positive * 5 / total if total > 0 else 0, 1)
        }
        
        products.append(product)
    
    # Lưu vào file
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"products": products}, f, ensure_ascii=False, indent=2)
    
    print(f"Đã tạo {num_products} sản phẩm và lưu vào {output_path}")
    
    return products

if __name__ == "__main__":
    # Tạo thư mục output nếu chưa tồn tại
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Tạo dữ liệu kiểm thử
    print("--- Tạo dữ liệu kiểm thử cho Sentiment Analysis Service ---")
    
    # Tạo đánh giá
    reviews = generate_reviews(num_reviews=200, output_file="output/test_data.json")
    
    # Tạo dữ liệu batch
    batch_files = generate_batch_test_data(output_dir=output_dir)
    
    # Tạo dữ liệu sản phẩm
    products = generate_product_test_data(num_products=15, output_file="output/product_test_data.json")
    
    print("\nQuá trình tạo dữ liệu kiểm thử hoàn tất.")
    print(f"Tổng cộng đã tạo {len(reviews)} đánh giá, {sum(len(json.load(open(f))['texts']) for f in batch_files.values())} văn bản và {len(products)} sản phẩm.")
    print(f"Dữ liệu được lưu trong thư mục: {output_dir}") 