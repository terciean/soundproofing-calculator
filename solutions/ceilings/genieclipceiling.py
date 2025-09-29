"""
Genie clip ceiling solution implementation.
"""

import logging
from solutions.base_calculator import BaseCalculator
from solutions.base_genieclip import BaseGenieClipSolution, BaseGenieClipSolutionError
from solutions.material_properties import get_material_properties
from solutions.solutions import get_solutions_manager
from typing import Dict, List, Optional, Any
import math
from solutions.config import SOLUTION_VARIANT_MONGO_IDS
from solutions.database import get_solution_by_id, get_db
from solutions.cache_manager import get_cache_manager
from solutions.base_sp15 import BaseSP15Solution

logger = logging.getLogger(__name__)

class GenieClipCeilingStandard(BaseGenieClipSolution):
    """Standard Genie Clip ceiling solution"""
    
    CODE_NAME = "Genie Clip ceiling (Standard)"
    SURFACE_TYPE = "ceiling"
    IS_SP15 = False
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
            
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
                    'variant': 'standard' if isinstance(self, GenieClipCeilingStandard) else 'sp15',
                    'surface_type': self.SURFACE_TYPE
                })
            
            return characteristics
            
        except Exception as e:
            logger.error(f"Error getting characteristics: {e}")
            return {}

    def calculate_acoustic_properties(self, noise_type: str, intensity: int) -> Dict[str, Any]:
        """Calculate acoustic properties specific to GenieClip ceilings"""
        try:
            # Get base acoustic properties
            result = super().calculate_acoustic_properties(noise_type, intensity)
            
            # Add ceiling-specific acoustic properties
            result['surface_type'] = self.SURFACE_TYPE
            result['ceiling_specific_reduction'] = 'Enhanced ceiling isolation'
            
            logger.info(f"Retrieved ceiling-specific acoustic properties for {self.CODE_NAME}")
            return result
            
        except BaseGenieClipSolutionError as e:
            logger.error(f"GenieClipCeiling acoustic properties error: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"Error calculating ceiling acoustic properties: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise BaseGenieClipSolutionCalculationError(error_msg) from e
    
    def generate_implementation_details(self, dimensions: Dict[str, float], noise_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation details specific to GenieClip ceilings"""
        try:
            # Get base implementation details
            result = super().generate_implementation_details(dimensions, noise_data)
            
            # Add ceiling-specific installation steps
            ceiling_steps = [
                "Verify ceiling joists are structurally sound",
                "Mark joist locations for secure mounting",
                "Install clips perpendicular to intended channel direction",
                "Maintain proper spacing between clips"
            ]
            
            if 'installation_steps' in result:
                result['installation_steps'].extend(ceiling_steps)
            else:
                result['installation_steps'] = ceiling_steps
            
            # Add ceiling-specific considerations
            ceiling_considerations = [
                "Check ceiling load capacity",
                "Plan for lighting fixture extensions",
                "Consider HVAC vent treatments"
            ]
            
            if 'special_considerations' in result:
                result['special_considerations'].extend(ceiling_considerations)
            else:
                result['special_considerations'] = ceiling_considerations
            
            result['surface_type'] = self.SURFACE_TYPE
            
            logger.info(f"Generated ceiling-specific implementation details for {self.CODE_NAME}")
            return result
            
        except BaseGenieClipSolutionError as e:
            logger.error(f"GenieClipCeiling implementation details error: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"Error generating ceiling implementation details: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'install_time': "3-5 days",
                'skill_level': self.SKILL_LEVEL,
                'error': str(e)
            }

class GenieClipCeilingSP15(BaseSP15Solution, GenieClipCeilingStandard):
    """SP15 variant of Genie Clip ceiling solution"""
    
    CODE_NAME = "Genie Clip ceiling (SP15 Soundboard Upgrade)"
    IS_SP15 = True
    
    def __init__(self, length: float = 0, height: float = 0):
        BaseSP15Solution.__init__(self, length, height)
        GenieClipCeilingStandard.__init__(self, length, height)
            
    def get_characteristics(self) -> Dict[str, Any]:
        """Get SP15 variant characteristics"""
        try:
            # Get base characteristics from cache or calculation
            characteristics = super().get_characteristics()
            return characteristics
            
        except Exception as e:
            logger.error(f"[SOLUTION DATA] Error getting SP15 characteristics for {self.CODE_NAME}: {e}")
            return {}
            
            # Log whether we're using database or fallback data
            if not characteristics:
                logger.warning(f"[SOLUTION DATA] {self.CODE_NAME}: NO DATA AVAILABLE - Using empty characteristics")
            elif characteristics.get('_source') == 'database':
                logger.info(f"[SOLUTION DATA] {self.CODE_NAME}: Using DATABASE data with {len(characteristics.get('materials', []))} materials")
            else:
                logger.warning(f"[SOLUTION DATA] {self.CODE_NAME}: Using FALLBACK data")
            
            # Log the solution details
            if characteristics:
                logger.info(f"[SOLUTION DATA] {self.CODE_NAME} details: "
                          f"STC Rating: {characteristics.get('stc_rating', 'N/A')}, "
                          f"Sound Reduction: {characteristics.get('sound_reduction', 'N/A')}, "
                          f"Frequency Range: {characteristics.get('frequencyRange', 'N/A')}")
            
            return characteristics
            
        except Exception as e:
            logger.error(f"[SOLUTION DATA] Error getting SP15 characteristics for {self.CODE_NAME}: {e}")
            return {}

    def calculate_acoustic_properties(self, noise_type: str, intensity: int) -> Dict[str, Any]:
        """Calculate acoustic properties specific to SP15 GenieClip ceilings"""
        try:
            # Get base acoustic properties with SP15 enhancements
            base_properties = super().calculate_acoustic_properties(noise_type, intensity)
            return base_properties
            
        except BaseGenieClipSolutionError as e:
            logger.error(f"SP15 GenieClipCeiling acoustic calculation error: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"Error calculating SP15 acoustic properties: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise BaseGenieClipSolutionError(error_msg)
    
    def generate_implementation_details(self, dimensions: Dict[str, float], noise_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation details specific to SP15 GenieClip ceilings"""
        try:
            # Validate inputs
            if not dimensions:
                raise BaseGenieClipSolutionError("Dimensions are required")
            
            if 'width' not in dimensions or 'height' not in dimensions:
                raise BaseGenieClipSolutionError("Width and height dimensions are required")
                
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
            
            logger.info(f"SP15 GenieClipCeiling implementation details generated successfully for area={area:.2f}m²")
            return base_details
            
        except BaseGenieClipSolutionError as e:
            logger.error(f"SP15 GenieClipCeiling implementation details error: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"Error generating SP15 implementation details: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            # Return minimal info without fallback
            return {
                'install_time': "4-6 days",  # Slightly longer for SP15
                'skill_level': self.SKILL_LEVEL,
                'requires_sp15': True,
                'error': str(e)
            }

def load_genieclipceiling_solutions():
    """Load GenieClip Ceiling solutions (Standard and SP15) from MongoDB and cache them."""
    from solutions.database import diagnose_missing_document
    cache_manager = get_cache_manager()
    ids = SOLUTION_VARIANT_MONGO_IDS['ceilings']
    standard_id = ids['GenieClipCeilingStandard']
    sp15_id = ids['GenieClipCeilingSP15']
    
    # Get documents from database
    standard_doc = get_solution_by_id('ceilingsolutions', standard_id)
    sp15_doc = get_solution_by_id('ceilingsolutions', sp15_id)
    
    # Create solution objects only if documents exist
    standard = None
    sp15 = None
    
    if standard_doc:
        try:
            standard = GenieClipCeilingStandard()
            standard._solution_data = standard_doc
            cache_manager.set('genieclipceiling_standard', standard, 3600)
            logger.info(f"Successfully loaded GenieClipCeilingStandard with {len(standard_doc.get('materials', []))} materials")
        except Exception as e:
            logger.error(f"Error creating GenieClipCeilingStandard: {e}")
            standard = None
    else:
        logger.warning(f"GenieClipCeilingStandard document not found with ID: {standard_id}")
    
    if sp15_doc:
        try:
            sp15 = GenieClipCeilingSP15()
            sp15._solution_data = sp15_doc
            cache_manager.set('genieclipceiling_sp15', sp15, 3600)
            logger.info(f"Successfully loaded GenieClipCeilingSP15 with {len(sp15_doc.get('materials', []))} materials")
        except Exception as e:
            logger.error(f"Error creating GenieClipCeilingSP15: {e}")
            sp15 = None
    else:
        logger.warning(f"GenieClipCeilingSP15 document not found with ID: {sp15_id}")
    
    return standard, sp15