"""
Product Client - Client for communicating with product services
"""

import os
import requests
import logging
from typing import Dict, List, Any, Optional
from ..config.settings import Config
from ..utils.cache import cache

# Configure logging
logger = logging.getLogger(__name__)

class ProductClient:
    """Client to interact with the Product Services (book and shoe services)"""
    
    def __init__(self):
        """Initialize clients with the product service URLs"""
        self.book_service_url = Config.BOOK_SERVICE_URL
        self.shoe_service_url = Config.SHOE_SERVICE_URL
        self.product_service_url = Config.PRODUCT_SERVICE_URL
        self.timeout = 5  # Timeout in seconds
    
    @cache(ttl=3600)
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get product details by ID
        
        Args:
            product_id (str): ID of the product
            
        Returns:
            Optional[Dict[str, Any]]: Product details or None if not found
        """
        # Try the generic product service first
        product = self._get_product_from_product_service(product_id)
        if product:
            return product
            
        # Try to get product from book service
        book = self._get_book(product_id)
        if book:
            return book
        
        # If not found, try shoe service
        shoe = self._get_shoe(product_id)
        if shoe:
            return shoe
        
        logger.warning(f"Product not found in any service: {product_id}")
        return None
    
    @cache(ttl=3600)
    def _get_product_from_product_service(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get product details from the generic product service
        
        Args:
            product_id (str): ID of the product
            
        Returns:
            Optional[Dict[str, Any]]: Product details or None if not found
        """
        try:
            url = f"{self.product_service_url}/products/{product_id}/"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                product = response.json()
                return {
                    'id': product.get('id', product_id),
                    'name': product.get('name', ''),
                    'description': product.get('description', ''),
                    'price': product.get('price', 0),
                    'category': product.get('type', 'general').lower(),  # Using type field from ProductType choices
                    'image_url': product.get('image_url', ''),
                    'rating': product.get('avg_rating', 0),
                    'reviews_count': product.get('reviews_count', 0)
                }
            
            return None
        except Exception as e:
            logger.error(f"Error fetching product {product_id} from product service: {str(e)}")
            return None
    
    @cache(ttl=3600)
    def _get_book(self, book_id: str) -> Optional[Dict[str, Any]]:
        """
        Get book details from book service
        
        Args:
            book_id (str): ID of the book
            
        Returns:
            Optional[Dict[str, Any]]: Book details or None if not found
        """
        try:
            url = f"{self.book_service_url}/books/detail/{book_id}/"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                book = response.json()
                return {
                    'id': book.get('product_id', book_id),
                    'name': book.get('title', ''),
                    'description': book.get('description', ''),
                    'price': book.get('price', 0),
                    'category': 'book',
                    'image_url': book.get('cover_image', ''),
                    'authors': book.get('authors', []),  # Using authors array from model
                    'rating': book.get('avg_rating', 0),
                    'reviews_count': book.get('reviews_count', 0),
                    'attributes': {
                        'isbn': book.get('isbn', ''),
                        'publisher': book.get('publisher', ''),
                        'publication_date': book.get('publication_date', ''),
                        'language': book.get('language', ''),
                        'pages': book.get('pages', 0),
                        'edition': book.get('edition', ''),
                        'series': book.get('series', ''),
                        'translator': book.get('translator', '')
                    }
                }
            
            return None
        except Exception as e:
            logger.error(f"Error fetching book {book_id}: {str(e)}")
            return None
    
    @cache(ttl=3600)
    def _get_shoe(self, shoe_id: str) -> Optional[Dict[str, Any]]:
        """
        Get shoe details from shoe service
        
        Args:
            shoe_id (str): ID of the shoe
            
        Returns:
            Optional[Dict[str, Any]]: Shoe details or None if not found
        """
        try:
            url = f"{self.shoe_service_url}/shoes/detail/{shoe_id}/"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                shoe = response.json()
                return {
                    'id': shoe.get('product_id', shoe_id),
                    'name': shoe.get('name', ''),
                    'description': shoe.get('description', ''),
                    'price': shoe.get('price', 0),
                    'category': 'shoe',
                    'image_url': shoe.get('image_url', ''),
                    'brand': shoe.get('brand', ''),
                    'rating': shoe.get('avg_rating', 0),
                    'reviews_count': shoe.get('reviews_count', 0),
                    'attributes': {
                        'color': shoe.get('color', ''),
                        'size': shoe.get('size', ''),
                        'gender': shoe.get('gender', ''),
                        'material': shoe.get('material', ''),
                        'style': shoe.get('style', ''),
                        'sport_type': shoe.get('sport_type', ''),
                        'closure_type': shoe.get('closure_type', ''),
                        'sole_material': shoe.get('sole_material', ''),
                        'waterproof': shoe.get('waterproof', False)
                    }
                }
            
            return None
        except Exception as e:
            logger.error(f"Error fetching shoe {shoe_id}: {str(e)}")
            return None
    
    @cache(ttl=1800)
    def get_products(self, category: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get list of products, optionally filtered by category
        
        Args:
            category (str, optional): Category to filter by. Defaults to None.
            limit (int, optional): Maximum number of products to return. Defaults to 50.
            
        Returns:
            List[Dict[str, Any]]: List of products
        """
        products = []
        
        # Try to get products from the generic product service first
        general_products = self._get_products_from_product_service(category, limit)
        if general_products:
            products.extend(general_products)
            
        # If we need more products or couldn't get from product service, try specific services
        if len(products) < limit:
            remaining_limit = limit - len(products)
            
            # Get books if category is None or 'book'
            if category is None or category.lower() == 'book':
                books = self._get_books(limit=remaining_limit)
                products.extend(books)
            
            # Get shoes if category is None or 'shoe'
            if category is None or category.lower() == 'shoe':
                remaining_limit = limit - len(products)
                if remaining_limit > 0:
                    shoes = self._get_shoes(limit=remaining_limit)
                    products.extend(shoes)
        
        # Return products sorted by rating (descending)
        products.sort(key=lambda x: x.get('rating', 0), reverse=True)
        return products[:limit]
    
    @cache(ttl=1800)
    def _get_products_from_product_service(self, category: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get list of products from the generic product service
        
        Args:
            category (str, optional): Category to filter by. Defaults to None.
            limit (int, optional): Maximum number of products to return. Defaults to 50.
            
        Returns:
            List[Dict[str, Any]]: List of products
        """
        try:
            url = f"{self.product_service_url}/products/"
            params = {}
            if category:
                # Map category to ProductType enum values
                category_map = {
                    'book': 'BOOK',
                    'shoe': 'SHOE',
                    'electronic': 'ELECTRONIC',
                    'clothing': 'CLOTHING'
                }
                params['type'] = category_map.get(category.lower(), category.upper())
            if limit:
                params['limit'] = limit
                
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                products_data = response.json()
                products = []
                
                for product in products_data.get('results', [])[:limit]:
                    products.append({
                        'id': product.get('id', ''),
                        'name': product.get('name', ''),
                        'description': product.get('description', ''),
                        'price': product.get('price', 0),
                        'category': product.get('type', 'general').lower(),  # Using type field from ProductType
                        'image_url': product.get('image_url', ''),
                        'rating': product.get('avg_rating', 0),
                        'reviews_count': product.get('reviews_count', 0)
                    })
                
                return products
            
            logger.warning(f"Failed to get products from product service: {response.status_code}")
            return []
        except Exception as e:
            logger.error(f"Error fetching products from product service: {str(e)}")
            return []
    
    @cache(ttl=1800)
    def _get_books(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get list of books
        
        Args:
            limit (int, optional): Maximum number of books to return. Defaults to 50.
            
        Returns:
            List[Dict[str, Any]]: List of books
        """
        try:
            url = f"{self.book_service_url}/books/"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                books_data = response.json()
                books = []
                
                for book in books_data.get('results', [])[:limit]:
                    books.append({
                        'id': book.get('product_id', ''),
                        'name': book.get('title', ''),  # Books use 'title' instead of 'name'
                        'description': book.get('description', ''),
                        'price': book.get('price', 0),
                        'category': 'book',
                        'image_url': book.get('cover_image', ''),  # Books use 'cover_image'
                        'authors': book.get('authors', []),  # List of authors
                        'rating': book.get('avg_rating', 0),
                        'reviews_count': book.get('reviews_count', 0)
                    })
                
                return books
            
            logger.warning(f"Failed to get books: {response.status_code}")
            return []
        except Exception as e:
            logger.error(f"Error fetching books: {str(e)}")
            return []
    
    @cache(ttl=1800)
    def _get_shoes(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get list of shoes
        
        Args:
            limit (int, optional): Maximum number of shoes to return. Defaults to 50.
            
        Returns:
            List[Dict[str, Any]]: List of shoes
        """
        try:
            url = f"{self.shoe_service_url}/shoes/"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                shoes_data = response.json()
                shoes = []
                
                for shoe in shoes_data.get('results', [])[:limit]:
                    shoes.append({
                        'id': shoe.get('product_id', ''),  # Using product_id as per model
                        'name': shoe.get('name', ''),  
                        'description': shoe.get('description', ''),
                        'price': shoe.get('price', 0),
                        'category': 'shoe',
                        'image_url': shoe.get('image_url', ''),
                        'brand': shoe.get('brand', ''),
                        'color': shoe.get('color', ''),
                        'gender': shoe.get('gender', ''),
                        'rating': shoe.get('avg_rating', 0),
                        'reviews_count': shoe.get('reviews_count', 0)
                    })
                
                return shoes
            
            logger.warning(f"Failed to get shoes: {response.status_code}")
            return []
        except Exception as e:
            logger.error(f"Error fetching shoes: {str(e)}")
            return [] 