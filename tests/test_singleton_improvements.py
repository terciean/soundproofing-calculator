"""Test suite for singleton pattern improvements."""

import unittest
import threading
import time
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tests.utils.singleton_reset import (
    reset_all_singletons,
    reset_acoustic_calculator,
    reset_cache_manager,
    reset_db_connection,
    reset_solutions_manager,
    setup_test_environment,
    teardown_test_environment
)

class TestSingletonThreadSafety(unittest.TestCase):
    """Test thread safety of singleton implementations."""
    
    def setUp(self):
        """Set up test environment."""
        setup_test_environment()
    
    def tearDown(self):
        """Clean up test environment."""
        teardown_test_environment()
    
    def test_acoustic_calculator_thread_safety(self):
        """Test that AcousticCalculator singleton is thread-safe."""
        from solutions.acoustic_calculator import get_acoustic_calculator
        
        instances = []
        errors = []
        
        def create_instance():
            try:
                instance = get_acoustic_calculator()
                instances.append(instance)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=create_instance)
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
        self.assertEqual(len(instances), 10, "Not all threads created instances")
        
        # All instances should be the same object
        first_instance = instances[0]
        for instance in instances[1:]:
            self.assertIs(instance, first_instance, "Instances are not the same object")
    
    def test_cache_manager_thread_safety(self):
        """Test that CacheManager singleton is thread-safe."""
        from solutions.cache_manager import get_cache_manager
        
        instances = []
        errors = []
        
        def create_instance():
            try:
                instance = get_cache_manager()
                instances.append(instance)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=create_instance)
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
        self.assertEqual(len(instances), 10, "Not all threads created instances")
        
        # All instances should be the same object
        first_instance = instances[0]
        for instance in instances[1:]:
            self.assertIs(instance, first_instance, "Instances are not the same object")
    
    def test_db_connection_thread_safety(self):
        """Test that database connection singleton is thread-safe."""
        from solutions.db_init import get_db
        
        # Mock the database connection to avoid actual DB calls
        with patch('solutions.db_init.MongoClient') as mock_client:
            mock_db = MagicMock()
            mock_client.return_value.__getitem__.return_value = mock_db
            mock_client.return_value.admin.command.return_value = True
            
            instances = []
            errors = []
            
            def create_instance():
                try:
                    instance = get_db()
                    instances.append(instance)
                except Exception as e:
                    errors.append(e)
            
            # Create multiple threads
            threads = []
            for _ in range(10):
                thread = threading.Thread(target=create_instance)
                threads.append(thread)
            
            # Start all threads
            for thread in threads:
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Check results
            self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
            
            # Filter out None instances (due to reconnection interval)
            valid_instances = [i for i in instances if i is not None]
            if valid_instances:
                # All valid instances should be the same object
                first_instance = valid_instances[0]
                for instance in valid_instances[1:]:
                    self.assertIs(instance, first_instance, "Instances are not the same object")

class TestSingletonReset(unittest.TestCase):
    """Test singleton reset functionality."""
    
    def test_acoustic_calculator_reset(self):
        """Test resetting AcousticCalculator singleton."""
        from solutions.acoustic_calculator import get_acoustic_calculator
        
        # Create first instance
        instance1 = get_acoustic_calculator()
        self.assertIsNotNone(instance1)
        
        # Reset singleton
        reset_acoustic_calculator()
        
        # Create second instance
        instance2 = get_acoustic_calculator()
        self.assertIsNotNone(instance2)
        
        # Instances should be different objects
        self.assertIsNot(instance1, instance2)
    
    def test_cache_manager_reset(self):
        """Test resetting CacheManager singleton."""
        from solutions.cache_manager import get_cache_manager
        
        # Create first instance
        instance1 = get_cache_manager()
        self.assertIsNotNone(instance1)
        
        # Reset singleton
        reset_cache_manager()
        
        # Create second instance
        instance2 = get_cache_manager()
        self.assertIsNotNone(instance2)
        
        # Instances should be different objects
        self.assertIsNot(instance1, instance2)
    
    def test_all_singletons_reset(self):
        """Test resetting all singletons."""
        from solutions.acoustic_calculator import get_acoustic_calculator
        from solutions.cache_manager import get_cache_manager
        
        # Create instances
        calc1 = get_acoustic_calculator()
        cache1 = get_cache_manager()
        
        # Reset all singletons
        reset_all_singletons()
        
        # Create new instances
        calc2 = get_acoustic_calculator()
        cache2 = get_cache_manager()
        
        # All instances should be different
        self.assertIsNot(calc1, calc2)
        self.assertIsNot(cache1, cache2)

class TestSingletonPerformance(unittest.TestCase):
    """Test performance characteristics of singleton implementations."""
    
    def setUp(self):
        """Set up test environment."""
        setup_test_environment()
    
    def tearDown(self):
        """Clean up test environment."""
        teardown_test_environment()
    
    def test_acoustic_calculator_performance(self):
        """Test performance of AcousticCalculator singleton access."""
        from solutions.acoustic_calculator import get_acoustic_calculator
        
        # Measure time for multiple accesses
        start_time = time.time()
        
        for _ in range(1000):
            instance = get_acoustic_calculator()
            self.assertIsNotNone(instance)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should be very fast (less than 1 second for 1000 accesses)
        self.assertLess(elapsed, 1.0, f"Singleton access too slow: {elapsed:.3f}s")
    
    def test_cache_manager_performance(self):
        """Test performance of CacheManager singleton access."""
        from solutions.cache_manager import get_cache_manager
        
        # Measure time for multiple accesses
        start_time = time.time()
        
        for _ in range(1000):
            instance = get_cache_manager()
            self.assertIsNotNone(instance)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should be very fast (less than 1 second for 1000 accesses)
        self.assertLess(elapsed, 1.0, f"Singleton access too slow: {elapsed:.3f}s")

class TestSingletonIntegration(unittest.TestCase):
    """Test integration between different singletons."""
    
    def setUp(self):
        """Set up test environment."""
        setup_test_environment()
    
    def tearDown(self):
        """Clean up test environment."""
        teardown_test_environment()
    
    def test_acoustic_calculator_dependencies(self):
        """Test that AcousticCalculator properly initializes its dependencies."""
        from solutions.acoustic_calculator import get_acoustic_calculator
        
        calculator = get_acoustic_calculator()
        
        # Check that dependencies are initialized
        self.assertIsNotNone(calculator.cache_manager)
        self.assertIsNotNone(calculator.solutions_manager)
        # Note: db might be None in test environment
    
    def test_singleton_consistency(self):
        """Test that singletons maintain consistency across the application."""
        from solutions.acoustic_calculator import get_acoustic_calculator
        from solutions.cache_manager import get_cache_manager
        
        # Get instances
        calculator = get_acoustic_calculator()
        cache_manager = get_cache_manager()
        
        # The calculator should use the same cache manager instance
        self.assertIs(calculator.cache_manager, cache_manager)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)