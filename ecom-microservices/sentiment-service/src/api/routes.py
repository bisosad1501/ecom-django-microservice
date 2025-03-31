from flask import Blueprint, request, jsonify, send_from_directory
from src.services.sentiment_analyzer import SentimentAnalyzer
from src.api.schemas import SentimentRequest, ProductReviewsRequest
from src.analytics.sentiment_trends import SentimentTrendAnalyzer
from typing import Dict, Any, List
import os
import tempfile
import subprocess

# Khởi tạo Blueprint
api_bp = Blueprint('api', __name__)

# Khởi tạo analyzer
sentiment_analyzer = SentimentAnalyzer()

@api_bp.route('/health', methods=['GET'])
def health_check() -> Dict[str, str]:
    """
    Endpoint kiểm tra trạng thái của service
    
    Returns:
        Dict[str, str]: Thông tin trạng thái
    """
    return jsonify({'status': 'ok', 'service': 'sentiment-service'})

@api_bp.route('/analyze', methods=['POST'])
def analyze_text() -> Dict[str, Any]:
    """
    Endpoint phân tích cảm xúc của đoạn văn bản
    
    Request body:
        {
            "text": "Đoạn văn bản cần phân tích"
        }
    
    Returns:
        Dict[str, Any]: Kết quả phân tích cảm xúc
    """
    data = request.get_json()
    
    # Validate dữ liệu
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text parameter'}), 400
    
    # Phân tích cảm xúc
    result = sentiment_analyzer.analyze_text(data['text'])
    
    return jsonify(result)

@api_bp.route('/analyze_batch', methods=['POST'])
def analyze_batch():
    """
    Endpoint phân tích cảm xúc cho nhiều đoạn văn bản
    
    Request Body:
        texts (list): Danh sách các đoạn văn bản cần phân tích
    
    Returns:
        Dict[str, Any]: Kết quả phân tích cảm xúc cho từng văn bản
    """
    data = request.get_json()
    texts = data.get('texts', [])
    
    if not texts or not isinstance(texts, list):
        return jsonify({"error": "Invalid or missing 'texts' parameter. Must be a non-empty array."}), 400
    
    results = []
    for text in texts:
        result = sentiment_analyzer.analyze_text(text)
        results.append(result)
    
    return jsonify({"results": results})

@api_bp.route('/product/<product_id>/sentiment', methods=['GET'])
def analyze_product_reviews(product_id: str) -> Dict[str, Any]:
    """
    Endpoint phân tích cảm xúc cho reviews của một sản phẩm
    
    Args:
        product_id (str): ID của sản phẩm
    
    Query parameters:
        limit (int, optional): Số lượng reviews tối đa. Mặc định là 100.
    
    Returns:
        Dict[str, Any]: Kết quả phân tích cảm xúc bao gồm phân phối cảm xúc và danh sách reviews đã phân tích
    """
    limit = request.args.get('limit', default=100, type=int)
    
    # Phân tích cảm xúc
    result = sentiment_analyzer.analyze_product_reviews(product_id, limit=limit)
    
    # Chuẩn hóa kết quả để phù hợp với các client
    response = {
        "product_id": product_id,
        "sentiment_score": result.get("overall_score", 0.5),
        "sentiment_distribution": result.get("sentiment_distribution", {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }),
        "reviews": result.get("reviews", []),
        "overall_sentiment": result.get("overall_sentiment", "neutral")
    }
    
    # Thêm thông tin sản phẩm và thống kê nếu có
    if "product_info" in result:
        response["product_info"] = result["product_info"]
    
    if "review_stats" in result:
        response["review_stats"] = result["review_stats"]
    
    if "average_star_rating" in result:
        response["average_star_rating"] = result["average_star_rating"]
    
    return jsonify(response)

