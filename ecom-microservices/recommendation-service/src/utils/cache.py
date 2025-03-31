"""
Cache utility for recommendation service
"""

import time
import functools
import logging
from typing import Dict, Any, Callable, Tuple, Optional
from ..config.settings import Config

# Configure logging
logger = logging.getLogger(__name__)

# Simple in-memory cache
_cache: Dict[str, Tuple[float, Any]] = {}

def cache(ttl: int = 3600):
    """
    Cache decorator for function results
    
    Args:
        ttl (int, optional): Time to live in seconds. Defaults to 3600 (1 hour).
    
    Returns:
        Callable: Decorated function with caching
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Skip caching if disabled
            if not Config.CACHE_ENABLED:
                return func(*args, **kwargs)
            
            # Create a cache key based on function name and arguments
            key = f"{func.__module__}.{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Check if result is in cache and not expired
            cached_result = _get_cached_result(key)
            if cached_result is not None:
                logger.debug(f"Cache hit: {key}")
                return cached_result
            
            # Call the function
            result = func(*args, **kwargs)
            
            # Cache the result
            _cache_result(key, result, ttl)
            
            return result
        return wrapper
    return decorator

def _get_cached_result(key: str) -> Optional[Any]:
    """
    Get cached result if it exists and is not expired
    
    Args:
        key (str): Cache key
    
    Returns:
        Optional[Any]: Cached result or None if not found or expired
    """
    if key not in _cache:
        return None
    
    expiry_time, value = _cache[key]
    
    # Check if expired
    if time.time() > expiry_time:
        # Remove expired entry
        del _cache[key]
        return None
    
    return value

def _cache_result(key: str, value: Any, ttl: int) -> None:
    """
    Cache a result with the given TTL
    
    Args:
        key (str): Cache key
        value (Any): Value to cache
        ttl (int): Time to live in seconds
    """
    expiry_time = time.time() + ttl
    _cache[key] = (expiry_time, value)

def clear_cache() -> None:
    """Clear the entire cache"""
    _cache.clear()

def get_cache_size() -> int:
    """
    Get the number of items in the cache
    
    Returns:
        int: Number of items in the cache
    """
    return len(_cache)

def remove_expired_entries() -> int:
    """
    Remove expired entries from the cache
    
    Returns:
        int: Number of entries removed
    """
    current_time = time.time()
    keys_to_remove = [k for k, (expiry, _) in _cache.items() if current_time > expiry]
    
    for key in keys_to_remove:
        del _cache[key]
    
    return len(keys_to_remove) 