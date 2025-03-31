#!/usr/bin/env python
"""
Script tạo báo cáo phân tích cảm xúc từ dữ liệu review.
Tạo các biểu đồ và báo cáo chi tiết về phân phối cảm xúc, xu hướng theo thời gian, và so sánh sản phẩm.
"""

import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from tabulate import tabulate
from datetime import datetime, timedelta

# Thêm thư mục gốc của dự án vào PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analytics.sentiment_trends import SentimentTrendAnalyzer
from src.services.sentiment_analyzer import SentimentAnalyzer
from src.services.review_client import ReviewClient

def load_data_from_api(product_ids=None, limit=100):
    """
    Tải dữ liệu từ API
    
    Args:
        product_ids (list, optional): Danh sách ID sản phẩm
        limit (int): Số lượng reviews tối đa cho mỗi sản phẩm
    
    Returns:
        list: Danh sách reviews đã phân tích cảm xúc
    """
    print("Đang tải dữ liệu từ API...")
    
    client = ReviewClient()
    sentiment_analyzer = SentimentAnalyzer()
    
    all_reviews = []
    
    if product_ids:
        for product_id in product_ids:
            print(f"Đang tải reviews cho sản phẩm {product_id}...")
            
            # Lấy reviews từ service
            product_reviews = client.get_product_reviews(product_id, limit=limit)
            reviews = product_reviews.get('results', [])
            
            # Phân tích cảm xúc
            if reviews:
                print(f"Đang phân tích cảm xúc cho {len(reviews)} reviews...")
                analyzed_reviews = sentiment_analyzer.analyze_reviews(reviews)
                all_reviews.extend(analyzed_reviews)
    else:
        # Nếu không có ID sản phẩm cụ thể, lấy từ list_products API (nếu có)
        try:
            # Đoạn code giả định rằng có endpoint để lấy danh sách sản phẩm
            # Trong thực tế, bạn cần triển khai endpoint này
            print("Đang lấy danh sách sản phẩm...")
            # products = client.list_products(limit=10)
            products = [] # Thay bằng API call thực tế
            
            for product in products:
                product_id = product.get('id')
                if product_id:
                    product_reviews = client.get_product_reviews(product_id, limit=limit)
                    reviews = product_reviews.get('results', [])
                    
                    if reviews:
                        analyzed_reviews = sentiment_analyzer.analyze_reviews(reviews)
                        all_reviews.extend(analyzed_reviews)
        except Exception as e:
            print(f"Lỗi khi lấy danh sách sản phẩm: {str(e)}")
            print("Sử dụng dữ liệu mẫu thay thế.")
            all_reviews = load_sample_data()
    
    print(f"Đã tải tổng cộng {len(all_reviews)} reviews.")
    return all_reviews