@api_bp.route('/reviews/sentiment', methods=['POST'])
def analyze_reviews() -> Dict[str, List[Dict[str, Any]]]:
    """
    Endpoint phân tích cảm xúc cho một danh sách reviews
    
    Request body:
        {
            "reviews": [
                {
                    "id": "review_id",
                    "comment": "Nội dung review",
                    ...
                },
                ...
            ]
        }
    
    Returns:
        Dict[str, List[Dict[str, Any]]]: Danh sách reviews đã được phân tích cảm xúc
    """
    data = request.get_json()
    
    # Validate dữ liệu
    if not data or 'reviews' not in data or not isinstance(data['reviews'], list):
        return jsonify({'error': 'Invalid or missing reviews parameter'}), 400
    
    # Phân tích cảm xúc
    analyzed_reviews = sentiment_analyzer.analyze_reviews(data['reviews'])
    
    return jsonify({'results': analyzed_reviews})

@api_bp.route('/reports/generate', methods=['POST'])
def generate_sentiment_report() -> Dict[str, Any]:
    """
    Endpoint tạo báo cáo phân tích cảm xúc
    
    Request body:
        {
            "product_ids": ["id1", "id2", ...],  # Optional, danh sách ID sản phẩm cần phân tích
            "use_sample": true,                  # Optional, sử dụng dữ liệu mẫu thay vì API
            "limit": 100                         # Optional, số lượng reviews tối đa mỗi sản phẩm
        }
    
    Returns:
        Dict[str, Any]: Thông tin về báo cáo đã tạo và đường dẫn để xem
    """
    data = request.get_json() or {}
    
    # Xác định tham số
    product_ids = data.get('product_ids')
    product_ids_str = ','.join(product_ids) if product_ids else None
    use_sample = data.get('use_sample', False)
    limit = data.get('limit', 100)
    
    # Tạo thư mục tạm thời cho báo cáo
    output_dir = os.path.join('reports', 'sentiment_analysis')
    os.makedirs(output_dir, exist_ok=True)
    
    # Xây dựng command để chạy script
    cmd = ['python', '-m', 'scripts.sentiment_report', f'--output={output_dir}']
    
    if use_sample:
        cmd.append('--use-sample')
    
    if product_ids_str:
        cmd.append(f'--product-ids={product_ids_str}')
    
    cmd.append(f'--limit={limit}')
    
    try:
        # Chạy script tạo báo cáo
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Trả về thông tin báo cáo
        return jsonify({
            'status': 'success',
            'message': 'Sentiment report generated successfully',
            'report_path': f'/api/reports/view',
            'output_dir': output_dir,
            'command_output': process.stdout
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to generate sentiment report: {str(e)}',
            'command_output': e.stdout,
            'error_output': e.stderr
        }), 500

@api_bp.route('/reports/view', methods=['GET'])
def view_sentiment_report():
    """
    Endpoint xem báo cáo phân tích cảm xúc
    
    Query parameters:
        file (str, optional): Tệp cụ thể để xem. Mặc định là index.html.
    
    Returns:
        File: Nội dung tệp báo cáo
    """
    file_path = request.args.get('file', 'index.html')
    report_dir = os.path.join('reports', 'sentiment_analysis')
    
    # Kiểm tra tệp tồn tại
    if not os.path.exists(os.path.join(report_dir, file_path)):
        return jsonify({
            'status': 'error',
            'message': f'Report file {file_path} not found'
        }), 404
    
    # Trả về tệp
    return send_from_directory(report_dir, file_path)

