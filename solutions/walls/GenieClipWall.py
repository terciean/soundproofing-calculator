"""GenieClip wall solution implementation."""
from solutions.base_sp15 import BaseSP15Solution
import logging
from solutions.base_calculator import BaseCalculator
from solutions.base_genieclip import BaseGenieClipSolution, BaseGenieClipSolutionError, BaseGenieClipSolutionInputError, BaseGenieClipSolutionCalculationError
from solutions.material_properties import get_material_properties
from solutions.solutions import get_solutions_manager
from typing import Dict, List, Optional, Any
import math
from solutions.config import SOLUTION_VARIANT_MONGO_IDS
from solutions.database import get_solution_by_id, get_db
from solutions.cache_manager import get_cache_manager

logger = logging.getLogger(__name__)

class GenieClipWallStandard(BaseGenieClipSolution):
    """Standard GenieClip wall solution"""
    
    CODE_NAME = "Genie Clip wall (Standard)"
    SURFACE_TYPE = "wall"
    IS_SP15 = False
        
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
    
    def calculate_acoustic_properties(self, noise_type: str, intensity: int) -> Dict[str, Any]:
        """Calculate acoustic properties specific to GenieClip walls"""
        try:
            # Get base acoustic properties
            result = super().calculate_acoustic_properties(noise_type, intensity)
            
            # Add wall-specific acoustic properties
            result['surface_type'] = self.SURFACE_TYPE
            result['wall_specific_reduction'] = 'Enhanced wall isolation'
            
            logger.info(f"Retrieved wall-specific acoustic properties for {self.CODE_NAME}")
            return result
            
        except BaseGenieClipSolutionError as e:
            logger.error(f"GenieClipWall acoustic properties error: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"Error calculating wall acoustic properties: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise BaseGenieClipSolutionCalculationError(error_msg) from e
    
    def generate_implementation_details(self, dimensions: Dict[str, float], noise_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation details specific to GenieClip walls"""
        try:
            # Get base implementation details
            result = super().generate_implementation_details(dimensions, noise_data)
            
            # Add wall-specific installation steps
            wall_steps = [
                "Ensure wall surface is clean and structurally sound",
                "Mark stud locations for secure mounting",
                "Install clips perpendicular to intended channel direction",
                "Leave expansion gap at wall perimeter"
            ]
            
            if 'installation_steps' in result:
                result['installation_steps'].extend(wall_steps)
            else:
                result['installation_steps'] = wall_steps
            
            # Add wall-specific considerations
            wall_considerations = [
                "Check wall load-bearing capacity",
                "Plan for electrical outlet extensions",
                "Consider door and window treatments"
            ]
            
            if 'special_considerations' in result:
                result['special_considerations'].extend(wall_considerations)
            else:
                result['special_considerations'] = wall_considerations
            
            result['surface_type'] = self.SURFACE_TYPE
            
            logger.info(f"Generated wall-specific implementation details for {self.CODE_NAME}")
            return result
            
        except BaseGenieClipSolutionError as e:
            logger.error(f"GenieClipWall implementation details error: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"Error generating wall implementation details: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise BaseGenieClipSolutionCalculationError(error_msg) from e
            logger.error(error_msg, exc_info=True)
            
            # Return minimal info instead of raising exception
            return {
                'install_time': "3-5 days",
                'skill_level': self.SKILL_LEVEL,
                'error': str(e)  # Include error message in result
            }

    def get_characteristics(self) -> Dict[str, Any]:
        """Get solution characteristics with caching"""
        try:
            # Get base characteristics from cache or calculation
            characteristics = super().get_characteristics()
            
            # Only modify if we got valid characteristics
            if characteristics:
                # Create a copy to avoid modifying cached data
                characteristics = characteristics.copy()
                characteristics.update({
                    'variant': 'standard' if isinstance(self, GenieClipWallStandard) else 'sp15',
                    'surface_type': self.SURFACE_TYPE
                })
            
            return characteristics
            
        except Exception as e:
            logger.error(f"Error getting characteristics: {e}")
            return {}

            

class GenieClipWallSP15(BaseSP15Solution, GenieClipWallStandard):
    """SP15 variant of GenieClip Wall solution"""
    
    CODE_NAME = "Genie Clip wall (SP15 Soundboard Upgrade)"
    
    def __init__(self, length: float = 0, height: float = 0):
        BaseSP15Solution.__init__(self, length, height)
        GenieClipWallStandard.__init__(self, length, height)
        
    def get_characteristics(self) -> dict:
        """Get SP15 variant characteristics"""
        try:
            # Get base characteristics from cache or calculation
            characteristics = super().get_characteristics()
            return characteristics
            
        except Exception as e:
            error_msg = f"Error getting SP15 characteristics: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {}
    
    def calculate_acoustic_properties(self, noise_type: str, intensity: int) -> Dict[str, Any]:
        """Calculate acoustic properties specific to SP15 GenieClip walls"""
        try:
            # Get base acoustic properties with SP15 enhancements
            base_properties = super().calculate_acoustic_properties(noise_type, intensity)
            return base_properties
            
        except BaseGenieClipSolutionError as e:
            logger.error(f"SP15 GenieClipWall acoustic calculation error: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"Error calculating SP15 acoustic properties: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise BaseGenieClipSolutionError(error_msg)
    
    def generate_implementation_details(self, dimensions: Dict[str, float], noise_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation details specific to SP15 GenieClip walls"""
        try:
            # Validate same inputs as parent
            if not dimensions:
                raise GenieClipWallInputError("Dimensions are required")
            
            if 'width' not in dimensions or 'height' not in dimensions:
                raise GenieClipWallInputError("Width and height dimensions are required")
                
            # Get base implementation details
            base_details = super().generate_implementation_details(dimensions, noise_data)
            
            if 'error' in base_details:
                logger.warning(f"Using base details with errors: {base_details.get('error')}")
            
            # Calculate area
            length = dimensions.get('width', self.length)
            height = dimensions.get('height', self.height)
            area = length * height
            
            # Calculate SP15 sheets (same size as drywall)
            sheets_per_sqm = 0.35  # Roughly 1 sheet per 2.9 sqm
            sp15_sheets_needed = math.ceil(area * sheets_per_sqm)
            
            # Add SP15 to materials list
            if 'materials' in base_details and isinstance(base_details['materials'], list):
                base_details['materials'].insert(2, f"{sp15_sheets_needed} sheets of SP15 Soundboard")
                logger.debug(f"Added {sp15_sheets_needed} SP15 sheets to materials list")
            else:
                logger.warning("Could not add SP15 sheets - materials list not found or invalid")
                base_details['materials'] = [f"{sp15_sheets_needed} sheets of SP15 Soundboard"]
            
            # Update installation steps
            if 'installation_steps' in base_details and isinstance(base_details['installation_steps'], list):
                new_steps = base_details['installation_steps'].copy()
                new_steps.insert(4, "Install SP15 Soundboard layer before drywall")
                base_details['installation_steps'] = new_steps
                logger.debug("Added SP15 installation step")
            else:
                logger.warning("Could not update installation steps - steps list not found or invalid")
            
            # Increase installation time for SP15
            if 'install_time' in base_details and isinstance(base_details['install_time'], str):
                try:
                    install_days = int(base_details['install_time'].split()[0])
                    base_details['install_time'] = f"{install_days + 1} days"  # Additional day for SP15
                    logger.debug(f"Updated install time to {base_details['install_time']}")
                except (ValueError, IndexError) as e:
                    logger.warning(f"Could not parse install time '{base_details['install_time']}': {str(e)}")
                    base_details['install_time'] = f"{math.ceil(area / 15)} days"  # SP15 is slower, 15 sqm per day
            
            # Add SP15 special considerations
            if 'special_considerations' in base_details and isinstance(base_details['special_considerations'], list):
                base_details['special_considerations'].append("Ensure SP15 boards are tightly butted together")
                base_details['special_considerations'].append("Handle SP15 boards with care as they are heavier than standard drywall")
                logger.debug("Added SP15 special considerations")
            else:
                logger.warning("Could not add special considerations - list not found or invalid")
            
            logger.info(f"SP15 GenieClipWall implementation details generated successfully for area={area:.2f}m²")
            return base_details
            
        except GenieClipWallError as e:
            # Log specific GenieClipWall errors
            logger.error(f"SP15 GenieClipWall implementation details error: {str(e)}")
            raise
        except Exception as e:
            # Log error and return minimal info
            error_msg = f"Error generating SP15 implementation details: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            # Return minimal info without fallback
            return {
                'install_time': "4-6 days",  # Slightly longer for SP15
                'skill_level': self.SKILL_LEVEL,
                'requires_sp15': True,
                'error': str(e)  # Include error message in result
                }

def load_genieclipwall_solutions():
    """Load GenieClip Wall solutions (Standard and SP15) from MongoDB and cache them."""
    cache_manager = get_cache_manager()
    ids = SOLUTION_VARIANT_MONGO_IDS['walls']
    standard_id = ids['GenieClipWallStandard']
    sp15_id = ids['GenieClipWallSP15']
    standard_doc = get_solution_by_id('wallsolutions', standard_id)
    sp15_doc = get_solution_by_id('wallsolutions', sp15_id)
    if not standard_doc:
        raise ValueError(f"No data found for GenieClipWallStandard with id {standard_id}")
    if not sp15_doc:
        raise ValueError(f"No data found for GenieClipWallSP15 with id {sp15_id}")
    standard = GenieClipWallStandard()
    sp15 = GenieClipWallSP15()
    standard._solution_data = standard_doc
    sp15._solution_data = sp15_doc
    cache_manager.set('genieclipwall_standard', standard, 3600)
    cache_manager.set('genieclipwall_sp15', sp15, 3600)
    return standard, sp15