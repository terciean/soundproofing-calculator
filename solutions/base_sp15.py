"""Base SP15 solution implementation.

This module provides a base class for SP15 variant solutions, consolidating common
SP15-specific functionality and characteristics. This reduces code duplication and
standardizes SP15 features across different solution types.

Key Features:
- Single layer plasterboard configuration
- SP15 soundboard integration
- Enhanced STC rating (65)
- Standardized SP15 characteristics
"""

import logging
from typing import Dict, List, Optional, Any
from solutions.base_solution import BaseSolution

logger = logging.getLogger(__name__)

class BaseSP15Solution(BaseSolution):
    """Base class for SP15 variant solutions.
    
    This class provides common SP15 functionality that can be inherited by specific
    SP15 solution implementations. It standardizes the SP15 features and reduces
    code duplication across different solution types.
    
    Features:
    - Single layer plasterboard configuration
    - SP15 soundboard integration
    - Enhanced STC rating
    - Standardized SP15 characteristics
    """
    
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
                
            # Add SP15 specific info
            result['additional_info'].update({
                'sp15_soundboard': True,
                'plasterboard_layers': self.plasterboard_layers
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating SP15 solution: {e}")
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
                    'description': 'Enhanced solution with improved sound isolation'
                })
                
            return characteristics
            
        except Exception as e:
            logger.error(f"Error getting SP15 characteristics: {e}")
            return {}