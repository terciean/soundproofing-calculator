"""
Resilient bar ceiling solution implementation.
"""

import logging
import math
from typing import Dict, Optional
from solutions.base_calculator import BaseCalculator
from solutions.base_solution import BaseSolution
from solutions.material_properties import get_material_properties
from solutions.config import SOLUTION_VARIANT_MONGO_IDS
from solutions.database import get_solution_by_id
from solutions.cache_manager import get_cache_manager

logger = logging.getLogger(__name__)

def get_solutions_manager():
    """Lazy import to avoid circular dependency"""
    from solutions.solutions import get_solutions_manager as get_global_solutions_manager
    return get_global_solutions_manager()

class ResilientBarCeilingStandard(BaseSolution):
    """Standard resilient bar ceiling solution"""
    
    CODE_NAME = "resilient_bar_ceiling_standard"
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
        self.solutions_manager = None
        
    def _get_solutions_manager(self):
        if self.solutions_manager is None:
            self.solutions_manager = get_solutions_manager()
        return self.solutions_manager

    def calculate(self, dimensions: Dict[str, float], materials: Optional[Dict] = None) -> Dict:
        try:
            if not materials:
                materials = get_material_properties()
                
            # Get solutions manager if needed
            solutions_manager = self._get_solutions_manager()
            
            # Rest of the calculation logic...
            return {
                'surface_type': 'ceiling',
                'area': dimensions.get('length', 0) * dimensions.get('width', 0),
                'materials': materials,
                'solution': self.CODE_NAME
            }
        except Exception as e:
            logger.error(f"Error calculating ResilientBarCeilingStandard: {e}")
            return None

    def get_characteristics(self) -> Dict:
        return {
            'name': 'Resilient Bar Ceiling (Standard)',
            'description': 'Standard resilient bar ceiling system',
            'stc_rating': 45
        }

class ResilientBarCeilingSP15(ResilientBarCeilingStandard):
    """Resilient bar ceiling solution with SP15 soundboard"""
    
    CODE_NAME = "resilient_bar_ceiling_sp15"
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)

    def get_characteristics(self) -> Dict:
        return {
            'name': 'Resilient Bar Ceiling (SP15)',
            'description': 'Enhanced resilient bar ceiling system with improved sound isolation',
            'stc_rating': 65
        }

def load_resilientbarceiling_solutions():
    """Load Resilient Bar Ceiling solutions (Standard and SP15) from MongoDB and cache them."""
    from solutions.database import diagnose_missing_document
    cache_manager = get_cache_manager()
    ids = SOLUTION_VARIANT_MONGO_IDS['ceilings']
    standard_id = ids['ResilientBarCeilingStandard']
    sp15_id = ids['ResilientBarCeilingSP15']
    
    # Get documents from database
    standard_doc = get_solution_by_id('ceilingsolutions', standard_id)
    sp15_doc = get_solution_by_id('ceilingsolutions', sp15_id)
    
    # Create solution objects only if documents exist
    standard = None
    sp15 = None
    
    if standard_doc:
        try:
            standard = ResilientBarCeilingStandard(0, 0)
            standard._solution_data = standard_doc
            cache_manager.set('resilientbarceiling_standard', standard, 3600)
            logger.info(f"Successfully loaded ResilientBarCeilingStandard with {len(standard_doc.get('materials', []))} materials")
        except Exception as e:
            logger.error(f"Error creating ResilientBarCeilingStandard: {e}")
            standard = None
    else:
        logger.warning(f"ResilientBarCeilingStandard document not found with ID: {standard_id}")
    
    if sp15_doc:
        try:
            sp15 = ResilientBarCeilingSP15(0, 0)
            sp15._solution_data = sp15_doc
            cache_manager.set('resilientbarceiling_sp15', sp15, 3600)
            logger.info(f"Successfully loaded ResilientBarCeilingSP15 with {len(sp15_doc.get('materials', []))} materials")
        except Exception as e:
            logger.error(f"Error creating ResilientBarCeilingSP15: {e}")
            sp15 = None
    else:
        logger.warning(f"ResilientBarCeilingSP15 document not found with ID: {sp15_id}")
    
    return standard, sp15