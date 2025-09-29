"""Utility functions for resetting singleton states during testing."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

def reset_acoustic_calculator():
    """Reset the AcousticCalculator singleton for testing."""
    try:
        from solutions.acoustic_calculator import reset_acoustic_calculator as reset_func
        reset_func()
        logger.debug("AcousticCalculator singleton reset")
    except Exception as e:
        logger.warning(f"Error resetting AcousticCalculator singleton: {e}")

def reset_cache_manager():
    """Reset the CacheManager singleton for testing."""
    try:
        from solutions.cache_manager import reset_cache_manager as reset_func
        reset_func()
        logger.debug("CacheManager singleton reset")
    except Exception as e:
        logger.warning(f"Error resetting CacheManager singleton: {e}")

def reset_db_connection():
    """Reset the DB connection singleton for testing."""
    try:
        from solutions.db_init import reset_db_connection as reset_func
        reset_func()
        logger.debug("Database connection singleton reset")
    except Exception as e:
        logger.warning(f"Error resetting database connection singleton: {e}")

def reset_solutions_manager():
    """Reset the SolutionsManager singleton for testing."""
    try:
        from solutions.solutions_manager import reset_solutions_manager as reset_func
        reset_func()
        logger.debug("SolutionsManager singleton reset")
    except Exception as e:
        logger.warning(f"Error resetting SolutionsManager singleton: {e}")

def reset_all_singletons():
    """Reset all backend singletons for testing."""
    logger.info("Resetting all backend singletons for testing")
    reset_acoustic_calculator()
    reset_cache_manager()
    reset_db_connection()
    reset_solutions_manager()
    logger.info("All backend singletons reset complete")

class MockAcousticCalculator:
    """Mock implementation of AcousticCalculator for testing."""
    
    def __init__(self):
        """Initialize the mock calculator."""
        self.cache_manager = None
        self.solutions_manager = None
        self.db = None
    
    def calculate_stc_rating(self, *args, **kwargs):
        """Mock STC rating calculation."""
        return 50
    
    def calculate_transmission_loss(self, *args, **kwargs):
        """Mock transmission loss calculation."""
        return {
            'frequency_response': [20, 25, 30, 35, 40],
            'average_tl': 32.5
        }
    
    def get_material_properties(self, *args, **kwargs):
        """Mock material properties retrieval."""
        return {
            'density': 1200,
            'thickness': 0.025,
            'absorption_coefficient': 0.85
        }
    
    def estimate_cost(self, *args, **kwargs):
        """Mock cost estimation."""
        return 150.0
    
    def get_frequency_response(self, *args, **kwargs):
        """Mock frequency response calculation."""
        return {
            "125": 30.0, "250": 35.0, "500": 40.0,
            "1000": 45.0, "2000": 50.0, "4000": 55.0
        }
    
    def calculate_surface_areas(self, dimensions):
        """Mock surface area calculation."""
        return {
            "floor": dimensions.get("length", 0) * dimensions.get("width", 0),
            "ceiling": dimensions.get("length", 0) * dimensions.get("width", 0),
            "walls": 2 * (dimensions.get("length", 0) + dimensions.get("width", 0)) * dimensions.get("height", 0)
        }
    
    def cleanup(self):
        """Mock cleanup method."""
        pass

def create_mock_acoustic_calculator():
    """Create a mock AcousticCalculator for testing."""
    return MockAcousticCalculator()

class MockCacheManager:
    """Mock implementation of CacheManager for testing."""
    
    def __init__(self):
        """Initialize the mock cache manager."""
        self.db = None
        self._stats = {
            'hits': 0,
            'misses': 0,
            'added': 0,
            'removed': 0
        }
    
    def get(self, *args, **kwargs):
        """Mock cache get operation."""
        self._stats['misses'] += 1
        return None
    
    def set(self, *args, **kwargs):
        """Mock cache set operation."""
        self._stats['added'] += 1
        return True
    
    def delete(self, *args, **kwargs):
        """Mock cache delete operation."""
        self._stats['removed'] += 1
        return True
    
    def clear(self, *args, **kwargs):
        """Mock cache clear operation."""
        self._stats['removed'] += 1
        return True
    
    def get_stats(self):
        """Return mock cache statistics."""
        return self._stats
    
    def cleanup(self):
        """Mock cleanup method."""
        self._stats = {
            'hits': 0,
            'misses': 0,
            'added': 0,
            'removed': 0
        }

def create_mock_cache_manager():
    """Create a mock CacheManager for testing."""
    return MockCacheManager()

class MockDBConnection:
    """Mock implementation of DB connection for testing."""
    
    def __init__(self):
        """Initialize the mock database connection."""
        self.client = MockMongoClient()
        self.database = MockDatabase()
    
    def get_collection(self, collection_name):
        """Mock get collection operation."""
        return MockCollection()
    
    def close(self):
        """Mock close connection operation."""
        pass
    
    def cleanup(self):
        """Mock cleanup method."""
        pass

class MockMongoClient:
    """Mock MongoDB client."""
    
    def close(self):
        """Mock close client operation."""
        pass

class MockDatabase:
    """Mock MongoDB database."""
    
    def get_collection(self, collection_name):
        """Mock get collection operation."""
        return MockCollection()

class MockCollection:
    """Mock MongoDB collection."""
    
    def find(self, *args, **kwargs):
        """Mock find operation."""
        return []
    
    def find_one(self, *args, **kwargs):
        """Mock find_one operation."""
        return None
    
    def insert_one(self, *args, **kwargs):
        """Mock insert_one operation."""
        return True
    
    def insert_many(self, *args, **kwargs):
        """Mock insert_many operation."""
        return True

class MockSolutionsManager:
    """Mock implementation of SolutionsManager for testing."""
    
    def __init__(self):
        """Initialize the mock solutions manager."""
        self.db = None
    
    def get_solutions(self, *args, **kwargs):
        """Mock get solutions operation."""
        return []
    
    def find_solutions(self, *args, **kwargs):
        """Mock find solutions operation."""
        return []
    
    def load_solutions_from_db(self, *args, **kwargs):
        """Mock load solutions from database operation."""
        return True
    
    def cleanup(self):
        """Mock cleanup method."""
        pass

def create_mock_db_connection():
    """Create a mock DB connection for testing."""
    return MockDBConnection()

def create_mock_solutions_manager():
    """Create a mock SolutionsManager for testing."""
    return MockSolutionsManager()

def setup_test_environment():
    """Set up a clean test environment with mock singletons."""
    # First reset all singletons
    reset_all_singletons()
    
    # Import modules and set up mocks
    try:
        # Create mock instances
        mock_db = create_mock_db_connection()
        mock_cache = create_mock_cache_manager()
        mock_solutions = create_mock_solutions_manager()
        
        # Set up dependencies for mock acoustic calculator
        mock_calc = MockAcousticCalculator()
        mock_calc.cache_manager = mock_cache
        mock_calc.solutions_manager = mock_solutions
        mock_calc.db = mock_db
        
        # Set up mock instances in their respective modules
        import solutions.acoustic_calculator as ac_module
        ac_module._acoustic_calculator_instance = mock_calc
        
        import solutions.cache_manager as cm_module
        cm_module._cache_manager = mock_cache
        
        import solutions.solutions_manager as sm_module
        sm_module._solutions_manager = mock_solutions
        
        import solutions.db_init as db_module
        db_module._db_connection = mock_db
        
        logger.info("Test environment setup complete with mock singletons")
    except Exception as e:
        logger.error(f"Error setting up test environment: {e}")

def teardown_test_environment():
    """Clean up test environment."""
    reset_all_singletons()
    logger.info("Test environment teardown complete")