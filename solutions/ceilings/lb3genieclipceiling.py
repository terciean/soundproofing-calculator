"""
LB3 genie clip ceiling solution implementation.
"""

import logging
from solutions.base_calculator import BaseCalculator
from solutions.base_solution import BaseSolution
from solutions.database import get_solution_by_id, get_db
from typing import Dict, List, Optional, Any
from solutions.material_properties import get_material_properties
from solutions.solutions import get_solutions_manager
import math
from solutions.config import CLIP_SPACING, SOLUTION_VARIANT_MONGO_IDS
from solutions.cache_manager import get_cache_manager
from solutions.base_sp15 import BaseSP15Solution

logger = logging.getLogger(__name__)

class LB3GenieClipCeilingStandard(BaseSolution):
    """Standard LB3 GenieClip ceiling solution"""
    
    CODE_NAME = "LB3GenieClipCeilingStandard"
    from solutions.config import CLIP_SPACING
    CLIP_SPACING = CLIP_SPACING['lb3_genie_clip']  # Use centralized clip spacing constant
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
        self.logger = logging.getLogger(__name__)
        self.solution_name = "LB3GenieClipCeilingStandard"
        self._load_solution_data(self.CODE_NAME)
        self._load_material_properties()
        self.plasterboard_layers = 2  # Two layers by default
        
    def calculate(self, dimensions: Optional[Dict] = None, materials: Optional[List] = None) -> Dict[str, Any]:
        """Calculate solution properties with LB3-specific additions"""
        try:
            # Get base calculation from parent
            base_result = super().calculate(dimensions, materials)
            if not base_result:
                return None
                
            # Add clip spacing calculations
            length = dimensions.get('width', self.length) if dimensions else self.length
            height = dimensions.get('height', self.height) if dimensions else self.height
            
            # Calculate area and clip quantities
            area = length * height
            clips_per_sqm = 1 / (self.CLIP_SPACING * self.CLIP_SPACING)
            clips_needed = math.ceil(area * clips_per_sqm)
            extra_clips = math.ceil(clips_needed * 0.1)  # 10% extra for corners and edges
            
            # Calculate channel quantities
            channel_spacing = 0.4  # 400mm spacing for channels
            channels_needed = math.ceil(length / channel_spacing)
            extra_channels = math.ceil(channels_needed * 0.1)  # 10% extra
            
            # Calculate LB3 bracket quantities
            brackets_per_clip = 1  # One bracket per clip
            total_brackets = (clips_needed + extra_clips) * brackets_per_clip
            
            # Log cache status
            cache_status = self.get_cache_status()
            logger.info(f"Cache status for {self.CODE_NAME}:")
            for key, status in cache_status.items():
                logger.info(f"  {key}: {'Cached' if status['cached'] else 'Not cached'} "
                          f"(Last updated: {status['last_updated']})")
            
            # Add to result without modifying cached base calculation
            result = base_result.copy()
            result['additional_info'] = {
                'clip_spacing': self.CLIP_SPACING,
                'clips_needed': clips_needed,
                'extra_clips': extra_clips,
                'channels_needed': channels_needed,
                'extra_channels': extra_channels,
                'total_brackets': total_brackets,
                'plasterboard_layers': self.plasterboard_layers
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating LB3GenieClipCeiling: {e}")
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

class LB3GenieClipCeilingSP15(LB3GenieClipCeilingStandard):
    """SP15 variant of LB3 GenieClip ceiling solution"""
    
    CODE_NAME = "LB3GenieClipCeilingSP15"
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
        self.logger = logging.getLogger(__name__)
        self.solution_name = "LB3GenieClipCeilingSP15"
        self._load_solution_data(self.CODE_NAME)
        self._load_material_properties()
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
                'plasterboard_layers': self.plasterboard_layers,
                'enhanced_clips': True,  # SP15 uses enhanced isolation clips
                'enhanced_brackets': True  # SP15 uses enhanced LB3 brackets
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating SP15 LB3GenieClipCeiling: {e}")
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
                    'description': 'Enhanced LB3 GenieClip Ceiling solution with improved sound isolation'
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

def load_lb3genieclipceiling_solutions():
    """Load LB3 GenieClip Ceiling solutions (Standard and SP15) from MongoDB and cache them."""
    from solutions.database import diagnose_missing_document
    cache_manager = get_cache_manager()
    ids = SOLUTION_VARIANT_MONGO_IDS['ceilings']
    standard_id = ids['LB3GenieClipCeilingStandard']
    sp15_id = ids['LB3GenieClipCeilingSP15']
    
    # Get documents from database
    standard_doc = get_solution_by_id('ceilingsolutions', standard_id)
    sp15_doc = get_solution_by_id('ceilingsolutions', sp15_id)
    
    # Create solution objects only if documents exist
    standard = None
    sp15 = None
    
    if standard_doc:
        try:
            standard = LB3GenieClipCeilingStandard()
            standard._solution_data = standard_doc
            cache_manager.set('lb3genieclipceiling_standard', standard, 3600)
            logger.info(f"Successfully loaded LB3GenieClipCeilingStandard with {len(standard_doc.get('materials', []))} materials")
        except Exception as e:
            logger.error(f"Error creating LB3GenieClipCeilingStandard: {e}")
            standard = None
    else:
        logger.warning(f"LB3GenieClipCeilingStandard document not found with ID: {standard_id}")
    
    if sp15_doc:
        try:
            sp15 = LB3GenieClipCeilingSP15()
            sp15._solution_data = sp15_doc
            cache_manager.set('lb3genieclipceiling_sp15', sp15, 3600)
            logger.info(f"Successfully loaded LB3GenieClipCeilingSP15 with {len(sp15_doc.get('materials', []))} materials")
        except Exception as e:
            logger.error(f"Error creating LB3GenieClipCeilingSP15: {e}")
            sp15 = None
    else:
        logger.warning(f"LB3GenieClipCeilingSP15 document not found with ID: {sp15_id}")
    
    return standard, sp15