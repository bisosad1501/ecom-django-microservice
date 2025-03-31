"""
Sentiment Client - Client for communicating with sentiment analysis service
"""

import os
import requests
import logging
from typing import Dict, List, Any, Optional
from ..config.settings import Config
from ..utils.cache import cache

# Configure logging
logger = logging.getLogger(__name__)

class SentimentClient:
    """Client to interact with the Sentiment Analysis Service"""
    
    def __init__(self, base_url=None):
        """
        Initialize client with the sentiment service URL
        
        Args:
            base_url (str, optional): Base URL of sentiment service. 
                                     Defaults to environment variable.
        """
        self.base_url = base_url or Config.SENTIMENT_SERVICE_URL
        self.timeout = 5  # Timeout in seconds
    
    @cache(ttl=3600)
    def get_product_sentiment(self, product_id: str) -> Dict[str, Any]:
        """
        Get sentiment analysis for a product
        
        Args:
            product_id (str): ID of the product
            
        Returns:
            Dict[str, Any]: Sentiment data including scores and distribution
        """
        try:
            url = f"{self.base_url}/product/{product_id}/sentiment"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            
            logger.warning(f"Failed to get sentiment for product {product_id}: {response.status_code}")
            # Return default values if service fails
            return {
                "product_id": product_id,
                "sentiment_score": 0.5,  # Neutral score
                "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0}
            }
        except Exception as e:
            logger.error(f"Error fetching sentiment for product {product_id}: {str(e)}")
            # Return default values on error
            return {
                "product_id": product_id, 
                "sentiment_score": 0.5,
                "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0}
            }
    
    def get_products_sentiment(self, product_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get sentiment analysis for multiple products
        
        Args:
            product_ids (List[str]): List of product IDs
            
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary mapping product IDs to sentiment data
        """
        results = {}
        for product_id in product_ids:
            results[product_id] = self.get_product_sentiment(product_id)
        return results
    
    @cache(ttl=3600)
    def get_sentiment_distribution(self) -> Dict[str, Any]:
        """
        Get overall sentiment distribution statistics
        
        Returns:
            Dict[str, Any]: Overall sentiment distribution
        """
        try:
            url = f"{self.base_url}/trends/distribution"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            
            logger.warning(f"Failed to get sentiment distribution: {response.status_code}")
            return {"distribution": {"positive": 0, "neutral": 0, "negative": 0}}
        except Exception as e:
            logger.error(f"Error fetching sentiment distribution: {str(e)}")
            return {"distribution": {"positive": 0, "neutral": 0, "negative": 0}}
    
    @cache(ttl=3600)
    def get_top_sentiment_products(self, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top products based on sentiment scores
        
        Args:
            category (str, optional): Filter by category
            limit (int, optional): Number of products to return. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of top products with sentiment data
        """
        try:
            url = f"{self.base_url}/products/top"
            params = {'limit': limit}
            if category:
                params['category'] = category
                
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json().get('products', [])
            
            logger.warning(f"Failed to get top sentiment products: {response.status_code}")
            return []
        except Exception as e:
            logger.error(f"Error fetching top sentiment products: {str(e)}")
            return []
    
    @cache(ttl=3600)
    def compare_products_sentiment(self, product_ids: List[str]) -> Dict[str, Any]:
        """
        Compare sentiment between multiple products
        
        Args:
            product_ids (List[str]): List of product IDs to compare
            
        Returns:
            Dict[str, Any]: Comparison data
        """
        if not product_ids:
            return {"products": [], "comparison": {}}
            
        try:
            url = f"{self.base_url}/products/compare"
            params = {'product_ids': ','.join(product_ids)}
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            
            logger.warning(f"Failed to compare product sentiment: {response.status_code}")
            return {"products": product_ids, "comparison": {}}
        except Exception as e:
            logger.error(f"Error comparing product sentiment: {str(e)}")
            return {"products": product_ids, "comparison": {}} 