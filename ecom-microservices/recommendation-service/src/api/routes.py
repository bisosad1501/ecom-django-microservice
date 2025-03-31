"""
API routes for recommendation service
"""

import logging
from flask import Blueprint, request, jsonify
from ..services.recommender import RecommendationService
from ..config.settings import Config

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
api_bp = Blueprint('api', __name__)

# Initialize services
recommender = RecommendationService()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "recommendation-service",
        "version": Config.API_VERSION
    })

@api_bp.route('/recommendations/user/<user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    """
    Get personalized recommendations for a user
    
    Query parameters:
        - limit: Maximum number of recommendations (default: 10)
        - include_sentiment: Whether to include sentiment analysis (default: true)
    """
    try:
        limit = request.args.get('limit', Config.DEFAULT_RECOMMENDATIONS, type=int)
        include_sentiment = request.args.get('include_sentiment', 'true').lower() == 'true'
        
        recommendations = recommender.get_recommendations_for_user(
            user_id, 
            limit=limit,
            include_sentiment=include_sentiment
        )
        
        return jsonify({
            "user_id": user_id,
            "count": len(recommendations),
            "recommendations": recommendations
        })
    except Exception as e:
        logger.error(f"Error in get_user_recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/recommendations/product/<product_id>/similar', methods=['GET'])
def get_similar_products(product_id):
    """
    Get similar products for a given product
    
    Query parameters:
        - limit: Maximum number of similar products (default: 10)
        - include_sentiment: Whether to include sentiment analysis (default: true)
    """
    try:
        limit = request.args.get('limit', Config.DEFAULT_RECOMMENDATIONS, type=int)
        include_sentiment = request.args.get('include_sentiment', 'true').lower() == 'true'
        
        similar_products = recommender.get_similar_products(
            product_id, 
            limit=limit,
            include_sentiment=include_sentiment
        )
        
        return jsonify({
            "product_id": product_id,
            "count": len(similar_products),
            "similar_products": similar_products
        })
    except Exception as e:
        logger.error(f"Error in get_similar_products: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/recommendations/sentiment', methods=['GET'])
def get_sentiment_recommendations():
    """
    Get recommendations based on sentiment analysis
    
    Query parameters:
        - category: Filter by category (default: None)
        - limit: Maximum number of recommendations (default: 10)
    """
    try:
        category = request.args.get('category')
        limit = request.args.get('limit', Config.DEFAULT_RECOMMENDATIONS, type=int)
        
        top_products = recommender.get_sentiment_based_recommendations(
            category=category,
            limit=limit
        )
        
        return jsonify({
            "category": category,
            "count": len(top_products),
            "products": top_products
        })
    except Exception as e:
        logger.error(f"Error in get_sentiment_recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/recommendations/popular', methods=['GET'])
def get_popular_products():
    """
    Get popular products
    
    Query parameters:
        - category: Filter by category (default: None)
        - limit: Maximum number of products (default: 10)
    """
    try:
        category = request.args.get('category')
        limit = request.args.get('limit', Config.DEFAULT_RECOMMENDATIONS, type=int)
        
        popular_products = recommender.get_popular_products(
            category=category,
            limit=limit
        )
        
        return jsonify({
            "category": category,
            "count": len(popular_products),
            "products": popular_products
        })
    except Exception as e:
        logger.error(f"Error in get_popular_products: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/recommendations/sentiment-based', methods=['GET'])
def get_sentiment_based_user_recommendations():
    """
    Get personalized recommendations for a user with high sentiment focus
    
    Query parameters:
        - user_id: ID of the user (required)
        - limit: Maximum number of recommendations (default: 10)
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
            
        limit = request.args.get('limit', Config.DEFAULT_RECOMMENDATIONS, type=int)
        
        # Get recommendations with sentiment analysis
        recommendations = recommender.get_recommendations_for_user(
            user_id, 
            limit=limit*2,  # Get more recommendations initially
            include_sentiment=True
        )
        
        # Filter to only highly rated products (sentiment score >= 0.7)
        sentiment_recommendations = [
            rec for rec in recommendations 
            if rec.get('sentiment_score', 0) >= 0.7
        ]
        
        # If we don't have enough recommendations, fall back to regular ones
        if len(sentiment_recommendations) < limit:
            sentiment_recommendations = recommendations[:limit]
        else:
            sentiment_recommendations = sentiment_recommendations[:limit]
        
        return jsonify({
            "user_id": user_id,
            "count": len(sentiment_recommendations),
            "sentiment_based_recommendations": sentiment_recommendations
        })
    except Exception as e:
        logger.error(f"Error in get_sentiment_based_user_recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/insights/user/<user_id>/preferences', methods=['GET'])
def get_user_preferences(user_id):
    """
    Get user preferences based on their interactions
    
    This endpoint analyzes user ratings and reviews to extract preferences
    """
    try:
        # This would be implemented with a more sophisticated analysis
        # For now, we return a sample response
        return jsonify({
            "user_id": user_id,
            "preferences": {
                "favorite_categories": ["books", "electronics"],
                "favorite_brands": ["Brand A", "Brand B"],
                "interests": ["fiction", "technology"],
                "average_rating": 4.2
            }
        })
    except Exception as e:
        logger.error(f"Error in get_user_preferences: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/insights/product/<product_id>/recommendation-reasons', methods=['GET'])
def get_recommendation_reasons(product_id):
    """
    Get reasons why a product might be recommended to users
    
    This endpoint provides insight into the factors that influence recommendations
    """
    try:
        # This would be implemented with a more sophisticated analysis
        # For now, we return a sample response
        return jsonify({
            "product_id": product_id,
            "recommendation_reasons": [
                "High overall sentiment score (4.2/5)",
                "Positive reviews mentioning quality and durability",
                "Similar to other products that users with similar preferences have rated highly",
                "High ratings from users with similar interests"
            ]
        })
    except Exception as e:
        logger.error(f"Error in get_recommendation_reasons: {str(e)}")
        return jsonify({"error": str(e)}), 500 