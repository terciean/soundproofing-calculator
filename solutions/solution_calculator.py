"""
Solution calculator module for generating implementation details.
"""

from typing import Dict, Any, List, Optional
import math
from solutions.logger import get_logger
import logging

from solutions.cache_manager import get_cache_manager

# Set up logging
logger = get_logger()

# Skill level mapping for solutions
SKILL_LEVELS = {
    'IndependentWallStandard': 'Professional',
    'IndependentWallSP15': 'Professional',
    'ResilientBarWallStandard': 'Professional',
    'ResilientBarWallSP15': 'Professional',
    'GenieClipWallStandard': 'Professional',
    'GenieClipWallSP15': 'Professional',
    'M20WallStandard': 'Professional',
    'M20WallSP15': 'Professional',
    'ResilientBarCeilingStandard': 'Professional',
    'ResilientBarCeilingSP15': 'Professional',
    'GenieClipCeilingStandard': 'Professional',
    'GenieClipCeilingSP15': 'Professional',
    'LB3GenieClipCeilingStandard': 'Professional',
    'LB3GenieClipCeilingSP15': 'Professional',
    'IndependentCeilingStandard': 'Professional',
    'IndependentCeilingSP15': 'Professional',
    'FloatingFloorStandard': 'Professional',
    'IsolationMatFloor': 'Professional'
}

def get_solution_with_cache_priority(solution_name, solution_type):
    """
    Gets a solution from cache.
    Returns the solution if found, None otherwise.
    
    Args:
        solution_name: Name of the solution to retrieve
        solution_type: Type of solution (e.g., 'wallsolutions', 'floorsolutions', 'ceilingsolutions')
    
    Returns:
        dict: The solution if found, None otherwise
    """
    logger.debug(f"Attempting to retrieve solution: {solution_name} (Type: {solution_type})")
    
    # Get cache manager
    cache_manager = get_cache_manager()
    if cache_manager is None:
        logger.warning("Cache manager not available")
        return None
    
    # Try to get from cache
    cache_key = f"db_solution_{solution_name}"
    cached_solution = cache_manager.get(cache_key)
    
    if cached_solution:
        logger.debug(f"Cache HIT for solution: {solution_name}")
        return cached_solution
    
    logger.debug(f"Cache MISS for solution: {solution_name}")
    return None

def get_materials_with_cache_priority():
    """
    Gets all materials from cache.
    Returns the materials if found, empty list otherwise.
    
    Returns:
        list: The materials if found, empty list otherwise
    """
    logger.debug("Attempting to retrieve all materials")
    
    # Get cache manager
    cache_manager = get_cache_manager()
    if not cache_manager:
        logger.warning("Cache manager not available")
        return []
    
    # Try to get from cache
    cache_key = "all_materials"
    cached_materials = cache_manager.get(cache_key)
    
    if cached_materials:
        logger.debug(f"Cache HIT for all materials (count: {len(cached_materials)})")
        return cached_materials
    
    logger.debug("Cache MISS for all materials")
    return []

def get_solutions_manager():
    """
    Get the solutions manager instance that handles solution management and calculations.
    
    Returns:
        SoundproofingSolutions: Instance of the solutions manager
    """
    try:
        from solutions.solutions import get_solutions_manager as get_global_solutions_manager
        solutions_manager = get_global_solutions_manager()
        if solutions_manager is None:
            logger.error("Failed to initialize solutions manager - returned None")
            return None
        return solutions_manager
    except Exception as e:
        logger.error(f"Error initializing solutions manager: {str(e)}")
        return None

