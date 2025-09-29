"""Independent ceiling solution implementation.

This module implements the Independent Ceiling soundproofing solution, which provides
superior sound isolation through a completely separate ceiling structure. The solution
uses the following key components and patterns:

1. Inheritance Structure:
   - Inherits from BaseSolution for core functionality
   - Provides specialized calculations for independent ceiling construction
   - SP15 variant extends standard solution with enhanced materials

2. Data Handling:
   - Dimensions and materials are processed through the base calculator
   - Material properties are fetched from centralized material database
   - Caching is implemented for performance optimization
   - Results are structured with solution-specific calculations

3. Key Features:
   - Configurable plasterboard layers
   - Automated joist spacing and quantity calculations
   - Material waste factor calculations
   - Enhanced isolation features in SP15 variant
"""

import logging
from solutions.base_calculator import BaseCalculator
from solutions.base_solution import BaseSolution
from solutions.material_properties import get_material_properties
from solutions.solutions import get_solutions_manager
from typing import Dict, List, Optional, Any
import math
from solutions.config import SOLUTION_VARIANT_MONGO_IDS
from solutions.database import get_solution_by_id, get_db
from solutions.cache_manager import get_cache_manager
from solutions.base_sp15 import BaseSP15Solution

logger = logging.getLogger(__name__)

class IndependentCeilingStandard(BaseSolution):
    """Standard independent ceiling solution.
    
    This class implements the standard independent ceiling solution with the following features:
    - Double layer plasterboard construction
    - Standard joist spacing optimization
    - Material quantity calculations with waste factors
    - Cached characteristics for performance
    
    The calculation process:
    1. Base calculations from BaseSolution (dimensions, basic materials)
    2. Joist spacing and quantity optimization
    3. Plasterboard quantity calculation with waste factor
    4. Additional component calculations
    """
    
    CODE_NAME = "Independent Ceiling (Standard)"
    JOIST_SPACING = 0.4  # 400mm spacing for ceiling joists
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
        self.plasterboard_layers = 2  # Two layers by default
        
    def calculate(self, dimensions: Optional[Dict] = None, materials: Optional[List] = None) -> Dict[str, Any]:
        """Calculate solution properties with independent ceiling specific additions"""
        try:
            # Get base calculation from parent
            base_result = super().calculate(dimensions, materials)
            if not base_result:
                return None
                
            # Add joist spacing calculations
            length = dimensions.get('width', self.length) if dimensions else self.length
            height = dimensions.get('height', self.height) if dimensions else self.height
            
            # Calculate area and joist quantities
            area = length * height
            joists_needed = math.ceil(length / self.JOIST_SPACING)
            extra_joists = math.ceil(joists_needed * 0.1)  # 10% extra for cuts
            
            # Calculate hanger quantities
            hangers_per_joist = math.ceil(height / 1.2)  # One hanger every 1.2m
            total_hangers = (joists_needed + extra_joists) * hangers_per_joist
            
            # Calculate plasterboard quantities
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
                'joist_spacing': self.JOIST_SPACING,
                'joists_needed': joists_needed,
                'extra_joists': extra_joists,
                'total_hangers': total_hangers,
                'plasterboard_quantity': plasterboard_quantity,
                'plasterboard_layers': self.plasterboard_layers
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating IndependentCeiling: {e}")
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

class IndependentCeilingSP15(BaseSP15Solution, IndependentCeilingStandard):
    """SP15 variant of independent ceiling solution.
    
    This variant enhances the standard independent ceiling with:
    - SP15 soundboard integration
    - Enhanced isolation hangers and joists
    - Optimized single-layer construction
    - Higher STC rating (65)
    
    The SP15 variant modifies the standard solution by:
    1. Using specialized SP15 soundboard material
    2. Implementing enhanced isolation hangers and joists
    3. Optimizing the plasterboard layer configuration
    4. Providing improved sound isolation characteristics
    """
    
    CODE_NAME = "Independent Ceiling (SP15 Soundboard Upgrade)"
    
    def __init__(self, length: float = 0, height: float = 0):
        BaseSP15Solution.__init__(self, length, height)
        IndependentCeilingStandard.__init__(self, length, height)
        
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
                'plasterboard_layers': self.plasterboard_layers,
                'enhanced_hangers': True,  # SP15 uses enhanced isolation hangers
                'enhanced_joists': True    # SP15 uses enhanced isolation joists
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating SP15 IndependentCeiling: {e}")
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
                    'description': 'Enhanced Independent Ceiling solution with improved sound isolation'
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

def load_independentceiling_solutions():
    """Load Independent Ceiling solutions (Standard and SP15) from MongoDB and cache them."""
    from solutions.database import diagnose_missing_document
    cache_manager = get_cache_manager()
    ids = SOLUTION_VARIANT_MONGO_IDS['ceilings']
    standard_id = ids['IndependentCeilingStandard']
    sp15_id = ids['IndependentCeilingSP15']
    
    # Get documents from database
    standard_doc = get_solution_by_id('ceilingsolutions', standard_id)
    sp15_doc = get_solution_by_id('ceilingsolutions', sp15_id)
    
    # Create solution objects only if documents exist
    standard = None
    sp15 = None
    
    if standard_doc:
        try:
            standard = IndependentCeilingStandard()
            standard._solution_data = standard_doc
            cache_manager.set('independentceiling_standard', standard, 3600)
            logger.info(f"Successfully loaded IndependentCeilingStandard with {len(standard_doc.get('materials', []))} materials")
        except Exception as e:
            logger.error(f"Error creating IndependentCeilingStandard: {e}")
            standard = None
    else:
        logger.warning(f"IndependentCeilingStandard document not found with ID: {standard_id}")
    
    if sp15_doc:
        try:
            sp15 = IndependentCeilingSP15()
            sp15._solution_data = sp15_doc
            cache_manager.set('independentceiling_sp15', sp15, 3600)
            logger.info(f"Successfully loaded IndependentCeilingSP15 with {len(sp15_doc.get('materials', []))} materials")
        except Exception as e:
            logger.error(f"Error creating IndependentCeilingSP15: {e}")
            sp15 = None
    else:
        logger.warning(f"IndependentCeilingSP15 document not found with ID: {sp15_id}")
    
    return standard, sp15