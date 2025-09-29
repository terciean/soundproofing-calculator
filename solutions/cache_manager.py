"""
Cache manager for storing and retrieving solution data.
"""

import logging
import time
import threading
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta


_cache_manager = None
_cache_manager_lock = threading.Lock()

def get_cache_manager():
    """Get the global cache manager instance with thread safety"""
    global _cache_manager
    if _cache_manager is None:
        with _cache_manager_lock:
            # Double-check locking pattern
            if _cache_manager is None:
                _cache_manager = CacheManager()
    return _cache_manager

def reset_cache_manager():
    """Reset the cache manager instance for testing purposes"""
    global _cache_manager
    with _cache_manager_lock:
        if _cache_manager is not None:
            # Cleanup resources
            if hasattr(_cache_manager, 'cleanup'):
                _cache_manager.cleanup()
        _cache_manager = None

def cleanup_cache_manager():
    """Cleanup the cache manager instance and its resources"""
    global _cache_manager
    with _cache_manager_lock:
        if _cache_manager is not None:
            try:
                _cache_manager.cleanup()
            except Exception as e:
                logger.error(f"Error during cache manager cleanup: {e}")
            finally:
                _cache_manager = None

class CacheManager:
    """
    Manages caching of solution calculations and other expensive operations
    """
    
    def __init__(self, cache_type="simple"):
        """Initialize the cache manager with a specific cache type"""
        self.logger = logging.getLogger(__name__)
        self.cache_type = cache_type
        self.cache = {}
        self.expiry = {}  # Track when cache entries expire
        self.stats = {
            "hits": 0,
            "misses": 0,
            "added": 0,
            "removed": 0,
            "solution_types": {}  # Track hits/misses by solution type
        }
        # Initialize database connection
        self.db = None
        self.cache_timeout = timedelta(hours=1)
        
        self.logger.info(f"Initialized {cache_type} cache manager")



    
    def get(self, key: str, default: Any = None) -> Any:
        """Get an item from cache with optional default"""
        try:
            if not key:
                self.logger.warning("Attempted cache get with empty key")
                return default
                
            # Check if key exists and is not expired
            if key in self.cache and (key not in self.expiry or self.expiry[key] > time.time()):
                self.stats["hits"] += 1
                
                # Track solution type hits if this is a solution cache
                if key.startswith("solution_"):
                    solution_type = self._extract_solution_type(key)
                    if solution_type not in self.stats["solution_types"]:
                        self.stats["solution_types"][solution_type] = {"hits": 0, "misses": 0, "added": 0}
                    self.stats["solution_types"][solution_type]["hits"] += 1
                    
                    # Log detailed cache hit information with file path if available
                    solution_name = key.split('_', 2)[-1] if len(key.split('_')) > 2 else 'unknown'
                    file_path = self._get_solution_file_path(solution_name)
                    
                    if file_path:
                        self.logger.info(f"[CACHE HIT] Type: {solution_type}, Key: {key}, Location: Memory Cache, Source File: {file_path}")
                    else:
                        self.logger.info(f"[CACHE HIT] Type: {solution_type}, Key: {key}, Location: Memory Cache")
                        

                else:
                    self.logger.info(f"[CACHE HIT] Key: {key}, Location: Memory Cache")
                    
                return self.cache[key]
            
            # Handle cache miss or expired item
            if key in self.cache:
                # Expired item
                self.logger.debug(f"Cache expired for {key}")
                del self.cache[key]
                if key in self.expiry:
                    del self.expiry[key]
            
            self.stats["misses"] += 1
            
            # Track solution type misses if this is a solution cache
            if key.startswith("solution_"):
                solution_type = self._extract_solution_type(key)
                if solution_type not in self.stats["solution_types"]:
                    self.stats["solution_types"][solution_type] = {"hits": 0, "misses": 0, "added": 0}
                self.stats["solution_types"][solution_type]["misses"] += 1
            
            self.logger.debug(f"Cache miss for {key}")
            return default
            
        except Exception as e:
            self.logger.error(f"Error getting from cache: {str(e)}")
            return default
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        Set an item in cache with optional TTL (in seconds)
        Returns True if successful, False otherwise
        """
        try:
            if not key:
                self.logger.warning("Attempted cache set with empty key")
                return False
                
            self.cache[key] = value
            if ttl > 0:
                self.expiry[key] = time.time() + ttl
            
            self.stats["added"] += 1
            
            # Track solution type additions with detailed logging
            if key.startswith("solution_"):
                solution_type = self._extract_solution_type(key)
                if solution_type not in self.stats["solution_types"]:
                    self.stats["solution_types"][solution_type] = {"hits": 0, "misses": 0, "added": 0}
                self.stats["solution_types"][solution_type]["added"] += 1
                
                # Log detailed cache set information with file path if available
                solution_name = key.split('_', 2)[-1] if len(key.split('_')) > 2 else 'unknown'
                file_path = self._get_solution_file_path(solution_name)
                
                if file_path:
                    self.logger.info(f"[CACHE SET] Type: {solution_type}, Key: {key}, Location: Memory Cache, Source File: {file_path}")
                else:
                    self.logger.info(f"[CACHE SET] Type: {solution_type}, Key: {key}, Location: Memory Cache")
                    
                if self.db:
                    self.logger.info(f"[CACHE BACKUP] Storing {key} in MongoDB")
            else:
                self.logger.info(f"[CACHE SET] Key: {key}, Location: Memory Cache")
            
            if ttl > 0:
                self.logger.info(f"[CACHE TTL] Key: {key}, Expires: {datetime.fromtimestamp(time.time() + ttl)}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting cache: {str(e)}")
            return False
    
    def has(self, key: str) -> bool:
        """Check if a key exists in the cache and is not expired"""
        try:
            if not key:
                return False
                
            # Check if key exists and is not expired
            if key in self.cache and (key not in self.expiry or self.expiry[key] > time.time()):
                return True
            
            # Clean up expired item if needed
            if key in self.cache and key in self.expiry and self.expiry[key] <= time.time():
                del self.cache[key]
                del self.expiry[key]
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking cache: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete an item from cache"""
        try:
            if not key or key not in self.cache:
                return False
                
            del self.cache[key]
            if key in self.expiry:
                del self.expiry[key]
            
            self.stats["removed"] += 1
            self.logger.debug(f"Removed {key} from cache")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting from cache: {str(e)}")
            return False
    
    def clear(self) -> bool:
        """Clear all items from cache"""
        try:
            self.cache = {}
            self.expiry = {}
            self.logger.info("Cache cleared")
            return True
            
        except Exception as e:
            self.logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            # Calculate hit/miss ratio if any requests have been made
            total_requests = self.stats["hits"] + self.stats["misses"]
            hit_ratio = self.stats["hits"] / total_requests if total_requests > 0 else 0
            
            # Get current size
            cache_size = len(self.cache)
            
            # Count expired items
            now = time.time()
            expired = sum(1 for exp_time in self.expiry.values() if exp_time <= now)
            
            # Get solution-specific stats
            solution_stats = {
                solution_type: {
                    "hits": stats["hits"],
                    "misses": stats["misses"],
                    "added": stats["added"],
                    "hit_ratio": stats["hits"] / (stats["hits"] + stats["misses"]) if (stats["hits"] + stats["misses"]) > 0 else 0
                }
                for solution_type, stats in self.stats["solution_types"].items()
            }
            
            return {
                "type": self.cache_type,
                "size": cache_size,
                "hits": self.stats["hits"],
                "misses": self.stats["misses"],
                "hit_ratio": round(hit_ratio, 2),
                "added": self.stats["added"],
                "removed": self.stats["removed"],
                "expired": expired,
                "solution_stats": solution_stats,
                "timestamp": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting cache stats: {str(e)}")
            return {"error": str(e)}
    
    def _extract_solution_type(self, key: str) -> str:
        """Extract solution type from cache key"""
        try:
            # Expected format: solution_<type>_<name>
            parts = key.split('_')
            if len(parts) >= 2:
                # Map common solution types to standardized categories
                type_map = {
                    'wall': 'wall',
                    'walls': 'wall',
                    'ceiling': 'ceiling',
                    'ceilings': 'ceiling',
                    'floor': 'floor',
                    'floors': 'floor'
                }
                solution_type = parts[1].lower()
                return type_map.get(solution_type, solution_type)
            return 'unknown'
        except Exception:
            return 'unknown'
            
    def _get_collection_name(self, solution_name: str) -> Optional[str]:
        """Get the appropriate collection name for a solution"""
        if 'Wall' in solution_name:
            return 'wallsolutions'
        elif 'Ceiling' in solution_name:
            return 'ceilingsolutions'
        elif 'Floor' in solution_name:
            return 'floorsolutions'
        return None
        
    def _get_solution_file_path(self, solution_name: str) -> Optional[str]:
        """Get the Python file path for a solution"""
        # Map solution names to their respective Python files
        wall_solutions = {
            'Genie Clip wall': 'walls/GenieClipWall.py',
            'Independent Wall': 'walls/Independentwall.py',
            'M20 Solution': 'walls/M20Wall.py',
            'Resilient bar wall': 'walls/resilientbarwall.py'
        }
        
        ceiling_solutions = {
            'Genie Clip ceiling': 'ceilings/genieclipceiling.py',
            'Independent Ceiling': 'ceilings/independentceiling.py',
            'LB3 Genie Clip': 'ceilings/lb3genieclipceiling.py',
            'Resilient bar Ceiling': 'ceilings/resilientbarceiling.py'
        }
        
        # Check both standard and SP15 variants
        base_name = solution_name.replace(' (SP15 Soundboard Upgrade)', '').replace(' (Standard)', '')
        
        if base_name in wall_solutions:
            return wall_solutions[base_name]
        elif base_name in ceiling_solutions:
            return ceiling_solutions[base_name]
        return None
        
    def _process_solution(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """Process a solution document for caching"""
        processed = solution.copy()
        
        # Convert ObjectId to string
        if '_id' in processed:
            processed['_id'] = str(processed['_id'])
            
        # Process materials
        if 'materials' in processed:
            for material in processed['materials']:
                # Convert costs to float
                if 'cost' in material:
                    if isinstance(material['cost'], dict):
                        if '$numberDouble' in material['cost']:
                            material['cost'] = float(material['cost']['$numberDouble'])
                        elif '$numberInt' in material['cost']:
                            material['cost'] = float(material['cost']['$numberInt'])
                        else:
                            # Try to extract first numeric value found
                            for value in material['cost'].values():
                                try:
                                    material['cost'] = float(value)
                                    break
                                except (ValueError, TypeError):
                                    continue
                    elif isinstance(material['cost'], (int, float)):
                        material['cost'] = float(material['cost'])
                    elif isinstance(material['cost'], str):
                        try:
                            # Remove any non-numeric characters except decimal point
                            clean_cost = ''.join(c for c in material['cost'] if c.isdigit() or c == '.')
                            material['cost'] = float(clean_cost)
                        except ValueError:
                            material['cost'] = 0.0
                
                # Convert coverage to float
                if 'coverage' in material:
                    try:
                        if isinstance(material['coverage'], str):
                            # Remove any non-numeric characters except decimal point
                            clean_coverage = ''.join(c for c in material['coverage'] if c.isdigit() or c == '.')
                            material['coverage'] = float(clean_coverage)
                        elif isinstance(material['coverage'], (int, float)):
                            material['coverage'] = float(material['coverage'])
                        elif isinstance(material['coverage'], dict):
                            # Try to extract first numeric value found
                            for value in material['coverage'].values():
                                try:
                                    material['coverage'] = float(value)
                                    break
                                except (ValueError, TypeError):
                                    continue
                    except (ValueError, AttributeError):
                        material['coverage'] = 1.0
                        
        # Process total_cost if present
        if 'total_cost' in processed:
            try:
                if isinstance(processed['total_cost'], dict):
                    if '$numberDouble' in processed['total_cost']:
                        processed['total_cost'] = float(processed['total_cost']['$numberDouble'])
                    elif '$numberInt' in processed['total_cost']:
                        processed['total_cost'] = float(processed['total_cost']['$numberInt'])
                elif isinstance(processed['total_cost'], (int, float)):
                    processed['total_cost'] = float(processed['total_cost'])
                elif isinstance(processed['total_cost'], str):
                    clean_total = ''.join(c for c in processed['total_cost'] if c.isdigit() or c == '.')
                    processed['total_cost'] = float(clean_total)
            except (ValueError, TypeError):
                processed['total_cost'] = 0.0
                        
        return processed

    def _get_cache_collection(self):
        """Get or create the cache collection in MongoDB"""
        return None
        
    def get_cached_calculation(self, key: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached calculation result with solution-specific handling"""
        try:
            # Create composite key from base key and parameters
            cache_key = f"{key}_{hash(frozenset(params.items()))}"
            
            # Special handling for solution data
            if key.startswith('solution_'):
                # Get from cache first
                cached = self.get(cache_key)
                if cached:
                    return cached
                    

            
            return self.get(cache_key)
            
        except Exception as e:
            self.logger.error(f"Error getting cached calculation: {str(e)}")
            return None
            

            

            

            
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.get_stats()


            


    def get_all_keys(self):
        """Get all keys in the cache, or an empty list if not supported by the cache implementation
        
        Returns:
            list: List of all keys in the cache
        """
        try:
            # For SimpleCache or Redis, try to access internal cache keys
            if hasattr(self.cache, 'cache') and hasattr(self.cache.cache, 'keys'):
                return list(self.cache.cache.keys())
            elif hasattr(self.cache, 'redis') and hasattr(self.cache.redis, 'keys'):
                return [k.decode('utf-8') for k in self.cache.redis.keys('*')]
            

                
            # Return empty list if keys cannot be accessed
            return []
        except Exception as e:
            self.logger.error(f"Error getting all cache keys: {e}")
            return []
    
    def cleanup(self):
        """Cleanup cache resources and clear all data"""
        try:
            # Clear in-memory cache
            self.cache.clear()
            self.expiry.clear()
            
            # Reset stats
            self.stats = {
                "hits": 0,
                "misses": 0,
                "added": 0,
                "removed": 0,
                "solution_types": {}
            }
            
            self.logger.info("CacheManager cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during CacheManager cleanup: {e}")

# Simple global cache implementation for backward compatibility
class SimpleCache:
    """Simple global cache for backward compatibility"""
    def __init__(self):
        self.cache_manager = get_cache_manager()
    
    def get(self, key):
        return self.cache_manager.get(key)
    
    def set(self, key, value, timeout=None):
        ttl = timeout if timeout is not None else 3600
        return self.cache_manager.set(key, value, ttl)