def load_sample_data():
    """
    Tạo dữ liệu mẫu để kiểm thử
    
    Returns:
        list: Danh sách reviews mẫu
    """
    print("Đang tạo dữ liệu mẫu...")
    
    # Các ID sản phẩm mẫu
    product_ids = ['p001', 'p002', 'p003', 'p004', 'p005']
    
    # Tạo dữ liệu mẫu
    sample_data = []
    
    sentiment_analyzer = SentimentAnalyzer()
    
    # Tạo các reviews với phân phối cảm xúc khác nhau cho mỗi sản phẩm
    for p_idx, product_id in enumerate(product_ids):
        # Số lượng reviews cho mỗi sản phẩm
        n_reviews = 20 + p_idx * 10
        
        # Tạo reviews cho sản phẩm này
        for i in range(n_reviews):
            # Tạo review theo kiểu có xu hướng khác nhau cho các sản phẩm khác nhau
            if p_idx == 0:  # Sản phẩm đầu tiên chủ yếu tích cực
                comment = f"This is a great product! I love it. Review {i+1}"
            elif p_idx == 1:  # Sản phẩm thứ hai khá tiêu cực
                comment = f"This product is disappointing. Not worth the money. Review {i+1}"
            elif p_idx == 2:  # Sản phẩm thứ ba trung tính
                comment = f"Product is okay. Nothing special. Just works as expected. Review {i+1}"
            elif p_idx == 3:  # Sản phẩm thứ tư phân phối đều
                if i % 3 == 0:
                    comment = f"Great quality and service! Very satisfied. Review {i+1}"
                elif i % 3 == 1:
                    comment = f"Terrible experience, would not recommend. Review {i+1}"
                else:
                    comment = f"Average product, does the job. Review {i+1}"
            else:  # Sản phẩm thứ năm có xu hướng thay đổi theo thời gian
                time_factor = i / n_reviews
                if time_factor < 0.3:
                    comment = f"Early review: Not that good, needs improvement. Review {i+1}"
                elif time_factor < 0.7:
                    comment = f"Getting better after updates. Decent product now. Review {i+1}"
                else:
                    comment = f"After recent changes, this product is excellent! Highly recommend. Review {i+1}"
            
            # Phân tích cảm xúc
            sentiment_result = sentiment_analyzer.analyze_text(comment)
            
            # Tạo ngày ngẫu nhiên trong 6 tháng qua
            days_ago = int(180 * (1 - i/n_reviews))  # Ngày xa nhất cho review đầu tiên
            created_at = (datetime.now() - timedelta(days=days_ago)).isoformat()
            
            # Xây dựng review
            review = {
                'id': f"{product_id}_review_{i+1}",
                'product_id': product_id,
                'user_id': f"user_{(i * 13) % 50 + 1:03d}",  # User ID giả
                'rating': min(5, max(1, int(sentiment_result['score'] * 5) + 1)),  # Rating 1-5 dựa trên cảm xúc
                'title': f"Review {i+1} for product {product_id}",
                'comment': comment,
                'created_at': created_at,
                'sentiment': {
                    'label': sentiment_result['sentiment'],
                    'score': sentiment_result['score']
                }
            }
            
            sample_data.append(review)
    
    print(f"Đã tạo {len(sample_data)} reviews mẫu cho {len(product_ids)} sản phẩm.")
    return sample_data

