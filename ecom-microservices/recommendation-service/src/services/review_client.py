"""
Review Client - Client for communicating with review service
"""

import os
import requests
import logging
from typing import Dict, List, Any, Optional
from ..config.settings import Config
from ..utils.cache import cache

# Configure logging
logger = logging.getLogger(__name__)

class ReviewClient:
    """Client to interact with the Review Service"""
    
    def __init__(self, base_url=None):
        """
        Initialize client with the review service URL
        
        Args:
            base_url (str, optional): Base URL of review service. 
                                     Defaults to environment variable.
        """
        self.base_url = base_url or Config.REVIEW_SERVICE_URL
        self.timeout = 5  # Timeout in seconds
    
    @cache(ttl=1800)
    def get_product_reviews(self, product_id: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get reviews for a product
        
        Args:
            product_id (str): ID of the product
            limit (int, optional): Maximum number of reviews to return. Defaults to 50.
            
        Returns:
            Dict[str, Any]: Product reviews data
        """
        try:
            url = f"{self.base_url}/reviews/product_reviews/{product_id}/"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'product_id': product_id,
                    'total_reviews': data.get('stats', {}).get('total_reviews', 0),
                    'average_rating': data.get('stats', {}).get('average_rating', 0),
                    'verified_reviews': data.get('verified_reviews', [])[:limit],
                    'general_reviews': data.get('general_reviews', [])[:limit]
                }
            
            logger.warning(f"Failed to get reviews for product {product_id}: {response.status_code}")
            return {
                'product_id': product_id,
                'total_reviews': 0,
                'average_rating': 0,
                'verified_reviews': [],
                'general_reviews': []
            }
        except Exception as e:
            logger.error(f"Error fetching reviews for product {product_id}: {str(e)}")
            return {
                'product_id': product_id,
                'total_reviews': 0,
                'average_rating': 0,
                'verified_reviews': [],
                'general_reviews': []
            }
    
    @cache(ttl=1800)
    def get_user_reviews(self, user_id: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get reviews by a user
        
        Args:
            user_id (str): ID of the user
            limit (int, optional): Maximum number of reviews to return. Defaults to 50.
            
        Returns:
            Dict[str, Any]: User reviews data
        """
        try:
            url = f"{self.base_url}/reviews/user_reviews/{user_id}/"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'user_id': user_id,
                    'total_reviews': data.get('total_reviews', 0),
                    'verified_reviews': data.get('verified_reviews', [])[:limit],
                    'general_reviews': data.get('general_reviews', [])[:limit]
                }
            
            logger.warning(f"Failed to get reviews for user {user_id}: {response.status_code}")
            return {
                'user_id': user_id,
                'total_reviews': 0,
                'verified_reviews': [],
                'general_reviews': []
            }
        except Exception as e:
            logger.error(f"Error fetching reviews for user {user_id}: {str(e)}")
            return {
                'user_id': user_id,
                'total_reviews': 0,
                'verified_reviews': [],
                'general_reviews': []
            }
    
    def get_user_rated_products(self, user_id: str) -> Dict[str, float]:
        """
        Get products rated by a user and their ratings
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            Dict[str, float]: Dictionary mapping product IDs to ratings
        """
        try:
            user_reviews = self.get_user_reviews(user_id)
            rated_products = {}
            
            # Process verified reviews
            for review in user_reviews.get('verified_reviews', []):
                rated_products[review.get('product_id')] = review.get('rating', 0)
            
            # Process general reviews
            for review in user_reviews.get('general_reviews', []):
                rated_products[review.get('product_id')] = review.get('rating', 0)
                
            return rated_products
        except Exception as e:
            logger.error(f"Error getting rated products for user {user_id}: {str(e)}")
            return {} 