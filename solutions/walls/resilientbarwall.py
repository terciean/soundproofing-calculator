"""Resilient bar wall solution implementation.

This module implements the Resilient Bar Wall soundproofing solution, which provides
sound isolation through a specialized mounting system. The solution uses the following
key components and patterns:

1. Inheritance Structure:
   - Inherits from BaseSolution for core functionality
   - Provides specialized calculations for resilient bar construction
   - SP15 variant extends standard solution with enhanced materials

2. Data Handling:
   - Dimensions and materials are processed through the base calculator
   - Material properties are fetched from centralized material database
   - Caching is implemented for performance optimization
   - Results are structured with solution-specific calculations

3. Key Features:
   - Configurable plasterboard layers
   - Automated bar spacing and quantity calculations
   - Material waste factor calculations
   - Enhanced isolation features in SP15 variant
"""

import logging
from solutions.base_calculator import BaseCalculator
from solutions.solution_mapping_new import SolutionMapping
import math
from solutions.base_solution import BaseSolution
from solutions.material_properties import get_material_properties
from solutions.solutions import get_solutions_manager
from typing import Dict, List, Optional, Any
from solutions.config import SOLUTION_VARIANT_MONGO_IDS
from solutions.database import get_solution_by_id, get_db
from solutions.cache_manager import get_cache_manager

logger = logging.getLogger(__name__)

