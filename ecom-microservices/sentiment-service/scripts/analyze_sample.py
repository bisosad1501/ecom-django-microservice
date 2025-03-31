#!/usr/bin/env python
"""
Script để phân tích mẫu và hiển thị kết quả phân tích cảm xúc.
Sử dụng dữ liệu mẫu để cho thấy cách hoạt động của mô hình phân tích cảm xúc.
"""

import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urljoin
import requests
from tabulate import tabulate

# Thêm thư mục gốc của dự án vào PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.sentiment_analyzer import SentimentAnalyzer
from src.config.settings import settings

def load_sample_data(file_path=None):
    """
    Tải dữ liệu mẫu cho phân tích cảm xúc
    
    Args:
        file_path (str, optional): Đường dẫn đến file CSV chứa dữ liệu
            Nếu không cung cấp, sẽ sử dụng dữ liệu mẫu có sẵn
    
    Returns:
        list: Danh sách các văn bản để phân tích
    """
    if file_path and os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df['review'].tolist()
    
    # Dữ liệu mẫu
    return [
        "This product exceeded all my expectations. The quality is outstanding!",
        "Terrible experience with this product. It broke after just one week.",
        "Product is okay. Nothing special, but it works as advertised.",
        "I've been using this for months and it's still perfect. Very satisfied with my purchase.",
        "The customer service was unhelpful and rude when I had an issue.",
        "Average product for the price point. Does the job adequately.",
        "Absolutely love this! Can't imagine using anything else now.",
        "Disappointing quality. Not worth the money at all.",
        "Works fine for what I need. No complaints but nothing impressive either.",
        "Best purchase I've made this year! Highly recommend to everyone.",
    ]

def analyze_samples(texts):
    """
    Phân tích cảm xúc cho danh sách văn bản
    
    Args:
        texts (list): Danh sách các văn bản cần phân tích
    
    Returns:
        list: Kết quả phân tích
    """
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_batch(texts)

def visualize_results(results):
    """
    Tạo các biểu đồ để hiển thị kết quả phân tích cảm xúc
    
    Args:
        results (list): Kết quả phân tích cảm xúc
    """
    # Phân loại kết quả
    sentiments = [result['sentiment'] for result in results]
    scores = [result['score'] for result in results]
    
    # Đếm số lượng mỗi loại cảm xúc
    sentiment_counts = {
        'positive': sentiments.count('positive'),
        'neutral': sentiments.count('neutral'),
        'negative': sentiments.count('negative')
    }
    
    # Tạo biểu đồ đếm
    plt.figure(figsize=(12, 10))
    
    # Biểu đồ cột cho số lượng mỗi loại cảm xúc
    plt.subplot(2, 2, 1)
    plt.bar(sentiment_counts.keys(), sentiment_counts.values(), color=['green', 'gray', 'red'])
    plt.title('Phân phối cảm xúc')
    plt.ylabel('Số lượng')
    
    # Biểu đồ tròn cho phân phối cảm xúc
    plt.subplot(2, 2, 2)
    plt.pie(sentiment_counts.values(), labels=sentiment_counts.keys(), autopct='%1.1f%%', 
            colors=['green', 'gray', 'red'], startangle=90)
    plt.title('Tỷ lệ cảm xúc')
    
    # Biểu đồ điểm cho độ tin cậy của từng phân loại
    plt.subplot(2, 1, 2)
    colors = {'positive': 'green', 'neutral': 'gray', 'negative': 'red'}
    for i, result in enumerate(results):
        plt.scatter(i, result['score'], color=colors[result['sentiment']], s=100)
    
    plt.xlabel('Mẫu')
    plt.ylabel('Điểm tin cậy')
    plt.title('Độ tin cậy của các phân loại')
    plt.xticks(range(len(results)), [f'Mẫu {i+1}' for i in range(len(results))])
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('sentiment_analysis_results.png')
    plt.show()

def display_table(results, texts):
    """
    Hiển thị kết quả phân tích cảm xúc dưới dạng bảng
    
    Args:
        results (list): Kết quả phân tích cảm xúc
        texts (list): Văn bản gốc
    """
    table_data = []
    for i, (result, text) in enumerate(zip(results, texts)):
        # Cắt văn bản nếu quá dài
        display_text = text if len(text) < 50 else text[:47] + '...'
        
        # Thêm dòng vào bảng
        table_data.append([
            i+1, 
            display_text,
            result['sentiment'],
            f"{result['score']:.4f}"
        ])
    
    # Hiển thị bảng
    headers = ['ID', 'Văn bản', 'Cảm xúc', 'Điểm tin cậy']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Hiển thị thống kê
    sentiments = [result['sentiment'] for result in results]
    print("\nTHỐNG KÊ:")
    print(f"- Số mẫu: {len(results)}")
    print(f"- Tích cực: {sentiments.count('positive')} ({sentiments.count('positive')/len(results)*100:.1f}%)")
    print(f"- Trung tính: {sentiments.count('neutral')} ({sentiments.count('neutral')/len(results)*100:.1f}%)")
    print(f"- Tiêu cực: {sentiments.count('negative')} ({sentiments.count('negative')/len(results)*100:.1f}%)")

def call_api(texts, api_url=None):
    """
    Gọi API phân tích cảm xúc thay vì sử dụng trực tiếp SentimentAnalyzer
    
    Args:
        texts (list): Danh sách các văn bản cần phân tích
        api_url (str, optional): URL của API. Nếu không cung cấp, sẽ sử dụng địa chỉ mặc định
    
    Returns:
        list: Kết quả phân tích từ API
    """
    if api_url is None:
        api_url = f"http://{settings.HOST}:{settings.PORT}/api/{settings.API_VERSION}/analyze/batch"
    
    try:
        response = requests.post(
            api_url,
            json={'texts': texts},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()['results']
        else:
            print(f"Lỗi khi gọi API: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Lỗi khi gọi API: {str(e)}")
        return None

def main():
    """
    Hàm chính của script
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Phân tích cảm xúc mẫu')
    parser.add_argument('--file', help='Đường dẫn đến file CSV chứa dữ liệu')
    parser.add_argument('--api', action='store_true', help='Sử dụng API thay vì gọi trực tiếp')
    parser.add_argument('--url', help='URL của API nếu sử dụng API')
    parser.add_argument('--no-viz', action='store_true', help='Không hiển thị biểu đồ')
    args = parser.parse_args()
    
    # Tải dữ liệu mẫu
    texts = load_sample_data(args.file)
    
    # Phân tích cảm xúc
    if args.api:
        print("Đang gọi API phân tích cảm xúc...")
        results = call_api(texts, args.url)
        if results is None:
            print("Không thể phân tích cảm xúc qua API. Đang chuyển sang phân tích trực tiếp...")
            results = analyze_samples(texts)
    else:
        print("Đang phân tích cảm xúc...")
        results = analyze_samples(texts)
    
    # Hiển thị kết quả dưới dạng bảng
    print("\nKẾT QUẢ PHÂN TÍCH CẢM XÚC:")
    display_table(results, texts)
    
    # Tạo biểu đồ
    if not args.no_viz:
        print("\nĐang tạo biểu đồ...")
        visualize_results(results)
        print(f"Biểu đồ đã được lưu thành: sentiment_analysis_results.png")

if __name__ == '__main__':
    main() 