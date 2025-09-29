from typing import Dict, List, Any, Optional
import math
import os
import sys
import logging

# Add parent directory to path to allow importing from solutions module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solutions.base_calculator import BaseCalculator
from solutions.solution import BaseSolution

class BaseFloorCalculator(BaseCalculator):
    """Base calculator for floor solutions"""
    
    def __init__(self, solution_id, **kwargs):
        """
        Initialize the floor calculator
        
        Args:
            solution_id: Solution identifier
            length: Floor length in meters (optional)
            width: Floor width in meters (optional)
        """
        self.solution_id = solution_id
        length = kwargs.get('length', 1)
        width = kwargs.get('width', 1)
        # Pass length and width to BaseCalculator as length and height
        super().__init__(length, width)
        self.logger = logging.getLogger(__name__)
        
    def calculate_area(self, dimensions=None):
        """
        Calculate floor area based on dimensions
        
        Args:
            dimensions: Dictionary with length and width in meters
            
        Returns:
            float: Floor area in square meters
        """
        if dimensions:
            length = float(dimensions.get('length', self.length))
            width = float(dimensions.get('width', self.height))
            return length * width
        return self.area
    
    def calculate_costs(self, dimensions=None, blockages=None):
        """
        Calculate costs for the floor solution
        
        Args:
            dimensions: Dictionary with length and width in meters (optional)
            blockages: Dictionary of blockages (optional)
            
        Returns:
            Dict: Cost breakdown
        """
        try:
            # Calculate area
            area = self.calculate_area(dimensions)
            
            # Apply blockage reductions if present
            if blockages and isinstance(blockages, dict):
                for blockage_type, blockage_details in blockages.items():
                    if blockage_type == 'floor':
                        for blockage in blockage_details:
                            if 'area' in blockage:
                                area -= float(blockage['area'])
            
            # Ensure area is not negative
            area = max(0.1, area)
            
            # Calculate costs using BaseCalculator logic
            return super().calculate_costs(area)
            
        except Exception as e:
            self.logger.error(f"Error calculating floor costs: {str(e)}")
            return None


class FloatingFloorStandard(BaseSolution):
    """Standard floating floor solution."""
    
    CODE_NAME = "FloatingFloorStandard"
    
    def __init__(self, width: float, length: float):
        super().__init__(width, length)
        self.name = "Floating Floor"
        self.description = "A standard floating floor solution"
        
    def calculate(self, room_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate implementation details based on room data."""
        return {
            "name": self.name,
            "description": self.description,
            "footage": self.width * self.length,
            "stc_rating": 50,
            "iic_rating": 45,
            "materials": []
        }


class IsolationMatFloor(BaseSolution):
    """Isolation mat floor solution."""
    
    CODE_NAME = "IsolationMatFloor"
    
    def __init__(self, width: float, length: float):
        super().__init__(width, length)
        self.name = "Isolation Mat Floor"
        self.description = "A premium floor solution with isolation mat"
        
    def calculate(self, room_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate implementation details based on room data."""
        return {
            "name": self.name,
            "description": self.description,
            "footage": self.width * self.length,
            "stc_rating": 58,
            "iic_rating": 52,
            "materials": []
        }


class FloatingFloorStandard(BaseFloorCalculator):
    """Standard floating floor solution calculator"""
    
    def __init__(self, **kwargs):
        super().__init__('FloatingFloorStandard', **kwargs)
    
    def get_characteristics(self):
        """Get solution characteristics"""
        return {
            "type": "floor",
            "displayName": "Floating Floor System",
            "description": "Standard floating floor system with acoustic underlay",
            "sound_reduction": 35,
            "stc_rating": 45,
            "frequencyRange": "80Hz-3500Hz",
            "suitable_noise_types": ["footsteps", "impact"],
            "materials": [
                {
                    "name": "Acoustic Underlay",
                    "baseCost": 15.0,
                    "unitsPerM2": 1.1,  # 10% extra for overlap
                    "unit": "m²"
                },
                {
                    "name": "Plywood Sheet",
                    "baseCost": 25.0,
                    "unitsPerM2": 0.34,  # 1 sheet covers about 3m²
                    "unit": "sheet"
                },
                {
                    "name": "Acoustic Sealant",
                    "baseCost": 8.0,
                    "unitsPerM2": 0.2,  # Based on perimeter
                    "unit": "tube"
                },
                {
                    "name": "Screws",
                    "baseCost": 12.0,
                    "unitsPerM2": 0.04,  # 1 box per 25m²
                    "unit": "box"
                }
            ]
        }


class IsolationMatFloor(BaseFloorCalculator):
    """Premium isolation mat floor solution calculator"""
    
    def __init__(self, **kwargs):
        super().__init__('IsolationMatFloor', **kwargs)
    
    def get_characteristics(self):
        """Get solution characteristics"""
        return {
            "type": "floor",
            "displayName": "Isolation Mat System",
            "description": "Premium floor isolation system with high-performance mat",
            "sound_reduction": 45,
            "stc_rating": 55,
            "frequencyRange": "60Hz-4000Hz",
            "suitable_noise_types": ["footsteps", "impact", "machinery"],
            "materials": [
                {
                    "name": "High-Density Isolation Mat",
                    "baseCost": 35.0,
                    "unitsPerM2": 1.1,  # 10% extra for overlap
                    "unit": "m²"
                },
                {
                    "name": "Engineered Floor Joists",
                    "baseCost": 30.0,
                    "unitsPerM2": 0.4,  # 1 joist per 2.5m²
                    "unit": "joist"
                },
                {
                    "name": "Sound-Rated Plywood",
                    "baseCost": 35.0,
                    "unitsPerM2": 0.34,  # 1 sheet covers about 3m²
                    "unit": "sheet"
                },
                {
                    "name": "Acoustic Decoupler",
                    "baseCost": 15.0,
                    "unitsPerM2": 0.2,  # Based on perimeter
                    "unit": "meter"
                },
                {
                    "name": "Isolation Fasteners",
                    "baseCost": 18.0,
                    "unitsPerM2": 0.08,  # 1 box per 12.5m²
                    "unit": "box"
                }
            ]
        } 