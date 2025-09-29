"""
Cost calculation module for soundproofing solutions.
"""

from typing import Dict, List, Any, Optional
from .base_calculator import BaseCalculator
from .cache_manager import get_cache_manager
from .logger import get_logger
from solutions.database import get_solution_by_id, get_all_materials_from_db

# Set up logging
logger = get_logger()

def calculate_material_cost(solution_id: str, dimensions: Dict[str, float]) -> float:
    """Calculate total cost for a solution based on dimensions using new loader."""
    try:
        cache_params = {
            'solution_id': solution_id,
            'dimensions': dimensions
        }
        cache_manager = get_cache_manager()
        cached_cost = cache_manager.get_cached_calculation('material_cost', cache_params)
        if cached_cost is not None:
            logger.info(f"Using cached cost for solution {solution_id}")
            return cached_cost
        solution = get_solution_by_id(solution_id)
        if not solution or 'materials' not in solution:
            logger.warning(f"Solution {solution_id} not found or has no materials")
            return 0.0
        calculator = BaseCalculator(dimensions['length'], dimensions['height'])
        costs = calculator.calculate_costs(calculator.area)
        if not costs:
            return 0.0
        total_cost = costs['breakdown']['totalCost']
        return total_cost
    except Exception as e:
        logger.error(f"Error calculating material cost: {str(e)}")
        return 0.0

def get_material_cost(material_name: str) -> Optional[float]:
    """Get cost for a specific material using new loader."""
    try:
        materials = get_all_materials_from_db()
        material = next((m for m in materials if m.get('name') == material_name), None)
        if material and "cost" in material:
            return float(material["cost"])
        return None
    except Exception as e:
        logger.error(f"Error getting material cost: {e}")
        return None

def calculate_material_quantity(material: Dict, areas: Dict) -> float:
    """Calculate quantity of material needed based on area using BaseCalculator"""
    try:
        # Create calculator instance with the largest dimension
        max_dimension = max(areas.values())
        calculator = BaseCalculator(max_dimension, max_dimension)
        
        # Calculate quantity using BaseCalculator
        return calculator.calculate_material_quantity(material)
        
    except Exception as e:
        logger.error(f"Error calculating material quantity: {str(e)}")
        return 0.0

def calculate_solution_costs(recommendations: Dict[str, Any], dimensions: Dict[str, float], blockages: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    """Calculate costs for all recommended solutions"""
    costs = {
        'wall': 0.0,
        'ceiling': 0.0,
        'floor': 0.0,
        'total': 0.0
    }
    
    try:
        # Calculate wall costs
        if 'walls' in recommendations.get('primary', {}):
            for wall_rec in recommendations['primary']['walls']:
                wall_cost = calculate_material_cost(wall_rec['solution'], dimensions)
                costs['wall'] += wall_cost
                
        # Calculate ceiling costs
        if 'ceiling' in recommendations.get('primary', {}):
            ceiling_solution = recommendations['primary']['ceiling'].get('solution')
            if ceiling_solution:
                costs['ceiling'] = calculate_material_cost(ceiling_solution, dimensions)
                
        # Calculate floor costs
        if 'floor' in recommendations.get('primary', {}):
            floor_solution = recommendations['primary']['floor'].get('solution')
            if floor_solution:
                costs['floor'] = calculate_material_cost(floor_solution, dimensions)
                
        # Apply blockage adjustments if provided
        if blockages:
            # Adjust wall costs for blockages
            if 'walls' in blockages:
                blockage_area = sum(b.get('area', 0) for b in blockages['walls'])
                total_area = dimensions['length'] * dimensions['height']
                if total_area > 0:
                    costs['wall'] *= (1 - blockage_area / total_area)
                    
            # Adjust ceiling costs for blockages
            if 'ceiling' in blockages:
                blockage_area = blockages['ceiling'].get('area', 0)
                total_area = dimensions['length'] * dimensions['width']
                if total_area > 0:
                    costs['ceiling'] *= (1 - blockage_area / total_area)
                    
            # Adjust floor costs for blockages
            if 'floor' in blockages:
                blockage_area = blockages['floor'].get('area', 0)
                total_area = dimensions['length'] * dimensions['width']
                if total_area > 0:
                    costs['floor'] *= (1 - blockage_area / total_area)
                    
        # Calculate total cost
        costs['total'] = costs['wall'] + costs['ceiling'] + costs['floor']
        
        return costs
        
    except Exception as e:
        logger.error(f"Error calculating solution costs: {str(e)}")
        return costs 