@api_bp.route('/trends/distribution', methods=['GET'])
def get_sentiment_distribution():
    """
    Endpoint lấy phân phối cảm xúc tổng quan
    
    Query parameters:
        product_id (str, optional): ID sản phẩm. Nếu không cung cấp, sẽ phân tích tất cả.
    
    Returns:
        Dict[str, Any]: Phân phối cảm xúc (số lượng và tỷ lệ)
    """
    product_id = request.args.get('product_id')
    
    # Phân tích cảm xúc
    if product_id:
        # Nếu có product_id, lấy dữ liệu cho sản phẩm cụ thể
        result = sentiment_analyzer.analyze_product_reviews(product_id)
        distribution = result['sentiment_distribution']
    else:
        # Nếu không có product_id, sử dụng dữ liệu mẫu
        from scripts.sentiment_report import load_sample_data
        reviews = load_sample_data()
        
        # Khởi tạo trend analyzer
        trend_analyzer = SentimentTrendAnalyzer(reviews)
        distribution = trend_analyzer.get_sentiment_distribution()
    
    # Tính tổng và tỷ lệ phần trăm
    total = sum(distribution.values())
    percentages = {
        f"{k}_pct": round(v / total * 100, 1) if total > 0 else 0
        for k, v in distribution.items()
    }
    
    # Định dạng kết quả trả về để phù hợp với recommendation-service
    response = {
        'distribution': distribution,
        'percentages': percentages,
        'total': total
    }
    
    return jsonify(response)

@api_bp.route('/trends/overtime', methods=['GET'])
def get_sentiment_over_time():
    """
    Endpoint lấy xu hướng cảm xúc theo thời gian
    
    Query parameters:
        product_id (str, optional): ID sản phẩm. Nếu không cung cấp, sẽ phân tích tất cả.
        time_unit (str, optional): Đơn vị thời gian (day, week, month). Mặc định là month.
    
    Returns:
        Dict[str, Any]: Dữ liệu xu hướng cảm xúc theo thời gian
    """
    product_id = request.args.get('product_id')
    time_unit = request.args.get('time_unit', 'month')
    
    # Tải dữ liệu mẫu
    from scripts.sentiment_report import load_sample_data
    reviews = load_sample_data()
    
    # Khởi tạo trend analyzer
    trend_analyzer = SentimentTrendAnalyzer(reviews)
    
    # Lọc dữ liệu theo sản phẩm nếu có
    if product_id:
        filtered_reviews = [r for r in reviews if r.get('product_id') == product_id]
        if filtered_reviews:
            trend_analyzer = SentimentTrendAnalyzer(filtered_reviews)
    
    # Lấy dữ liệu theo thời gian
    try:
        trend_data = trend_analyzer.get_sentiment_score_over_time(time_unit=time_unit)
        
        # Chuyển đổi DataFrame thành định dạng JSON
        result = {
            'time_periods': trend_data.index.tolist(),
            'positive': trend_data['positive'].tolist() if 'positive' in trend_data.columns else [],
            'neutral': trend_data['neutral'].tolist() if 'neutral' in trend_data.columns else [],
            'negative': trend_data['negative'].tolist() if 'negative' in trend_data.columns else [],
            'sentiment_score': trend_data['sentiment_score'].tolist() if 'sentiment_score' in trend_data.columns else []
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to analyze sentiment trends: {str(e)}'
        }), 500

@api_bp.route('/products/compare', methods=['GET'])
def compare_products():
    """
    Endpoint so sánh cảm xúc giữa các sản phẩm
    
    Query parameters:
        product_ids (str): Danh sách ID sản phẩm, cách nhau bởi dấu phẩy
    
    Returns:
        Dict[str, Any]: Dữ liệu so sánh cảm xúc giữa các sản phẩm
    """
    product_ids_str = request.args.get('product_ids')
    
    if not product_ids_str:
        return jsonify({
            'status': 'error',
            'message': 'Missing product_ids parameter'
        }), 400
    
    product_ids = product_ids_str.split(',')
    
    # Tải dữ liệu mẫu
    from scripts.sentiment_report import load_sample_data
    reviews = load_sample_data()
    
    # Khởi tạo trend analyzer
    trend_analyzer = SentimentTrendAnalyzer(reviews)
    
    # So sánh sản phẩm
    try:
        comparison_data = trend_analyzer.compare_products(product_ids)
        return jsonify(comparison_data)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to compare products: {str(e)}'
        }), 500

