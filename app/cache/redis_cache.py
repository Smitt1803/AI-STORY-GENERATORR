import os
import json
import time
from functools import lru_cache

# For demonstration, using a simple dictionary cache
# In production, you would use Redis or another caching system
_cache = {}

def get_cache(key):
    """Get a value from the cache"""
    # Return None if key doesn't exist or has expired
    if key not in _cache:
        return None
    
    value, expiry = _cache[key]
    
    # Check if the cache entry has expired
    if expiry and time.time() > expiry:
        del _cache[key]
        return None
    
    return value

def set_cache(key, value, expire=None):
    """Set a value in the cache with optional expiration time in seconds"""
    if expire:
        expiry_time = time.time() + expire
    else:
        expiry_time = None
    
    _cache[key] = (value, expiry_time)
    return True

def delete_cache(key):
    """Delete a key from the cache"""
    if key in _cache:
        del _cache[key]
        return True
    return False

def flush_cache():
    """Clear the entire cache"""
    _cache.clear()
    return True