class ResilientBarWallStandard(BaseSolution):
    """Standard resilient bar wall solution.
    
    This class implements the standard resilient bar wall solution with the following features:
    - Double layer plasterboard construction
    - Optimized bar spacing
    - Material quantity calculations with waste factors
    - Cached characteristics for performance
    
    The calculation process:
    1. Base calculations from BaseSolution (dimensions, basic materials)
    2. Bar spacing and quantity optimization
    3. Plasterboard quantity calculation with waste factor
    4. Additional component calculations
    """
    
    CODE_NAME = "Resilient bar wall (Standard)"
    BAR_SPACING = 0.4  # 400mm spacing for resilient bars
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
        self.plasterboard_layers = 2  # Two layers by default
        
    def calculate(self, dimensions: Optional[Dict] = None, materials: Optional[List] = None) -> Dict[str, Any]:
        """Calculate solution properties with bar-specific additions"""
        try:
            # Get base calculation from parent
            base_result = super().calculate(dimensions, materials)
            if not base_result:
                return None
                
            # Add bar spacing calculations
            length = dimensions.get('width', self.length) if dimensions else self.length
            height = dimensions.get('height', self.height) if dimensions else self.height
            
            # Calculate number of bars needed
            bars_needed = math.ceil(length / self.BAR_SPACING)
            extra_bars = math.ceil(bars_needed * 0.1)  # 10% extra for cuts and waste
            
            # Calculate plasterboard quantities
            area = length * height
            plasterboard_quantity = area * self.plasterboard_layers * 1.1  # 10% waste
            
            # Log cache status
            cache_status = self.get_cache_status()
            logger.info(f"Cache status for {self.CODE_NAME}:")
            for key, status in cache_status.items():
                logger.info(f"  {key}: {'Cached' if status['cached'] else 'Not cached'} "
                          f"(Last updated: {status['last_updated']})")
            
            # Add to result without modifying cached base calculation
            result = base_result.copy()
            result['additional_info'] = {
                'bar_spacing': self.BAR_SPACING,
                'bars_needed': bars_needed,
                'extra_bars': extra_bars,
                'plasterboard_quantity': plasterboard_quantity,
                'plasterboard_layers': self.plasterboard_layers
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating ResilientBarWall: {e}")
            return None
            
    def get_characteristics(self) -> Dict[str, Any]:
        """Get solution characteristics with caching"""
        try:
            # Get base characteristics from cache or calculation
            characteristics = super().get_characteristics()
            
            # Log cache status
            cache_status = self.get_cache_status()
            logger.info(f"Characteristics cache status for {self.CODE_NAME}:")
            for key, status in cache_status.items():
                logger.info(f"  {key}: {'Cached' if status['cached'] else 'Not cached'} "
                          f"(Last updated: {status['last_updated']})")
            
            return characteristics
            
        except Exception as e:
            logger.error(f"Error getting characteristics: {e}")
            return {}

class ResilientBarWallSP15(ResilientBarWallStandard):
    """SP15 variant of resilient bar wall solution.
    
    This variant enhances the standard resilient bar wall with:
    - SP15 soundboard integration
    - Optimized single-layer construction
    - Higher STC rating (65)
    
    The SP15 variant modifies the standard solution by:
    1. Using specialized SP15 soundboard material
    2. Optimizing the plasterboard layer configuration
    3. Providing improved sound isolation characteristics
    """
    
    CODE_NAME = "Resilient bar wall (SP15 Soundboard Upgrade)"
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
        self.plasterboard_layers = 1  # Single layer for SP15
        
    def calculate(self, dimensions: Optional[Dict] = None, materials: Optional[List] = None) -> Dict[str, Any]:
        """Calculate SP15 solution properties"""
        try:
            # Get base calculation from parent
            result = super().calculate(dimensions, materials)
            if not result:
                return None
                
            # Log cache status
            cache_status = self.get_cache_status()
            logger.info(f"Cache status for {self.CODE_NAME}:")
            for key, status in cache_status.items():
                logger.info(f"  {key}: {'Cached' if status['cached'] else 'Not cached'} "
                          f"(Last updated: {status['last_updated']})")
            
            # Add SP15 specific info
            result['additional_info'].update({
                'sp15_soundboard': True,
                'plasterboard_layers': self.plasterboard_layers
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating SP15 ResilientBarWall: {e}")
            return None
            
    def get_characteristics(self) -> Dict[str, Any]:
        """Get SP15 variant characteristics"""
        try:
            # Get base characteristics from cache or calculation
            characteristics = super().get_characteristics()
            
            # Only modify if we got valid characteristics
            if characteristics:
                # Create a copy to avoid modifying cached data
                characteristics = characteristics.copy()
                characteristics.update({
                    'stc_rating': 65,  # Higher STC rating for SP15
                    'variant': 'SP15',
                    'description': 'Enhanced Resilient Bar Wall solution with improved sound isolation'
                })
                
            # Log cache status
            cache_status = self.get_cache_status()
            logger.info(f"Characteristics cache status for {self.CODE_NAME}:")
            for key, status in cache_status.items():
                logger.info(f"  {key}: {'Cached' if status['cached'] else 'Not cached'} "
                          f"(Last updated: {status['last_updated']})")
            
            return characteristics
            
        except Exception as e:
            logger.error(f"Error getting SP15 characteristics: {e}")
            return {}

def load_resilientbarwall_solutions():
    """Load Resilient Bar Wall solutions (Standard and SP15) from MongoDB and cache them."""
    from solutions.database import diagnose_missing_document
    cache_manager = get_cache_manager()
    ids = SOLUTION_VARIANT_MONGO_IDS['walls']
    standard_id = ids['ResilientBarWallStandard']
    sp15_id = ids['ResilientBarWallSP15']
    standard_doc = get_solution_by_id('wallsolutions', standard_id)
    if standard_doc:
        print(f"[DEBUG] ResilientBarWallStandard ({standard_id}) keys: {list(standard_doc.keys())}")
    else:
        print(f"[WARN] ResilientBarWallStandard ({standard_id}) not found.")
    sp15_doc = get_solution_by_id('wallsolutions', sp15_id)
    if sp15_doc:
        print(f"[DEBUG] ResilientBarWallSP15 ({sp15_id}) keys: {list(sp15_doc.keys())}")
    else:
        print(f"[WARN] ResilientBarWallSP15 ({sp15_id}) not found.")
    standard = ResilientBarWallStandard() if standard_doc else None
    sp15 = ResilientBarWallSP15() if sp15_doc else None
    if standard:
        standard._solution_data = standard_doc
        cache_manager.set('resilientbarwall_standard', standard, 3600)
    if sp15:
        sp15._solution_data = sp15_doc
        cache_manager.set('resilientbarwall_sp15', sp15, 3600)
    return standard, sp15