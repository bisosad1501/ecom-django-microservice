#!/usr/bin/env python
"""
Recommendation Service - Main Application Module
Provides product recommendations based on collaborative filtering, content-based filtering,
and sentiment analysis from reviews.
"""

import logging
import logging.config
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .api.routes import api_bp
from .config.settings import Config

# Load environment variables
load_dotenv()

# Configure logging
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        }
    },
    'root': {
        'level': Config.LOG_LEVEL,
        'handlers': ['console']
    }
})

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure app
    app.config.from_object(Config)
    
    # Setup CORS
    CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {"status": "ok", "service": "recommendation-service"}
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    ) 