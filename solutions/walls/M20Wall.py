"""M20 wall solution implementation."""

import logging
from solutions.base_calculator import BaseCalculator
from solutions.base_solution import BaseSolution
from solutions.material_properties import get_material_properties
from solutions.solution_calculator import get_solutions_manager
from typing import Dict, List, Optional, Any
import math
from solutions.walls.base_wall import BaseWall
from solutions.config import SOLUTION_VARIANT_MONGO_IDS
from solutions.database import get_solution_by_id, get_db
from solutions.cache_manager import get_cache_manager

logger = logging.getLogger(__name__)

class M20WallStandard(BaseWall):
    """Standard M20 Wall solution"""
    
    CODE_NAME = "M20 Solution (Standard)"
    PANEL_SPACING = 0.6  # 600mm spacing for M20 panels
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
        self.panel_layers = 2  # Two layers by default
        
    def calculate(self, dimensions: Optional[Dict] = None, materials: Optional[List] = None) -> Dict[str, Any]:
        """Calculate solution properties with M20-specific additions"""
        try:
            # Get base calculation from parent
            base_result = super().calculate(dimensions, materials)
            if not base_result:
                return None
                
            # Add panel spacing calculations
            length = dimensions.get('width', self.length) if dimensions else self.length
            height = dimensions.get('height', self.height) if dimensions else self.height
            
            # Calculate number of panels needed
            area = length * height
            panels_needed = math.ceil(area / (self.PANEL_SPACING * self.PANEL_SPACING))
            extra_panels = math.ceil(panels_needed * 0.1)  # 10% extra for cuts
            
            # Calculate rubber mount quantities
            mounts_per_panel = 4
            total_mounts = (panels_needed + extra_panels) * mounts_per_panel
            
            # Log cache status
            cache_status = self.get_cache_status()
            logger.info(f"Cache status for {self.CODE_NAME}:")
            for key, status in cache_status.items():
                logger.info(f"  {key}: {'Cached' if status['cached'] else 'Not cached'} "
                          f"(Last updated: {status['last_updated']})")
            
            # Add to result without modifying cached base calculation
            result = base_result.copy()
            result['additional_info'] = {
                'panel_spacing': self.PANEL_SPACING,
                'panels_needed': panels_needed,
                'extra_panels': extra_panels,
                'total_mounts': total_mounts,
                'panel_layers': self.panel_layers
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating M20Wall: {e}")
            return None
            
    def get_characteristics(self) -> Dict[str, Any]:
        """Get solution characteristics with caching"""
        try:
            # Get base characteristics from cache or calculation
            characteristics = super().get_characteristics()
            
            # Log cache status
            cache_status = self.get_cache_status()
            logger.info(f"[SOLUTION DATA] {self.CODE_NAME} cache status:")
            for key, status in cache_status.items():
                logger.info(f"[SOLUTION DATA]   {key}: {'CACHED' if status['cached'] else 'NOT CACHED'} "
                          f"(Last updated: {status['last_updated']})")
            
            # Log the solution details
            if characteristics:
                logger.info(f"[SOLUTION DATA] {self.CODE_NAME} details: "
                          f"STC Rating: {characteristics.get('stc_rating', 'N/A')}, "
                          f"Sound Reduction: {characteristics.get('sound_reduction', 'N/A')}, "
                          f"Frequency Range: {characteristics.get('frequencyRange', 'N/A')}")
            else:
                logger.warning(f"[SOLUTION DATA] {self.CODE_NAME}: NO DATA AVAILABLE")
            
            return characteristics
            
        except Exception as e:
            logger.error(f"[SOLUTION DATA] Error getting characteristics for {self.CODE_NAME}: {e}")
            return {}

class M20WallSP15(M20WallStandard):
    """SP15 variant of M20 Wall solution"""
    
    CODE_NAME = "M20 Solution (SP15 Soundboard upgrade)"
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
        self.panel_layers = 1  # Single layer for SP15
        
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
                'panel_layers': self.panel_layers,
                'enhanced_mounts': True  # SP15 uses enhanced rubber mounts
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating SP15 M20Wall: {e}")
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
                    'description': 'Enhanced M20 Wall solution with improved sound isolation'
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

def load_m20wall_solutions():
    """Load M20 Wall solutions (Standard and SP15) from MongoDB and cache them."""
    from solutions.database import diagnose_missing_document
    cache_manager = get_cache_manager()
    ids = SOLUTION_VARIANT_MONGO_IDS['walls']
    standard_id = ids['M20WallStandard']
    sp15_id = ids['M20WallSP15']
    standard_doc = get_solution_by_id('wallsolutions', standard_id)
    if standard_doc:
        print(f"[DEBUG] M20WallStandard ({standard_id}) keys: {list(standard_doc.keys())}")
    else:
        print(f"[WARN] M20WallStandard ({standard_id}) not found.")
    sp15_doc = get_solution_by_id('wallsolutions', sp15_id)
    if sp15_doc:
        print(f"[DEBUG] M20WallSP15 ({sp15_id}) keys: {list(sp15_doc.keys())}")
    else:
        print(f"[WARN] M20WallSP15 ({sp15_id}) not found.")
    standard = M20WallStandard() if standard_doc else None
    sp15 = M20WallSP15() if sp15_doc else None
    if standard:
        standard._solution_data = standard_doc
        cache_manager.set('m20wall_standard', standard, 3600)
    if sp15:
        sp15._solution_data = sp15_doc
        cache_manager.set('m20wall_sp15', sp15, 3600)
    return standard, sp15