def generate_overall_report(trend_analyzer, output_dir):
    """
    Tạo báo cáo tổng quan về cảm xúc
    
    Args:
        trend_analyzer (SentimentTrendAnalyzer): Bộ phân tích xu hướng
        output_dir (str): Thư mục lưu báo cáo
    """
    print("Đang tạo báo cáo tổng quan...")
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Phân phối cảm xúc
    print("- Tạo biểu đồ phân phối cảm xúc...")
    fig = trend_analyzer.plot_sentiment_distribution()
    plt.savefig(os.path.join(output_dir, 'sentiment_distribution.png'))
    plt.close(fig)
    
    # 2. Xu hướng cảm xúc theo thời gian
    print("- Tạo biểu đồ xu hướng cảm xúc theo thời gian...")
    fig = trend_analyzer.plot_sentiment_over_time(time_unit='month')
    plt.savefig(os.path.join(output_dir, 'sentiment_trend_by_month.png'))
    plt.close(fig)
    
    try:
        fig = trend_analyzer.plot_sentiment_over_time(time_unit='week')
        plt.savefig(os.path.join(output_dir, 'sentiment_trend_by_week.png'))
        plt.close(fig)
    except Exception as e:
        print(f"  Lỗi khi tạo biểu đồ xu hướng theo tuần: {str(e)}")
    
    # 3. Phân tích cảm xúc theo rating
    print("- Tạo biểu đồ cảm xúc theo rating...")
    fig = trend_analyzer.plot_sentiment_by_rating()
    plt.savefig(os.path.join(output_dir, 'sentiment_by_rating.png'))
    plt.close(fig)
    
    # 4. Top sản phẩm theo điểm cảm xúc
    print("- Tạo danh sách top sản phẩm...")
    top_products = trend_analyzer.get_top_products(n=10)
    
    if not top_products.empty:
        # Lưu danh sách top sản phẩm
        top_products.to_csv(os.path.join(output_dir, 'top_products.csv'), index=False)
        
        # Tạo file HTML với kết quả
        with open(os.path.join(output_dir, 'top_products.html'), 'w') as f:
            f.write('<html><head><title>Top Products by Sentiment</title>')
            f.write('<style>table {border-collapse: collapse; width: 100%;} th, td {text-align: left; padding: 8px; border-bottom: 1px solid #ddd;} tr:nth-child(even) {background-color: #f2f2f2;} th {background-color: #4CAF50; color: white;}</style>')
            f.write('</head><body>')
            f.write('<h1>Top Products by Sentiment Score</h1>')
            f.write(top_products.to_html(index=False))
            f.write('<p>Generated on: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '</p>')
            f.write('</body></html>')
    
    print(f"Báo cáo tổng quan đã được lưu vào thư mục: {output_dir}")

def generate_product_reports(trend_analyzer, product_ids, output_dir):
    """
    Tạo báo cáo riêng cho từng sản phẩm
    
    Args:
        trend_analyzer (SentimentTrendAnalyzer): Bộ phân tích xu hướng
        product_ids (list): Danh sách ID sản phẩm
        output_dir (str): Thư mục lưu báo cáo
    """
    print("Đang tạo báo cáo cho từng sản phẩm...")
    
    # Thư mục lưu báo cáo chi tiết
    product_dir = os.path.join(output_dir, 'products')
    os.makedirs(product_dir, exist_ok=True)
    
    # So sánh các sản phẩm
    print("- Tạo biểu đồ so sánh giữa các sản phẩm...")
    fig = trend_analyzer.plot_product_comparison(product_ids)
    plt.savefig(os.path.join(output_dir, 'product_comparison.png'))
    plt.close(fig)
    
    # Phân tích chi tiết cho từng sản phẩm
    comparison_data = trend_analyzer.compare_products(product_ids)
    
    for product_id in product_ids:
        if product_id not in comparison_data:
            print(f"  Không có dữ liệu cho sản phẩm {product_id}, bỏ qua...")
            continue
        
        print(f"- Đang tạo báo cáo cho sản phẩm {product_id}...")
        
        # Tạo thư mục cho sản phẩm
        product_subdir = os.path.join(product_dir, product_id)
        os.makedirs(product_subdir, exist_ok=True)
        
        # Lọc dữ liệu cho sản phẩm này
        product_data = trend_analyzer.df[trend_analyzer.df['product_id'] == product_id].copy()
        
        if product_data.empty:
            print(f"  Không có dữ liệu cho sản phẩm {product_id}, bỏ qua...")
            continue
        
        # Tạo analyzer mới chỉ với dữ liệu của sản phẩm này
        product_analyzer = SentimentTrendAnalyzer()
        product_analyzer.df = product_data
        
        # 1. Phân phối cảm xúc
        try:
            fig = product_analyzer.plot_sentiment_distribution()
            plt.savefig(os.path.join(product_subdir, 'sentiment_distribution.png'))
            plt.close(fig)
        except Exception as e:
            print(f"  Lỗi khi tạo biểu đồ phân phối cảm xúc: {str(e)}")
        
        # 2. Xu hướng cảm xúc theo thời gian
        try:
            fig = product_analyzer.plot_sentiment_over_time(
                time_unit='month', 
                title=f'Xu hướng cảm xúc cho sản phẩm {product_id}'
            )
            plt.savefig(os.path.join(product_subdir, 'sentiment_trend.png'))
            plt.close(fig)
        except Exception as e:
            print(f"  Lỗi khi tạo biểu đồ xu hướng cảm xúc: {str(e)}")
        
        # 3. Tạo file báo cáo tổng quan cho sản phẩm
        product_stats = comparison_data[product_id]
        
        with open(os.path.join(product_subdir, 'summary.html'), 'w') as f:
            f.write(f'<html><head><title>Sentiment Analysis for Product {product_id}</title>')
            f.write('<style>body{font-family:Arial,sans-serif;margin:20px;} .metric{font-size:24px;font-weight:bold;} .card{border:1px solid #ddd;border-radius:5px;padding:15px;margin-bottom:15px;} table{border-collapse:collapse;width:100%;} th,td{text-align:left;padding:8px;border-bottom:1px solid #ddd;} th{background-color:#4CAF50;color:white;}</style>')
            f.write('</head><body>')
            f.write(f'<h1>Sentiment Analysis Report for Product {product_id}</h1>')
            f.write('<div class="card">')
            f.write('<h2>Summary</h2>')
            f.write('<table>')
            f.write(f'<tr><td>Total Reviews:</td><td class="metric">{product_stats["total_reviews"]}</td></tr>')
            f.write(f'<tr><td>Sentiment Score:</td><td class="metric">{product_stats["sentiment_score"]:.2f}</td></tr>')
            f.write(f'<tr><td>Average Rating:</td><td class="metric">{product_stats["avg_rating"]:.1f}</td></tr>')
            f.write('</table>')
            f.write('</div>')
            
            f.write('<div class="card">')
            f.write('<h2>Sentiment Distribution</h2>')
            f.write('<table>')
            f.write('<tr><th>Sentiment</th><th>Count</th><th>Percentage</th></tr>')
            f.write(f'<tr><td>Positive</td><td>{product_stats["positive"]}</td><td>{product_stats["positive_pct"]:.1f}%</td></tr>')
            f.write(f'<tr><td>Neutral</td><td>{product_stats["neutral"]}</td><td>{product_stats["neutral_pct"]:.1f}%</td></tr>')
            f.write(f'<tr><td>Negative</td><td>{product_stats["negative"]}</td><td>{product_stats["negative_pct"]:.1f}%</td></tr>')
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
    
    print(f"Báo cáo sản phẩm đã được lưu vào thư mục: {product_dir}")

def generate_index_page(output_dir):
    """
    Tạo trang index để dễ dàng xem tất cả báo cáo
    
    Args:
        output_dir (str): Thư mục lưu báo cáo
    """
    print("Đang tạo trang index...")
    
    # Tạo file index.html
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
        product_dir = os.path.join(output_dir, 'products')
        if os.path.exists(product_dir):
            f.write('<div class="card">')
            f.write('<h2>Product Reports</h2>')
            f.write('<ul>')
            
            for product_id in os.listdir(product_dir):
                product_subdir = os.path.join(product_dir, product_id)
                if os.path.isdir(product_subdir) and os.path.exists(os.path.join(product_subdir, 'summary.html')):
                    f.write(f'<li><a href="products/{product_id}/summary.html">Product {product_id}</a></li>')
            
            f.write('</ul>')
            f.write('</div>')
        
        f.write('<p>Generated on: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '</p>')
        f.write('</body></html>')
    
    print(f"Trang index đã được tạo: {os.path.join(output_dir, 'index.html')}")

def main():
    parser = argparse.ArgumentParser(description='Tạo báo cáo phân tích cảm xúc')
    parser.add_argument('--output', help='Thư mục lưu báo cáo', default='sentiment_reports')
    parser.add_argument('--product-ids', help='Danh sách ID sản phẩm, cách nhau bởi dấu phẩy')
    parser.add_argument('--use-sample', action='store_true', help='Sử dụng dữ liệu mẫu thay vì tải từ API')
    parser.add_argument('--limit', type=int, default=100, help='Số lượng reviews tối đa cho mỗi sản phẩm')
    args = parser.parse_args()
    
    # Chuyển đổi chuỗi ID sản phẩm thành list
    product_ids = args.product_ids.split(',') if args.product_ids else None
    
    # Tải dữ liệu
    if args.use_sample:
        reviews = load_sample_data()
    else:
        reviews = load_data_from_api(product_ids, args.limit)
    
    if not reviews:
        print("Không có dữ liệu reviews, không thể tạo báo cáo.")
        return
    
    # Khởi tạo trend analyzer
    trend_analyzer = SentimentTrendAnalyzer(reviews)
    
    # Lấy danh sách các ID sản phẩm từ dữ liệu nếu không được chỉ định
    if not product_ids:
        if trend_analyzer.df is not None and 'product_id' in trend_analyzer.df.columns:
            product_ids = trend_analyzer.df['product_id'].unique().tolist()
        else:
            product_ids = []
    
    # Tạo các báo cáo
    generate_overall_report(trend_analyzer, args.output)
    
    if product_ids:
        generate_product_reports(trend_analyzer, product_ids, args.output)
    
    generate_index_page(args.output)
    
    print(f"\nBáo cáo đã được tạo thành công trong thư mục: {args.output}")
    print(f"Mở file {os.path.join(args.output, 'index.html')} để xem báo cáo.")

if __name__ == '__main__':
    main() 