@api_bp.route('/products/top', methods=['GET'])
def get_top_sentiment_products():
    """
    Endpoint lấy danh sách sản phẩm có cảm xúc tích cực nhất
    
    Query parameters:
        limit (int, optional): Số lượng sản phẩm tối đa. Mặc định là 10.
        category (str, optional): Danh mục sản phẩm cần lọc.
    
    Returns:
        Dict[str, Any]: Danh sách sản phẩm có cảm xúc tích cực nhất
    """
    limit = request.args.get('limit', default=10, type=int)
    category = request.args.get('category')
    
    try:
        # Sử dụng dữ liệu mẫu từ sentiment_report nếu không có dữ liệu thực
        from scripts.sentiment_report import load_sample_data
        reviews = load_sample_data()
        
        # Khởi tạo trend analyzer
        from src.analytics.sentiment_trends import SentimentTrendAnalyzer
        trend_analyzer = SentimentTrendAnalyzer(reviews)
        
        # Lọc theo danh mục nếu cần
        if category:
            filtered_reviews = [r for r in reviews if r.get('category') == category]
            if filtered_reviews:
                trend_analyzer = SentimentTrendAnalyzer(filtered_reviews)
        
        # Lấy top sản phẩm
        top_products = trend_analyzer.get_top_products(n=limit, by='sentiment_score')
        
        # Chuyển đổi sang định dạng phù hợp
        products = []
        for _, row in top_products.iterrows():
            product = {
                'product_id': row.get('product_id', ''),
                'sentiment_score': float(row.get('sentiment_score', 0.5)),
                'positive_count': int(row.get('positive_count', 0)),
                'neutral_count': int(row.get('neutral_count', 0)),
                'negative_count': int(row.get('negative_count', 0)),
                'total_reviews': int(row.get('total_reviews', 0))
            }
            
            # Thêm thông tin sản phẩm nếu có
            if 'product_name' in row:
                product['product_name'] = row['product_name']
            if 'category' in row:
                product['category'] = row['category']
                
            products.append(product)
        
        return jsonify({'products': products})
    except Exception as e:
        return jsonify({
            'error': f'Error getting top products: {str(e)}',
            'products': []
        }), 500

@api_bp.route('/products/compare', methods=['GET'])
def compare_products_sentiment():
    """
    Endpoint so sánh cảm xúc giữa nhiều sản phẩm
    
    Query parameters:
        product_ids (str): Danh sách ID sản phẩm, phân cách bằng dấu phẩy.
    
    Returns:
        Dict[str, Any]: Dữ liệu so sánh cảm xúc giữa các sản phẩm
    """
    product_ids_param = request.args.get('product_ids', '')
    if not product_ids_param:
        return jsonify({'error': 'Missing product_ids parameter'}), 400
    
    # Chuyển đổi chuỗi product_ids thành danh sách
    product_ids = product_ids_param.split(',')
    
    # Dữ liệu so sánh cho các sản phẩm
    comparison_data = {}
    product_details = []
    
    for product_id in product_ids:
        # Phân tích cảm xúc cho sản phẩm
        result = sentiment_analyzer.analyze_product_reviews(product_id.strip())
        
        # Lưu thông tin so sánh
        comparison_data[product_id] = {
            'sentiment_score': result.get('overall_score', 0.5),
            'distribution': result.get('sentiment_distribution', {
                'positive': 0,
                'neutral': 0,
                'negative': 0
            })
        }
        
        # Thêm thông tin chi tiết sản phẩm
        product_info = result.get('product_info', {})
        product_info['product_id'] = product_id
        product_info['sentiment_score'] = result.get('overall_score', 0.5)
        product_details.append(product_info)
    
    return jsonify({
        'products': product_details,
        'comparison': comparison_data
    })