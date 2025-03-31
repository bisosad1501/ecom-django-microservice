"""
Hybrid Recommendation Model
Combines content-based filtering, collaborative filtering, and sentiment analysis
"""

import os
import logging
from typing import Dict, List, Any, Optional
from ..services.sentiment_client import SentimentClient
from ..models.collaborative import CollaborativeRecommender
from ..models.content_based import ContentBasedRecommender
from ..config.settings import Config

# Configure logging
logger = logging.getLogger(__name__)

class HybridRecommender:
    """
    Hybrid Recommender Model
    Combines multiple recommendation approaches with sentiment analysis
    """
    
    def __init__(self):
        """Initialize hybrid recommender with its component models"""
        self.collaborative = CollaborativeRecommender()
        self.content_based = ContentBasedRecommender()
        self.sentiment_client = SentimentClient()
        
        # Weight configuration for combining recommendations
        self.weights = {
            'collaborative': Config.COLLABORATION_WEIGHT,  # Default 0.7
            'content_based': 1.0 - Config.COLLABORATION_WEIGHT,  # Default 0.3
            'sentiment': Config.SENTIMENT_WEIGHT  # Default 0.3
        }
    
    def recommend_for_user(self, user_id: str, limit: int = 10, include_sentiment: bool = True) -> List[Dict[str, Any]]:
        """
        Generate recommendations for a user using hybrid approach
        
        Args:
            user_id (str): ID of the user
            limit (int, optional): Maximum number of recommendations. Defaults to 10.
            include_sentiment (bool, optional): Whether to include sentiment analysis. Defaults to True.
            
        Returns:
            List[Dict[str, Any]]: List of recommended products with scores
        """
        # Step 1: Get recommendations from each component model
        collaborative_recs = self.collaborative.recommend(user_id, limit=limit*2)
        content_based_recs = self.content_based.recommend_for_user(user_id, limit=limit*2)
        
        # Step 2: Combine recommendations from different sources
        combined_recs = self._combine_recommendations(collaborative_recs, content_based_recs)
        
        # Step 3: If sentiment analysis is enabled, adjust scores based on sentiment
        if include_sentiment:
            combined_recs = self._apply_sentiment_scores(combined_recs)
        
        # Step 4: Sort by final score and return top N
        combined_recs.sort(key=lambda x: x['final_score'], reverse=True)
        return combined_recs[:limit]
    
    def recommend_similar_products(self, product_id: str, limit: int = 10, include_sentiment: bool = True) -> List[Dict[str, Any]]:
        """
        Find similar products based on content with sentiment adjustment
        
        Args:
            product_id (str): ID of the product
            limit (int, optional): Maximum number of similar products. Defaults to 10.
            include_sentiment (bool, optional): Whether to include sentiment analysis. Defaults to True.
            
        Returns:
            List[Dict[str, Any]]: List of similar products with scores
        """
        # Get similar products based on content
        similar_products = self.content_based.find_similar(product_id, limit=limit*2)
        
        # If sentiment analysis is enabled, adjust scores
        if include_sentiment:
            similar_products = self._apply_sentiment_scores(similar_products)
            
            # Rename fields for consistency
            for product in similar_products:
                product['final_score'] = product.get('final_score', product.get('similarity', 0))
                if 'similarity' in product and 'score' not in product:
                    product['score'] = product['similarity']
        
        # Sort by final score and return top N
        similar_products.sort(key=lambda x: x.get('final_score', x.get('similarity', 0)), reverse=True)
        return similar_products[:limit]
    
    def _combine_recommendations(self, collaborative_recs: List[Dict[str, Any]], content_based_recs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Combine recommendations from different sources
        
        Args:
            collaborative_recs (List[Dict[str, Any]]): Recommendations from collaborative filtering
            content_based_recs (List[Dict[str, Any]]): Recommendations from content-based filtering
            
        Returns:
            List[Dict[str, Any]]: Combined recommendations with weighted scores
        """
        combined = {}
        
        # Process collaborative recommendations
        for rec in collaborative_recs:
            product_id = rec['product_id']
            combined[product_id] = {
                'product_id': product_id,
                'collaborative_score': rec['score'],
                'content_based_score': 0,
                'sentiment_score': 0,
                'type': 'hybrid'
            }
        
        # Process content-based recommendations
        for rec in content_based_recs:
            product_id = rec['product_id']
            if product_id in combined:
                combined[product_id]['content_based_score'] = rec['score']
            else:
                combined[product_id] = {
                    'product_id': product_id,
                    'collaborative_score': 0,
                    'content_based_score': rec['score'],
                    'sentiment_score': 0,
                    'type': 'hybrid'
                }
        
        # Calculate weighted scores (without sentiment yet)
        combined_list = []
        for product_id, data in combined.items():
            # Calculate weighted score (without sentiment for now)
            weighted_score = (
                self.weights['collaborative'] * data['collaborative_score'] +
                self.weights['content_based'] * data['content_based_score']
            )
            
            data['weighted_score'] = weighted_score
            combined_list.append(data)
        
        return combined_list
    
    def _apply_sentiment_scores(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply sentiment analysis scores to recommendations
        
        Args:
            recommendations (List[Dict[str, Any]]): Recommendations to adjust
            
        Returns:
            List[Dict[str, Any]]: Recommendations with sentiment scores and adjusted final scores
        """
        # Get product IDs
        product_ids = [rec['product_id'] for rec in recommendations]
        
        # Get sentiment data for products
        sentiment_data = self.sentiment_client.get_products_sentiment(product_ids)
        
        # Apply sentiment scores to recommendations
        for rec in recommendations:
            product_id = rec['product_id']
            sentiment_info = sentiment_data.get(product_id, {})
            sentiment_score = sentiment_info.get('sentiment_score', 0.5)  # Default to neutral
            
            # Store sentiment score
            rec['sentiment_score'] = sentiment_score
            
            # Calculate final score with sentiment adjustment
            base_score = rec.get('weighted_score', rec.get('score', rec.get('similarity', 0)))
            
            # Apply sentiment weighting
            # Formula: (1-sentiment_weight) * base_score + sentiment_weight * sentiment_score
            sentiment_weight = self.weights['sentiment']
            final_score = (1 - sentiment_weight) * base_score + sentiment_weight * sentiment_score
            
            rec['final_score'] = final_score
            
            # Add distribution information if available
            sentiment_distribution = sentiment_info.get('sentiment_distribution')
            if sentiment_distribution:
                rec['sentiment_distribution'] = sentiment_distribution
        
        return recommendations
    
    def get_top_sentiment_recommendations(self, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top products based on sentiment scores
        
        Args:
            category (str, optional): Filter by category. Defaults to None.
            limit (int, optional): Maximum number of products to return. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of top products by sentiment
        """
        try:
            # Get top sentiment products from sentiment service
            top_products = self.sentiment_client.get_top_sentiment_products(category=category, limit=limit)
            
            if not top_products:
                logger.warning("No top sentiment products found")
                return []
                
            return top_products
        except Exception as e:
            logger.error(f"Error getting top sentiment recommendations: {str(e)}")
            return [] 