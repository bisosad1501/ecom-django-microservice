"""
Collaborative Filtering Recommender Model
"""

import os
import logging
import numpy as np
from typing import Dict, List, Any, Optional
from ..services.review_client import ReviewClient
from ..config.settings import Config

# Configure logging
logger = logging.getLogger(__name__)

class CollaborativeRecommender:
    """
    Collaborative Filtering based recommendation model
    Uses user-item interactions (reviews, ratings) to recommend products
    """
    
    def __init__(self):
        """Initialize collaborative recommender"""
        self.review_client = ReviewClient()
        self.user_item_matrix = {}  # User-item rating matrix
        self.user_similarity = {}  # User similarity cache
    
    def recommend(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Generate recommendations for a user based on collaborative filtering
        
        Args:
            user_id (str): ID of the user
            limit (int, optional): Maximum number of recommendations. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of recommended products with scores
        """
        # Get products rated by the user
        user_ratings = self.review_client.get_user_rated_products(user_id)
        
        if not user_ratings:
            logger.warning(f"No ratings found for user {user_id}, using fallback recommendations")
            return self._get_fallback_recommendations(limit=limit)
        
        # Update user-item matrix with current user's ratings
        self._update_user_item_matrix(user_id, user_ratings)
        
        # Calculate recommendations
        recommendations = self._calculate_recommendations(user_id, user_ratings.keys(), limit)
        
        return recommendations
    
    def _update_user_item_matrix(self, user_id: str, ratings: Dict[str, float]) -> None:
        """
        Update the user-item matrix with a user's ratings
        
        Args:
            user_id (str): ID of the user
            ratings (Dict[str, float]): Dictionary mapping product IDs to ratings
        """
        self.user_item_matrix[user_id] = ratings
        # Clear similarity cache for this user as it needs to be recalculated
        if user_id in self.user_similarity:
            del self.user_similarity[user_id]
    
    def _calculate_user_similarity(self, user_id1: str, user_id2: str) -> float:
        """
        Calculate similarity between two users based on their ratings
        
        Args:
            user_id1 (str): First user ID
            user_id2 (str): Second user ID
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Get ratings for both users
        ratings1 = self.user_item_matrix.get(user_id1, {})
        ratings2 = self.user_item_matrix.get(user_id2, {})
        
        if not ratings1 or not ratings2:
            return 0.0
        
        # Find common products rated by both users
        common_products = set(ratings1.keys()) & set(ratings2.keys())
        
        if not common_products:
            return 0.0
        
        # Extract ratings for common products
        vec1 = [ratings1[p] for p in common_products]
        vec2 = [ratings2[p] for p in common_products]
        
        # Calculate cosine similarity
        dot_product = sum(r1 * r2 for r1, r2 in zip(vec1, vec2))
        norm1 = sum(r1 * r1 for r1 in vec1) ** 0.5
        norm2 = sum(r2 * r2 for r2 in vec2) ** 0.5
        
        # Avoid division by zero
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        similarity = dot_product / (norm1 * norm2)
        return similarity
    
    def _get_user_similarities(self, user_id: str) -> Dict[str, float]:
        """
        Get similarity scores between the given user and all other users
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            Dict[str, float]: Dictionary mapping user IDs to similarity scores
        """
        # Return cached similarities if available
        if user_id in self.user_similarity:
            return self.user_similarity[user_id]
        
        similarities = {}
        
        for other_id in self.user_item_matrix:
            if other_id != user_id:
                similarity = self._calculate_user_similarity(user_id, other_id)
                if similarity > 0:  # Only store non-zero similarities
                    similarities[other_id] = similarity
        
        # Cache the similarities
        self.user_similarity[user_id] = similarities
        
        return similarities
    
    def _calculate_recommendations(self, user_id: str, exclude_products: List[str], limit: int) -> List[Dict[str, Any]]:
        """
        Calculate recommendations for a user based on user similarities
        
        Args:
            user_id (str): ID of the user
            exclude_products (List[str]): Products to exclude (already rated by the user)
            limit (int): Maximum number of recommendations
            
        Returns:
            List[Dict[str, Any]]: List of recommended products with scores
        """
        # Get user similarities
        user_similarities = self._get_user_similarities(user_id)
        
        if not user_similarities:
            logger.warning(f"No similar users found for user {user_id}, using fallback recommendations")
            return self._get_fallback_recommendations(limit=limit)
        
        # Calculate predicted ratings for each product
        product_scores = {}
        
        for other_id, similarity in user_similarities.items():
            # Get products rated by the similar user
            other_ratings = self.user_item_matrix.get(other_id, {})
            
            for product_id, rating in other_ratings.items():
                # Skip products already rated by the user
                if product_id in exclude_products:
                    continue
                
                # Update product score
                if product_id not in product_scores:
                    product_scores[product_id] = {'weighted_sum': 0, 'similarity_sum': 0}
                
                product_scores[product_id]['weighted_sum'] += similarity * rating
                product_scores[product_id]['similarity_sum'] += similarity
        
        # Calculate final predicted ratings
        recommendations = []
        
        for product_id, scores in product_scores.items():
            if scores['similarity_sum'] > 0:
                predicted_rating = scores['weighted_sum'] / scores['similarity_sum']
                
                # Normalize score to be between 0 and 1
                normalized_score = predicted_rating / 5.0
                
                recommendations.append({
                    'product_id': product_id,
                    'score': normalized_score,
                    'type': 'collaborative'
                })
        
        # Sort by predicted rating (descending) and return top N
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    def _get_fallback_recommendations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get fallback recommendations based on overall popularity
        
        Args:
            limit (int, optional): Maximum number of recommendations. Defaults to 10.
            
        Returns:
            List[Dict[str, Any]]: List of recommended products with scores
        """
        # For fallback, let's use the most rated products
        all_product_ratings = {}
        
        # Collect ratings for all products
        for user_ratings in self.user_item_matrix.values():
            for product_id, rating in user_ratings.items():
                if product_id not in all_product_ratings:
                    all_product_ratings[product_id] = {'sum': 0, 'count': 0}
                
                all_product_ratings[product_id]['sum'] += rating
                all_product_ratings[product_id]['count'] += 1
        
        # Calculate average rating for each product
        recommendations = []
        
        for product_id, ratings in all_product_ratings.items():
            avg_rating = ratings['sum'] / ratings['count'] if ratings['count'] > 0 else 0
            
            # Normalize score to be between 0 and 1
            normalized_score = avg_rating / 5.0
            
            recommendations.append({
                'product_id': product_id,
                'score': normalized_score,
                'type': 'popularity'
            })
        
        # Sort by average rating (descending) and return top N
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit] 