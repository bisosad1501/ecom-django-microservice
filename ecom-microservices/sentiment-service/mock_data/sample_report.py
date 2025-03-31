#!/usr/bin/env python
"""
Script tạo dữ liệu báo cáo mẫu cho dịch vụ phân tích cảm xúc.
Tạo các tệp HTML và hình ảnh để minh họa giao diện báo cáo.
"""

import os
import json
import random
import shutil
import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

def ensure_dir(directory):
    """Tạo thư mục nếu chưa tồn tại"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_sentiment_distribution_chart(output_path):
    """
    Tạo biểu đồ phân phối cảm xúc
    """
    # Dữ liệu mẫu
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [60, 25, 15]  # 60% tích cực, 25% trung tính, 15% tiêu cực
    colors = ['#4CAF50', '#FFC107', '#F44336']
    explode = (0.1, 0, 0)  # Nhấn mạnh vào phần tích cực
    
    # Tạo biểu đồ
    plt.figure(figsize=(10, 7))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Sentiment Distribution', fontsize=16)
    plt.savefig(output_path)
    plt.close()

def generate_sentiment_trend_chart(output_path, time_unit='month'):
    """
    Tạo biểu đồ xu hướng cảm xúc theo thời gian
    
    Args:
        output_path: Đường dẫn lưu biểu đồ
        time_unit: Đơn vị thời gian (month, week)
    """
    # Dữ liệu mẫu
    if time_unit == 'month':
        periods = 6
        time_labels = [(datetime.now() - timedelta(days=30*i)).strftime('%b %Y') for i in range(periods)]
        time_labels.reverse()
    else:
        periods = 10
        time_labels = [(datetime.now() - timedelta(days=7*i)).strftime('Week %W') for i in range(periods)]
        time_labels.reverse()
    
    # Dữ liệu cảm xúc theo thời gian
    # Giả lập xu hướng: bắt đầu thấp, cải thiện dần, có vài đợt biến động
    positive_trend = [30 + i*5 + random.randint(-3, 7) for i in range(periods)]
    neutral_trend = [40 - i*2 + random.randint(-5, 5) for i in range(periods)]
    negative_trend = [30 - i*3 + random.randint(-2, 5) for i in range(periods)]
    
    # Chuẩn hóa để tổng bằng 100%
    total = np.array([p + n + u for p, n, u in zip(positive_trend, negative_trend, neutral_trend)])
    positive_trend = 100 * np.array(positive_trend) / total
    neutral_trend = 100 * np.array(neutral_trend) / total
    negative_trend = 100 * np.array(negative_trend) / total
    
    # Tạo biểu đồ
    plt.figure(figsize=(12, 7))
    
    # Vẽ dạng stacked area chart
    plt.stackplot(range(periods), positive_trend, neutral_trend, negative_trend, 
                labels=['Positive', 'Neutral', 'Negative'],
                colors=['#4CAF50', '#FFC107', '#F44336'], alpha=0.7)
    
    # Thiết lập trục
    plt.xticks(range(periods), time_labels, rotation=45)
    plt.ylim(0, 100)
    plt.ylabel('Percentage (%)')
    plt.title(f'Sentiment Trend by {time_unit.capitalize()}', fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper left')
    plt.tight_layout()
    
    # Lưu biểu đồ
    plt.savefig(output_path)
    plt.close()

def generate_sentiment_by_rating_chart(output_path):
    """
    Tạo biểu đồ phân phối cảm xúc theo đánh giá sao
    """
    # Dữ liệu mẫu
    ratings = [1, 2, 3, 4, 5]
    
    # Phân phối cảm xúc cho từng mức đánh giá
    positive = [5, 10, 30, 70, 90]  # % tích cực
    neutral = [10, 20, 50, 20, 8]   # % trung tính
    negative = [85, 70, 20, 10, 2]  # % tiêu cực
    
    # Thiết lập biểu đồ
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Vẽ biểu đồ cột chồng
    bar_width = 0.7
    ax.bar(ratings, positive, bar_width, label='Positive', color='#4CAF50')
    ax.bar(ratings, neutral, bar_width, bottom=positive, label='Neutral', color='#FFC107')
    ax.bar(ratings, negative, bar_width, bottom=np.array(positive) + np.array(neutral),
          label='Negative', color='#F44336')
    
    # Thêm nhãn cho mỗi cột
    for i, r in enumerate(ratings):
        ax.text(r, 103, f"{r} ★", ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Thiết lập trục
    ax.set_xticks(ratings)
    ax.set_xticklabels([])
    ax.set_xlabel('Rating', fontsize=12)
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_ylim(0, 110)
    ax.set_title('Sentiment Distribution by Rating', fontsize=16)
    ax.legend()
    
    # Thêm lưới
    ax.grid(True, axis='y', alpha=0.3)
    
    # Lưu biểu đồ
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def generate_product_comparison_chart(output_path):
    """
    Tạo biểu đồ so sánh sản phẩm
    """
    # Dữ liệu mẫu
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    positive = [75, 45, 60, 55, 80]
    neutral = [15, 25, 30, 25, 15]
    negative = [10, 30, 10, 20, 5]
    
    # Tính toán sentiment score
    sentiment_score = [(p - n) / 100 for p, n in zip(positive, negative)]
    
    # Thiết lập biểu đồ
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Biểu đồ 1: Phân phối cảm xúc
    bar_width = 0.6
    x = np.arange(len(products))
    
    ax1.bar(x, positive, bar_width, label='Positive', color='#4CAF50')
    ax1.bar(x, neutral, bar_width, bottom=positive, label='Neutral', color='#FFC107')
    ax1.bar(x, negative, bar_width, bottom=np.array(positive) + np.array(neutral),
           label='Negative', color='#F44336')
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(products, rotation=45, ha='right')
    ax1.set_ylabel('Percentage (%)')
    ax1.set_title('Sentiment Distribution by Product')
    ax1.legend()
    ax1.grid(True, axis='y', alpha=0.3)
    
    # Biểu đồ 2: Sentiment score
    colors = ['#4CAF50' if s > 0.5 else '#FFC107' if s > 0 else '#F44336' for s in sentiment_score]
    ax2.bar(x, sentiment_score, color=colors)
    
    # Thêm nhãn giá trị
    for i, score in enumerate(sentiment_score):
        ax2.text(i, score + 0.02, f"{score:.2f}", ha='center', va='bottom')
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(products, rotation=45, ha='right')
    ax2.set_ylim(-1, 1)
    ax2.set_ylabel('Sentiment Score (-1 to 1)')
    ax2.set_title('Sentiment Score by Product')
    ax2.grid(True, axis='y', alpha=0.3)
    
    # Lưu biểu đồ
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def generate_top_products_data():
    """
    Tạo dữ liệu cho top sản phẩm
    """
    product_ids = ['p001', 'p002', 'p003', 'p004', 'p005', 'p006', 'p007', 'p008', 'p009', 'p010']
    product_names = [
        'Premium Wireless Headphones',
        'Smart Fitness Tracker',
        'Ultra HD 4K Monitor',
        'Professional Camera Lens',
        'Ergonomic Office Chair',
        'Multi-function Blender',
        'Portable Power Bank',
        'Gaming Mechanical Keyboard',
        'Smart Home Speaker',
        'Designer Desk Lamp'
    ]
    
    top_products = []
    
    for i, (pid, name) in enumerate(zip(product_ids, product_names)):
        # Tạo dữ liệu giả với các xu hướng khác nhau
        sentiment_score = round(0.85 - i * 0.06 + random.uniform(-0.05, 0.05), 2)
        
        positive = int(60 + (0.85 - sentiment_score) * 100)
        negative = int(10 + (0.85 - sentiment_score) * 50)
        neutral = 100 - positive - negative
        
        # Đảm bảo tỷ lệ hợp lý
        positive = max(0, min(positive, 100))
        negative = max(0, min(negative, 100))
        neutral = max(0, min(neutral, 100))
        
        # Điều chỉnh để tổng bằng 100%
        total = positive + neutral + negative
        if total != 100:
            neutral += (100 - total)
        
        # Lượng đánh giá giảm dần theo thứ hạng
        total_reviews = 100 - i * 7 + random.randint(-5, 10)
        
        top_products.append({
            'product_id': pid,
            'product_name': name,
            'sentiment_score': sentiment_score,
            'total_reviews': total_reviews,
            'positive': int(total_reviews * positive / 100),
            'neutral': int(total_reviews * neutral / 100),
            'negative': int(total_reviews * negative / 100),
            'positive_pct': positive,
            'neutral_pct': neutral,
            'negative_pct': negative,
            'avg_rating': round(3.5 + sentiment_score, 1)
        })
    
    return top_products

def generate_top_products_html(data, output_file):
    """
    Tạo file HTML cho top sản phẩm
    """
    with open(output_file, 'w') as f:
        f.write('<html><head><title>Top Products by Sentiment</title>')
        f.write('<style>body{font-family:Arial,sans-serif;margin:20px;} table{border-collapse:collapse;width:100%;} th,td{text-align:left;padding:8px;border-bottom:1px solid #ddd;} tr:nth-child(even){background-color:#f2f2f2;} th{background-color:#4CAF50;color:white;}</style>')
        f.write('</head><body>')
        f.write('<h1>Top Products by Sentiment Score</h1>')
        
        f.write('<table>')
        f.write('<tr><th>Product ID</th><th>Product Name</th><th>Sentiment Score</th><th>Avg Rating</th><th>Total Reviews</th><th>Positive</th><th>Neutral</th><th>Negative</th></tr>')
        
        for product in data:
            f.write(f'<tr>')
            f.write(f'<td>{product["product_id"]}</td>')
            f.write(f'<td>{product["product_name"]}</td>')
            f.write(f'<td>{product["sentiment_score"]:.2f}</td>')
            f.write(f'<td>{product["avg_rating"]:.1f}</td>')
            f.write(f'<td>{product["total_reviews"]}</td>')
            f.write(f'<td>{product["positive"]} ({product["positive_pct"]}%)</td>')
            f.write(f'<td>{product["neutral"]} ({product["neutral_pct"]}%)</td>')
            f.write(f'<td>{product["negative"]} ({product["negative_pct"]}%)</td>')
            f.write(f'</tr>')
        
        f.write('</table>')
        f.write('<p>Generated on: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '</p>')
        f.write('</body></html>')

def generate_product_report(product_id, product_name, output_dir):
    """
    Tạo báo cáo chi tiết cho một sản phẩm
    """
    # Tạo thư mục cho sản phẩm
    product_dir = os.path.join(output_dir, 'products', product_id)
    ensure_dir(product_dir)
    
    # Tạo các biểu đồ
    generate_sentiment_distribution_chart(os.path.join(product_dir, 'sentiment_distribution.png'))
    generate_sentiment_trend_chart(os.path.join(product_dir, 'sentiment_trend.png'), 'month')
    
    # Tính toán các số liệu cho sản phẩm này
    # Tạo dữ liệu khác nhau cho từng sản phẩm dựa trên ID
    seed = sum(ord(c) for c in product_id)
    random.seed(seed)
    
    total_reviews = random.randint(50, 150)
    positive_pct = random.randint(40, 80)
    negative_pct = random.randint(5, 25)
    neutral_pct = 100 - positive_pct - negative_pct
    
    sentiment_score = (positive_pct - negative_pct) / 100
    avg_rating = 3.0 + sentiment_score * 2
    
    # Tạo file HTML
    with open(os.path.join(product_dir, 'summary.html'), 'w') as f:
        f.write(f'<html><head><title>Sentiment Analysis for Product {product_id}</title>')
        f.write('<style>body{font-family:Arial,sans-serif;margin:20px;} .metric{font-size:24px;font-weight:bold;} .card{border:1px solid #ddd;border-radius:5px;padding:15px;margin-bottom:15px;} table{border-collapse:collapse;width:100%;} th,td{text-align:left;padding:8px;border-bottom:1px solid #ddd;} th{background-color:#4CAF50;color:white;}</style>')
        f.write('</head><body>')
        f.write(f'<h1>Sentiment Analysis Report for Product {product_id}</h1>')
        f.write('<div class="card">')
        f.write('<h2>Summary</h2>')
        f.write('<table>')
        f.write(f'<tr><td>Product Name:</td><td class="metric">{product_name}</td></tr>')
        f.write(f'<tr><td>Total Reviews:</td><td class="metric">{total_reviews}</td></tr>')
        f.write(f'<tr><td>Sentiment Score:</td><td class="metric">{sentiment_score:.2f}</td></tr>')
        f.write(f'<tr><td>Average Rating:</td><td class="metric">{avg_rating:.1f}</td></tr>')
        f.write('</table>')
        f.write('</div>')
        
        f.write('<div class="card">')
        f.write('<h2>Sentiment Distribution</h2>')
        f.write('<table>')
        f.write('<tr><th>Sentiment</th><th>Count</th><th>Percentage</th></tr>')
        f.write(f'<tr><td>Positive</td><td>{int(total_reviews * positive_pct / 100)}</td><td>{positive_pct:.1f}%</td></tr>')
        f.write(f'<tr><td>Neutral</td><td>{int(total_reviews * neutral_pct / 100)}</td><td>{neutral_pct:.1f}%</td></tr>')
        f.write(f'<tr><td>Negative</td><td>{int(total_reviews * negative_pct / 100)}</td><td>{negative_pct:.1f}%</td></tr>')
        f.write('</table>')
        f.write('</div>')
        
        f.write('<div class="card">')
        f.write('<h2>Visualizations</h2>')
        f.write('<p>Sentiment Distribution:</p>')
        f.write(f'<img src="sentiment_distribution.png" alt="Sentiment Distribution" style="max-width:100%">')
        f.write('<p>Sentiment Trend Over Time:</p>')
        f.write(f'<img src="sentiment_trend.png" alt="Sentiment Trend" style="max-width:100%">')
        f.write('</div>')
        
        f.write('<p>Generated on: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '</p>')
        f.write('</body></html>')

def generate_index_page(output_dir, product_ids, product_names):
    """
    Tạo trang index
    """
    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write('<html><head><title>Sentiment Analysis Reports</title>')
        f.write('<style>body{font-family:Arial,sans-serif;margin:20px;} .card{border:1px solid #ddd;border-radius:5px;padding:15px;margin-bottom:15px;} img{max-width:100%;height:auto;border:1px solid #ddd;}</style>')
        f.write('</head><body>')
        f.write('<h1>Sentiment Analysis Reports</h1>')
        
        # Overall reports
        f.write('<div class="card">')
        f.write('<h2>Overall Sentiment Analysis</h2>')
        
        # Hiển thị các biểu đồ tổng quan
        f.write('<p>Sentiment Distribution:</p>')
        f.write('<img src="sentiment_distribution.png" alt="Sentiment Distribution">')
        
        f.write('<p>Sentiment Trend by Month:</p>')
        f.write('<img src="sentiment_trend_by_month.png" alt="Monthly Sentiment Trend">')
        
        if os.path.exists(os.path.join(output_dir, 'sentiment_trend_by_week.png')):
            f.write('<p>Sentiment Trend by Week:</p>')
            f.write('<img src="sentiment_trend_by_week.png" alt="Weekly Sentiment Trend">')
        
        f.write('<p>Sentiment by Rating:</p>')
        f.write('<img src="sentiment_by_rating.png" alt="Sentiment by Rating">')
        
        if os.path.exists(os.path.join(output_dir, 'top_products.html')):
            f.write('<p>Top Products by Sentiment: <a href="top_products.html">View Details</a></p>')
        
        f.write('</div>')
        
        # Product comparison
        if os.path.exists(os.path.join(output_dir, 'product_comparison.png')):
            f.write('<div class="card">')
            f.write('<h2>Product Comparison</h2>')
            f.write('<img src="product_comparison.png" alt="Product Comparison">')
            f.write('</div>')
        
        # Links to product reports
        f.write('<div class="card">')
        f.write('<h2>Product Reports</h2>')
        f.write('<ul>')
        
        for pid, name in zip(product_ids, product_names):
            f.write(f'<li><a href="products/{pid}/summary.html">Product {pid}: {name}</a></li>')
        
        f.write('</ul>')
        f.write('</div>')
        
        f.write('<p>Generated on: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '</p>')
        f.write('</body></html>')

def main():
    parser = argparse.ArgumentParser(description='Generate sample sentiment report data')
    parser.add_argument('--output', help='Output directory', default='reports/sentiment_sample')
    args = parser.parse_args()
    
    # Tạo thư mục đầu ra
    output_dir = args.output
    ensure_dir(output_dir)
    ensure_dir(os.path.join(output_dir, 'products'))
    
    print(f"Generating sample report data to {output_dir}...")
    
    # Tạo các biểu đồ tổng quan
    generate_sentiment_distribution_chart(os.path.join(output_dir, 'sentiment_distribution.png'))
    generate_sentiment_trend_chart(os.path.join(output_dir, 'sentiment_trend_by_month.png'), 'month')
    generate_sentiment_trend_chart(os.path.join(output_dir, 'sentiment_trend_by_week.png'), 'week')
    generate_sentiment_by_rating_chart(os.path.join(output_dir, 'sentiment_by_rating.png'))
    generate_product_comparison_chart(os.path.join(output_dir, 'product_comparison.png'))
    
    # Tạo dữ liệu top sản phẩm
    top_products = generate_top_products_data()
    generate_top_products_html(top_products, os.path.join(output_dir, 'top_products.html'))
    
    # Lưu dữ liệu top sản phẩm dưới dạng CSV
    with open(os.path.join(output_dir, 'top_products.csv'), 'w') as f:
        f.write('product_id,product_name,sentiment_score,total_reviews,positive,neutral,negative,positive_pct,neutral_pct,negative_pct,avg_rating\n')
        for p in top_products:
            f.write(f"{p['product_id']},{p['product_name']},{p['sentiment_score']},{p['total_reviews']},{p['positive']},{p['neutral']},{p['negative']},{p['positive_pct']},{p['neutral_pct']},{p['negative_pct']},{p['avg_rating']}\n")
    
    # Lấy 5 sản phẩm đầu tiên để tạo báo cáo chi tiết
    selected_products = [(p['product_id'], p['product_name']) for p in top_products[:5]]
    
    # Tạo báo cáo cho từng sản phẩm
    for pid, name in selected_products:
        print(f"  Generating report for product {pid}...")
        generate_product_report(pid, name, output_dir)
    
    # Tạo trang index
    product_ids = [p[0] for p in selected_products]
    product_names = [p[1] for p in selected_products]
    generate_index_page(output_dir, product_ids, product_names)
    
    print(f"Sample report generation complete. View at {output_dir}/index.html")

if __name__ == '__main__':
    main() 