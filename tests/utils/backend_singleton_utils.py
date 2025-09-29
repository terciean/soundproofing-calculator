"""Backend singleton testing utilities for soundproofing calculator

This module provides utilities for managing singleton instances during testing,
including reset, cleanup, and mock functionality.
"""

import threading
from typing import Optional, Dict, Any
from unittest.mock import Mock, MagicMock

# Import singleton functions
try:
    from solutions.acoustic_calculator import (
        reset_acoustic_calculator, 
        cleanup_acoustic_calculator,
        get_acoustic_calculator
    )
except ImportError:
    reset_acoustic_calculator = None
    cleanup_acoustic_calculator = None
    get_acoustic_calculator = None

try:
    from solutions.cache_manager import get_cache_manager
except ImportError:
    get_cache_manager = None

try:
    from solutions.solutions_manager import (
        reset_solutions_manager,
        cleanup_solutions_manager,
        get_solutions_manager
    )
except ImportError:
    reset_solutions_manager = None
    cleanup_solutions_manager = None
    get_solutions_manager = None

try:
    from solutions.db_init import (
        reset_db_connection,
        cleanup_db_connection,
        get_db_connection
    )
except ImportError:
    reset_db_connection = None
    cleanup_db_connection = None
    get_db_connection = None


class BackendSingletonManager:
    """Manager for backend singleton instances during testing"""
    
    def __init__(self):
        self._original_instances = {}
        self._mock_instances = {}
        self._reset_lock = threading.Lock()
    
    def reset_all_singletons(self):
        """Reset all singleton instances to None"""
        with self._reset_lock:
            # Reset acoustic calculator
            if reset_acoustic_calculator:
                reset_acoustic_calculator()
            
            # Reset cache manager
            if get_cache_manager:
                cache_manager = get_cache_manager()
                if cache_manager and hasattr(cache_manager, 'cleanup'):
                    cache_manager.cleanup()
            
            # Reset solutions manager
            if reset_solutions_manager:
                reset_solutions_manager()
            
            # Reset database connection
            if reset_db_connection:
                reset_db_connection()
    
    def cleanup_all_singletons(self):
        """Cleanup all singleton instances and their resources"""
        with self._reset_lock:
            # Cleanup acoustic calculator
            if cleanup_acoustic_calculator:
                cleanup_acoustic_calculator()
            
            # Cleanup cache manager
            if get_cache_manager:
                cache_manager = get_cache_manager()
                if cache_manager and hasattr(cache_manager, 'cleanup'):
                    cache_manager.cleanup()
            
            # Cleanup solutions manager
            if cleanup_solutions_manager:
                cleanup_solutions_manager()
            
            # Cleanup database connection
            if cleanup_db_connection:
                cleanup_db_connection()
    
    def create_mock_acoustic_calculator(self) -> Mock:
        """Create a mock acoustic calculator with common methods"""
        mock_calc = Mock()
        
        # Mock common methods
        mock_calc.calculate_stc_rating.return_value = 45
        mock_calc.calculate_transmission_loss.return_value = {
            'frequency_response': [20, 25, 30, 35, 40],
            'average_tl': 32.5
        }
        mock_calc.get_material_properties.return_value = {
            'density': 1200,
            'thickness': 0.025,
            'absorption_coefficient': 0.85
        }
        mock_calc.estimate_cost.return_value = 150.0
        mock_calc.cleanup = Mock()
        
        return mock_calc
    
    def create_mock_cache_manager(self) -> Mock:
        """Create a mock cache manager with common methods"""
        mock_cache = Mock()
        
        # Mock cache operations
        mock_cache.get.return_value = None
        mock_cache.set.return_value = True
        mock_cache.delete.return_value = True
        mock_cache.clear.return_value = True
        mock_cache.get_stats.return_value = {
            'hits': 0,
            'misses': 0,
            'added': 0,
            'removed': 0
        }
        mock_cache.cleanup = Mock()
        
        return mock_cache
    
    def create_mock_solutions_manager(self) -> Mock:
        """Create a mock solutions manager with common methods"""
        mock_solutions = Mock()
        
        # Mock solution operations
        mock_solutions.get_solutions.return_value = []
        mock_solutions.find_solutions.return_value = []
        mock_solutions.load_solutions_from_db.return_value = True
        mock_solutions.cleanup = Mock()
        
        return mock_solutions
    
    def create_mock_db_connection(self) -> Mock:
        """Create a mock database connection"""
        mock_db = Mock()
        
        # Mock database operations
        mock_db.client = Mock()
        mock_db.database = Mock()
        mock_db.client.close = Mock()
        
        return mock_db
    
    def get_singleton_status(self) -> Dict[str, Any]:
        """Get status of all singleton instances"""
        status = {}
        
        # Check acoustic calculator
        if get_acoustic_calculator:
            try:
                calc = get_acoustic_calculator()
                status['acoustic_calculator'] = {
                    'initialized': calc is not None,
                    'type': type(calc).__name__ if calc else None
                }
            except Exception as e:
                status['acoustic_calculator'] = {'error': str(e)}
        
        # Check cache manager
        if get_cache_manager:
            try:
                cache = get_cache_manager()
                status['cache_manager'] = {
                    'initialized': cache is not None,
                    'type': type(cache).__name__ if cache else None
                }
            except Exception as e:
                status['cache_manager'] = {'error': str(e)}
        
        # Check solutions manager
        if get_solutions_manager:
            try:
                solutions = get_solutions_manager()
                status['solutions_manager'] = {
                    'initialized': solutions is not None,
                    'type': type(solutions).__name__ if solutions else None
                }
            except Exception as e:
                status['solutions_manager'] = {'error': str(e)}
        
        # Check database connection
        if get_db_connection:
            try:
                db = get_db_connection()
                status['db_connection'] = {
                    'initialized': db is not None,
                    'type': type(db).__name__ if db else None
                }
            except Exception as e:
                status['db_connection'] = {'error': str(e)}
        
        return status


# Global instance for easy access
backend_singleton_manager = BackendSingletonManager()


# Convenience functions
def reset_all_backend_singletons():
    """Reset all backend singleton instances"""
    backend_singleton_manager.reset_all_singletons()


def cleanup_all_backend_singletons():
    """Cleanup all backend singleton instances"""
    backend_singleton_manager.cleanup_all_singletons()


def get_backend_singleton_status() -> Dict[str, Any]:
    """Get status of all backend singleton instances"""
    return backend_singleton_manager.get_singleton_status()


def create_mock_backend_singletons() -> Dict[str, Mock]:
    """Create mock instances for all backend singletons"""
    return {
        'acoustic_calculator': backend_singleton_manager.create_mock_acoustic_calculator(),
        'cache_manager': backend_singleton_manager.create_mock_cache_manager(),
        'solutions_manager': backend_singleton_manager.create_mock_solutions_manager(),
        'db_connection': backend_singleton_manager.create_mock_db_connection()
    }