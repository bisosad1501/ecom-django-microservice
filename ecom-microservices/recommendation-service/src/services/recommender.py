"""
Recommender Service - Main service coordinating recommendation operations
"""

import logging
from typing import Dict, List, Any, Optional
from ..models.hybrid_model import HybridRecommender
from ..services.product_client import ProductClient
from ..utils.cache import cache
from ..config.settings import Config

# Configure logging
logger = logging.getLogger(__name__)

class RecommendationService:
    """Main service for handling product recommendations"""
    
    def __init__(self):
        """Initialize recommendation service"""
        self.hybrid_model = HybridRecommender()
        self.product_client = ProductClient()
    
    @cache(ttl=1800)
    def get_recommendations_for_user(self, user_id: str, limit: int = 10, include_sentiment: bool = True) -> List[Dict[str, Any]]:
        """
        Get personalized recommendations for a user
        
        Args:
            user_id (str): ID of the user
            limit (int, optional): Maximum number of recommendations. Defaults to 10.
            include_sentiment (bool, optional): Whether to include sentiment analysis. Defaults to True.
            
        Returns:
            List[Dict[str, Any]]: List of recommended products with details
        """
        try:
            # Get recommendations from hybrid model
            recommendations = self.hybrid_model.recommend_for_user(
                user_id, 
                limit=min(limit, Config.MAX_RECOMMENDATIONS),
                include_sentiment=include_sentiment
            )
            
            # Enrich recommendations with product details
            enriched_recommendations = self._enrich_recommendations(recommendations)
            
            return enriched_recommendations
        except Exception as e:
            logger.error(f"Error getting recommendations for user {user_id}: {str(e)}")
            return []
    
    @cache(ttl=1800)
    def get_similar_products(self, product_id: str, limit: int = 10, include_sentiment: bool = True) -> List[Dict[str, Any]]:
        """
        Get similar products for a given product
        
        Args:
            product_id (str): ID of the product
            limit (int, optional): Maximum number of similar products. Defaults to 10.
            include_sentiment (bool, optional): Whether to include sentiment analysis. Defaults to True.
            
        Returns:
            List[Dict[str, Any]]: List of similar products with details
        """
        try:
            # Get similar products from hybrid model
            similar_products = self.hybrid_model.recommend_similar_products(
                product_id, 
                limit=min(limit, Config.MAX_RECOMMENDATIONS),
                include_sentiment=include_sentiment
            )
            
            # Enrich recommendations with product details
            enriched_recommendations = self._enrich_recommendations(similar_products)
            
            return enriched_recommendations
        except Exception as e:
            logger.error(f"Error getting similar products for {product_id}: {str(e)}")
            return []
    
    @cache(ttl=3600)
    def get_sentiment_based_recommendations(self, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recommendations based on sentiment analysis
        
        Args:
            category (str, optional): Filter by category. Defaults to None.
            limit (int, optional): Maximum number of recommendations. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of recommended products with details
        """
        try:
            # Get top sentiment products from hybrid model
            top_products = self.hybrid_model.get_top_sentiment_recommendations(
                category=category,
                limit=min(limit, Config.MAX_RECOMMENDATIONS)
            )
            
            # If products already have details, return them
            if top_products and 'name' in top_products[0]:
                return top_products
            
            # Otherwise, enrich with product details
            enriched_recommendations = []
            
            for rec in top_products:
                product_id = rec.get('product_id')
                product = self.product_client.get_product(product_id)
                
                if product:
                    # Merge recommendation data with product details
                    product.update({
                        'sentiment_score': rec.get('sentiment_score', 0),
                        'recommendation_type': 'sentiment'
                    })
                    enriched_recommendations.append(product)
            
            return enriched_recommendations
        except Exception as e:
            logger.error(f"Error getting sentiment-based recommendations: {str(e)}")
            return []
    
    @cache(ttl=1800)
    def get_popular_products(self, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get popular products
        
        Args:
            category (str, optional): Filter by category. Defaults to None.
            limit (int, optional): Maximum number of products. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of popular products
        """
        try:
            # Get products from product client
            products = self.product_client.get_products(
                category=category,
                limit=min(limit, Config.MAX_RECOMMENDATIONS)
            )
            
            # Sort by rating (already done in product client)
            return products
        except Exception as e:
            logger.error(f"Error getting popular products: {str(e)}")
            return []
    
    def _enrich_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich recommendations with product details
        
        Args:
            recommendations (List[Dict[str, Any]]): List of recommendations
            
        Returns:
            List[Dict[str, Any]]: Enriched recommendations with product details
        """
        enriched_recommendations = []
        
        for rec in recommendations:
            product_id = rec.get('product_id')
            product = self.product_client.get_product(product_id)
            
            if product:
                # Extract recommendation metadata
                rec_metadata = {
                    'recommendation_score': rec.get('final_score', rec.get('score', 0)),
                    'recommendation_type': rec.get('type', 'hybrid')
                }
                
                # Add sentiment data if available
                if 'sentiment_score' in rec:
                    rec_metadata['sentiment_score'] = rec['sentiment_score']
                
                if 'sentiment_distribution' in rec:
                    rec_metadata['sentiment_distribution'] = rec['sentiment_distribution']
                
                # Merge product with recommendation metadata
                product.update(rec_metadata)
                enriched_recommendations.append(product)
        
        return enriched_recommendations 