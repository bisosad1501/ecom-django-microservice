#!/usr/bin/env python
"""
Sentiment Analysis Service - Main Application
"""

import os
import logging
import sys

# Add monkey patch for werkzeug url_quote compatibility
import werkzeug
if not hasattr(werkzeug.urls, 'url_quote'):
    werkzeug.urls.url_quote = werkzeug.urls.quote

from flask import Flask, jsonify
from flask_cors import CORS
from src.api.routes import api_bp

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """
    Khởi tạo ứng dụng Flask
    """
    app = Flask(__name__)
    
    # Thiết lập CORS
    CORS(app)
    
    # Đăng ký blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Endpoint kiểm tra hệ thống
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'ok',
            'service': 'sentiment-service',
            'version': '1.0.0'
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Lấy thông tin cổng từ biến môi trường hoặc sử dụng giá trị mặc định
    port = int(os.environ.get('PORT', 8010))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting Sentiment Analysis Service on {host}:{port}")
    app.run(host=host, port=port, debug=os.environ.get('DEBUG', 'False').lower() == 'true')