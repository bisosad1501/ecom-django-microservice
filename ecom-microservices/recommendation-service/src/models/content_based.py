"""
Content-Based Filtering Recommender Model
"""

import os
import logging
from typing import Dict, List, Any, Optional
from ..services.product_client import ProductClient
from ..services.review_client import ReviewClient
from ..config.settings import Config

# Configure logging
logger = logging.getLogger(__name__)

class ContentBasedRecommender:
    """
    Content-Based Filtering recommendation model
    Uses product attributes and descriptions to recommend similar products
    """
    
    def __init__(self):
        """Initialize content-based recommender"""
        self.product_client = ProductClient()
        self.review_client = ReviewClient()
        self.product_features = {}  # Cache for product features
        
    def find_similar(self, product_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Find similar products based on content features
        
        Args:
            product_id (str): ID of the product
            limit (int, optional): Maximum number of similar products. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of similar products with similarity scores
        """
        # Get the product details
        product = self.product_client.get_product(product_id)
        
        if not product:
            logger.warning(f"Product not found: {product_id}")
            return []
        
        # Extract features from the product
        base_features = self._extract_features(product)
        
        if not base_features:
            logger.warning(f"Failed to extract features for product {product_id}")
            return []
        
        # Get products of the same category
        category = product.get('category')
        category_products = self.product_client.get_products(category=category, limit=50)
        
        # Calculate similarity with other products
        similarities = []
        
        for other_product in category_products:
            other_id = other_product.get('id')
            
            # Skip the same product
            if other_id == product_id:
                continue
            
            # Extract features for the other product
            other_features = self._extract_features(other_product)
            
            if not other_features:
                continue
            
            # Calculate similarity between products
            similarity = self._calculate_similarity(base_features, other_features)
            
            similarities.append({
                'product_id': other_id,
                'similarity': similarity,
                'type': 'content-based'
            })
        
        # Sort by similarity (descending) and return top N
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:limit]
    
    def recommend_for_user(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Recommend products for a user based on their past rated products
        
        Args:
            user_id (str): ID of the user
            limit (int, optional): Maximum number of recommendations. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of recommended products with scores
        """
        # Get products rated by the user
        user_ratings = self.review_client.get_user_rated_products(user_id)
        
        if not user_ratings:
            logger.warning(f"No ratings found for user {user_id}")
            return []
        
        # Get top rated products by the user (rating >= 4)
        top_rated_products = [pid for pid, rating in user_ratings.items() if rating >= 4]
        
        if not top_rated_products:
            # If no top rated products, use all products
            top_rated_products = list(user_ratings.keys())
        
        # Get similar products for each top rated product
        all_similarities = {}
        
        for pid in top_rated_products:
            similar_products = self.find_similar(pid, limit=5)
            
            for product in similar_products:
                product_id = product['product_id']
                
                # Skip products already rated by the user
                if product_id in user_ratings:
                    continue
                
                # Update similarity score (taking the maximum if a product appears multiple times)
                if product_id not in all_similarities or product['similarity'] > all_similarities[product_id]:
                    all_similarities[product_id] = product['similarity']
        
        # Convert to list of recommendations
        recommendations = [
            {
                'product_id': pid,
                'score': similarity,
                'type': 'content-based'
            }
            for pid, similarity in all_similarities.items()
        ]
        
        # Sort by similarity (descending) and return top N
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    def _extract_features(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant features from a product for similarity calculation
        
        Args:
            product (Dict[str, Any]): Product data
            
        Returns:
            Dict[str, Any]: Extracted features
        """
        product_id = product.get('id')
        
        # Check if features are already cached
        if product_id in self.product_features:
            return self.product_features[product_id]
        
        features = {}
        
        # Basic features
        features['category'] = product.get('category', '')
        features['description_keywords'] = self._extract_keywords(product.get('description', ''))
        features['name_keywords'] = self._extract_keywords(product.get('name', ''))
        
        # Category-specific features
        if product.get('category') == 'book':
            features['author'] = product.get('author', '')
            
            # Book attributes
            attributes = product.get('attributes', {})
            features['publisher'] = attributes.get('publisher', '')
            features['language'] = attributes.get('language', '')
            
        elif product.get('category') == 'shoe':
            features['brand'] = product.get('brand', '')
            
            # Shoe attributes
            attributes = product.get('attributes', {})
            features['color'] = attributes.get('color', '')
            features['style'] = attributes.get('style', '')
            features['gender'] = attributes.get('gender', '')
            features['material'] = attributes.get('material', '')
        
        # Cache the features
        self.product_features[product_id] = features
        
        return features
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text (str): Text to extract keywords from
            
        Returns:
            List[str]: List of keywords
        """
        if not text:
            return []
        
        # Simple keyword extraction: lowercase, split by spaces, remove short words
        words = text.lower().split()
        keywords = [word for word in words if len(word) > 3]
        
        return keywords
    
    def _calculate_similarity(self, features1: Dict[str, Any], features2: Dict[str, Any]) -> float:
        """
        Calculate similarity between two sets of product features
        
        Args:
            features1 (Dict[str, Any]): Features of the first product
            features2 (Dict[str, Any]): Features of the second product
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Start with a base similarity score
        similarity = 0.0
        
        # Check if products are in the same category
        if features1.get('category') == features2.get('category'):
            similarity += 0.2
        else:
            # Different categories, very low similarity
            return 0.1
        
        # Compare text features (description and name keywords)
        desc_sim = self._calculate_text_similarity(
            features1.get('description_keywords', []),
            features2.get('description_keywords', [])
        )
        similarity += 0.3 * desc_sim
        
        name_sim = self._calculate_text_similarity(
            features1.get('name_keywords', []),
            features2.get('name_keywords', [])
        )
        similarity += 0.2 * name_sim
        
        # Compare category-specific features
        if features1.get('category') == 'book':
            # Compare book features
            if features1.get('author') == features2.get('author'):
                similarity += 0.15
            
            if features1.get('publisher') == features2.get('publisher'):
                similarity += 0.05
                
            if features1.get('language') == features2.get('language'):
                similarity += 0.1
                
        elif features1.get('category') == 'shoe':
            # Compare shoe features
            if features1.get('brand') == features2.get('brand'):
                similarity += 0.15
                
            if features1.get('color') == features2.get('color'):
                similarity += 0.05
                
            if features1.get('style') == features2.get('style'):
                similarity += 0.1
                
            if features1.get('gender') == features2.get('gender'):
                similarity += 0.05
                
            if features1.get('material') == features2.get('material'):
                similarity += 0.05
        
        return min(similarity, 1.0)  # Cap similarity at 1.0
    
    def _calculate_text_similarity(self, keywords1: List[str], keywords2: List[str]) -> float:
        """
        Calculate similarity between two sets of keywords
        
        Args:
            keywords1 (List[str]): First set of keywords
            keywords2 (List[str]): Second set of keywords
            
        Returns:
            float: Similarity score between 0 and 1
        """
        if not keywords1 or not keywords2:
            return 0.0
        
        # Find common keywords
        common_keywords = set(keywords1) & set(keywords2)
        
        # Calculate Jaccard similarity
        similarity = len(common_keywords) / (len(set(keywords1) | set(keywords2)))
        
        return similarity 