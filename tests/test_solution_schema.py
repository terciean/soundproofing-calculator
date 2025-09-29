import logging
import pytest
from schemas.solution_schema import Solution

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_solution_schema():
    # Adjusted test data to match Solution schema requirements
    data = {
        "solution": "TestWall",
        "surface_type": "walls",
        "materials": [],
        "total_cost": 100.0,
        "notes": ["Sample note"]
    }
    solution = Solution(**data)
    assert solution.solution == "TestWall"
    assert solution.surface_type == "walls"
    assert solution.materials == []
    assert solution.total_cost == 100.0
    assert solution.notes == ["Sample note"]

def test_database_fetch():
    from testmongo import test_mongodb_connection
    assert test_mongodb_connection() is True

def test_calculator():
    from testmongo import test_material_calculations
    # Example: test material calculation for a known solution and dimensions
    test_material_calculations('M20 Solution (Standard)', {'length': 4, 'height': 2.4})
    assert True

def test_solution_characteristics():
    from testmongo import test_solution_structure
    assert test_solution_structure('M20WallStandard') is True
    assert test_solution_structure('GenieClipWallSP15') is True
    assert test_solution_structure('ResilientBarCeilingStandard') is True

def test_database_solution():
    from test_db_connection import test_collection_data
    assert test_collection_data('guyrazor', 'wallsolutions') is True
    assert test_collection_data('guyrazor', 'ceilingsolutions') is True
    assert test_collection_data('guyrazor', 'materials') is True

if __name__ == "__main__":
    logger.info("Starting tests...\n")
    
    tests = [
        ("Schema Validation", test_solution_schema),
        ("Database Integration", test_database_fetch),
        ("Calculator Integration", test_calculator),
        ("Solution Characteristics", test_solution_characteristics),
        ("Database Solution", test_database_solution)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
        logger.info("")
    
    logger.info("Test Summary:")
    for name, passed in results:
        status = "✓" if passed else "✗"
        logger.info(f"{status} {name}")