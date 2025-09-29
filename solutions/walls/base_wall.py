"""Base wall solution implementation."""

from solutions.base_solution import BaseSolution
import logging
from typing import Dict, List, Optional, Any

class BaseWall(BaseSolution):
    """Base class for all wall solutions"""
    
    SURFACE_TYPE = "wall"
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def calculate_acoustic_properties(self, noise_type: str, intensity: int) -> Dict[str, Any]:
        """Calculate acoustic properties for wall solutions"""
        try:
            # Get base acoustic properties
            result = super().calculate_acoustic_properties(noise_type, intensity)
            
            # Add wall-specific acoustic properties
            result['surface_type'] = self.SURFACE_TYPE
            result['wall_specific_reduction'] = 'Standard wall isolation'
            
            self.logger.info(f"Retrieved wall acoustic properties for {self.CODE_NAME}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error calculating wall acoustic properties: {str(e)}")
            return {}
    
    def generate_implementation_details(self, dimensions: Dict[str, float], noise_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation details for wall solutions"""
        try:
            # Get base implementation details
            result = super().generate_implementation_details(dimensions, noise_data)
            
            # Add wall-specific installation steps
            wall_steps = [
                "Ensure wall surface is clean and structurally sound",
                "Mark stud locations for secure mounting",
                "Install according to manufacturer specifications",
                "Leave appropriate expansion gaps"
            ]
            
            if 'installation_steps' in result:
                result['installation_steps'].extend(wall_steps)
            else:
                result['installation_steps'] = wall_steps
            
            # Add wall-specific considerations
            wall_considerations = [
                "Check wall load-bearing capacity",
                "Plan for electrical and plumbing modifications",
                "Consider door and window treatments"
            ]
            
            if 'special_considerations' in result:
                result['special_considerations'].extend(wall_considerations)
            else:
                result['special_considerations'] = wall_considerations
            
            result['surface_type'] = self.SURFACE_TYPE
            
            self.logger.info(f"Generated wall implementation details for {self.CODE_NAME}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating wall implementation details: {str(e)}")
            return {}
    
    def calculate(self, dimensions: Optional[Dict] = None, materials: Optional[List] = None) -> Dict[str, Any]:
        """Standard wall calculation with validation"""
        try:
            self.logger.info(f"Calculating {self.CODE_NAME}")
            result = super().calculate(dimensions, materials)
            
            if not result:
                self.logger.error(f"No result from calculation for {self.CODE_NAME}")
                return None
                
            # Add wall-specific calculations
            result['surface_type'] = self.SURFACE_TYPE
            result['total_area'] = self.length * self.height
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error calculating {self.CODE_NAME}: {str(e)}")
            return None
    
    def get_characteristics(self) -> Dict[str, Any]:
        """Get wall solution characteristics with caching"""
        try:
            # Get base characteristics from cache or calculation
            characteristics = super().get_characteristics()
            
            # Only modify if we got valid characteristics
            if characteristics:
                # Create a copy to avoid modifying cached data
                characteristics = characteristics.copy()
                characteristics.update({
                    'surface_type': self.SURFACE_TYPE
                })
            
            return characteristics
            
        except Exception as e:
            self.logger.error(f"Error getting characteristics: {e}")
            return {}