def calculate_solution(solution_name, dimensions, solution_type="wallsolutions"):
    """
    Calculate a solution based on given dimensions with cache prioritization
    
    Args:
        solution_name: The solution identifier
        dimensions: A dictionary with length, width, and height dimensions
        solution_type: The type of solution (collection name)
        
    Returns:
        Dictionary with calculation results or None if failed
    """
    import logging
    from solutions.cache_manager import get_cache_manager
    
    logger = logging.getLogger(__name__)
    logger.info(f"Calculating solution {solution_name} with dimensions: {dimensions}")
    
    try:
        # Generate cache key for this calculation
        dims_hash = hash(f"{dimensions.get('length', 0)}_{dimensions.get('width', 0)}_{dimensions.get('height', 0)}")
        cache_key = f"solution_calc_{solution_name}_{dims_hash}"
        
        # Try to get from cache first
        cache_manager = get_cache_manager()
        if cache_manager is not None:
            cached_result = cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Retrieved calculation for {solution_name} from cache")
                return cached_result
        
        # Cache miss, calculate solution
        logger.info(f"Cache miss for solution {solution_name}, calculating...")
        
        # Get solution data with cache priority
        solution_data = get_solution_with_cache_priority(solution_name, solution_type)
        if not solution_data:
            logger.error(f"No solution data found for {solution_name}")
            return None
        
        # Get materials with cache priority
        materials = get_materials_with_cache_priority()
        
        # Get calculator for solution
        from solutions.solution_mapping_new import SolutionMapping
        calculator = SolutionMapping.get_calculator(
            solution_name,
            float(dimensions.get('length', 0)),
            float(dimensions.get('height', 0))
        )
        
        if not calculator:
            logger.error(f"No calculator found for solution: {solution_name}")
            return None
        
        # Log calculator info
        logger.info(f"Using calculator: {calculator.__class__.__name__} for solution {solution_name}")
        
        # Calculate with materials if available
        if materials:
            result = calculator.calculate(dimensions, materials)
        else:
            result = calculator.calculate(dimensions)
        
        if not result:
            logger.warning(f"Calculation returned no results for {solution_name}")
            return None
        
        # Cache the result
        if cache_manager is not None and result:
            cache_success = cache_manager.set(cache_key, result, 3600)  # 1 hour TTL
            if cache_success:
                logger.info(f"Cached calculation result for {solution_name}")
            else:
                logger.warning(f"Failed to cache calculation for {solution_name}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error calculating solution {solution_name}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None





def generate_implementation_details_detailed(solution_id, surface_type, dimensions=None, surfaces=None, solutions_manager=None):
    """
    Generate implementation details for a solution with detailed logging
    
    Args:
        solution_id (str): Solution identifier
        dimensions (dict): Room dimensions
        surfaces (dict): Surface details (optional)
        solutions_manager: Solution manager instance (optional)
        
    Returns:
        Dict with implementation details or None if failed
    """
    import logging
    from solutions.cache_manager import get_cache_manager
    
    logger = logging.getLogger(__name__)
    logger.info(f"Generating implementation details for solution {solution_id}")
    
    try:
        # Try to get from cache first
        cache_key = f"implementation_{solution_id}_{hash(str(dimensions))}"
        cache_manager = get_cache_manager()
        cached_result = cache_manager.get(cache_key)
        
        if cached_result:
            logger.info(f"Retrieved implementation details for {solution_id} from cache")
            return cached_result
            
        logger.info(f"Cache miss for implementation details of solution {solution_id}, generating...")
        
        # Parse dimensions
        if not dimensions:
            dimensions = {"length": 0, "width": 0, "height": 0}
            
        # Get SolutionMapping
        from solutions.solution_mapping_new import SolutionMapping
        
        # Get solution database record if possible
        from solutions.database import get_solution, get_collection_for_solution
        
        collection_name = f"{surface_type}solutions"
            
        solution_record = None
        if collection_name:
            try:
                logger.info(f"Looking up solution in {collection_name} collection")
                solution_record = get_solution(solution_id, collection_name)
                if solution_record:
                    logger.info(f"Found solution record in database: {solution_id}")
                else:
                    logger.warning(f"Solution record not found in database: {solution_id}")
            except Exception as db_error:
                logger.error(f"Error retrieving solution from database: {db_error}")
                
        # Calculate solution
        calculation_result = calculate_solution(solution_id, dimensions, collection_name)
        if not calculation_result:
            logger.warning(f"No calculation results available for {solution_id}")
            
        # Combine data sources
        implementation = {
            "solution_id": solution_id,
            "name": solution_id,
            "dimensions": dimensions,
            "calculation": calculation_result,
            "database": solution_record,
            "data_source": "calculation"
        }
        
        # Set data source
        if solution_record:
            implementation["data_source"] = "database+calculation"
            implementation["name"] = solution_record.get("solution", solution_id)
            
        # Cache the result
        if cache_manager:
            cache_success = cache_manager.set(cache_key, implementation, 3600)  # 1 hour TTL
            if cache_success:
                logger.info(f"Cached implementation details for {solution_id}")
            else:
                logger.warning(f"Failed to cache implementation details for {solution_id}")
                
        return implementation
        
    except Exception as e:
        logger.error(f"Error generating implementation details for {solution_id}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None



