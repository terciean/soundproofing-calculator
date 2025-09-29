"""Base class for GenieClip solutions."""

from typing import Dict, List, Optional, Any
from solutions.base_solution import BaseSolution
from solutions.config import CLIP_SPACING
import math
import logging

logger = logging.getLogger(__name__)

class BaseGenieClipSolutionError(Exception):
    """Base exception for BaseGenieClipSolution errors"""
    pass

class BaseGenieClipSolutionInputError(BaseGenieClipSolutionError):
    """Exception for invalid inputs to BaseGenieClipSolution calculations"""
    pass

class BaseGenieClipSolutionCalculationError(BaseGenieClipSolutionError):
    """Exception for errors during BaseGenieClipSolution calculations"""
    pass

class BaseGenieClipSolution(BaseSolution):
    """Base class for all GenieClip-based solutions"""
    
    SKILL_LEVEL = "Professional"
    CLIP_SPACING = CLIP_SPACING['genie_clip']  # Use centralized clip spacing constant
    SURFACE_TYPE = None  # Must be set by child classes ('wall' or 'ceiling')
    IS_SP15 = False  # Flag for SP15 variant
    plasterboard_layers = 2  # Default for standard variant
    
    def calculate_clip_spacing(self, dimensions: Optional[Dict] = None) -> Dict[str, Any]:
        """Calculate clip spacing and quantities for GenieClip solutions"""
        try:
            # Validate input dimensions
            if dimensions:
                if 'width' not in dimensions:
                    raise BaseGenieClipSolutionInputError("Missing required dimension: width")
                if 'height' not in dimensions:
                    raise BaseGenieClipSolutionInputError("Missing required dimension: height")
                
                width = dimensions.get('width', self.length)
                height = dimensions.get('height', self.height)
                
                # Check for valid numerical values
                if not isinstance(width, (int, float)) or width <= 0:
                    raise BaseGenieClipSolutionInputError(f"Width must be a positive number, got: {width}")
                if not isinstance(height, (int, float)) or height <= 0:
                    raise BaseGenieClipSolutionInputError(f"Height must be a positive number, got: {height}")
            else:
                width = self.length
                height = self.height
            
            area = width * height
            
            # Calculate clips needed based on standard spacing
            clips_per_sqm = 1 / (self.CLIP_SPACING * self.CLIP_SPACING)  # Convert to m²
            clips_needed = math.ceil(area * clips_per_sqm)
            extra_clips = math.ceil(clips_needed * 0.1)  # 10% extra for corners and edges
            
            # Calculate channel quantities
            channel_spacing = 0.4  # 400mm spacing for channels
            channels_needed = math.ceil(width / channel_spacing)
            extra_channels = math.ceil(channels_needed * 0.1)  # 10% extra
            
            # Calculate material quantities
            material_quantities = self.calculate_material_quantities(area)
            
            return {
                'clip_spacing': self.CLIP_SPACING,
                'clips_needed': clips_needed,
                'extra_clips': extra_clips,
                'channels_needed': channels_needed,
                'extra_channels': extra_channels,
                'area': area,
                'plasterboard_layers': self.plasterboard_layers,
                **material_quantities
            }
        except BaseGenieClipSolutionError as e:
            logger.error(f"BaseGenieClipSolution specific error: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"Error calculating clip spacing: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise BaseGenieClipSolutionCalculationError(error_msg) from e
    
    def __init__(self, length: float = 0, height: float = 0):
        super().__init__(length, height)
        if self.IS_SP15:
            self.plasterboard_layers = 1  # SP15 variant uses 1 layer plus SP15
        self.validate_surface_type()
        
    def calculate_material_quantities(self, area: float) -> Dict[str, float]:
        """Calculate material quantities for GenieClip solutions"""
        try:
            # Calculate plasterboard quantity with 10% waste
            plasterboard_quantity = area * self.plasterboard_layers * 1.1
            
            # Calculate channel length with 10% extra
            channel_spacing = 0.4  # 400mm spacing
            channel_rows = math.ceil(self.height / channel_spacing)
            channel_length = channel_rows * self.length * 1.1  # 10% extra
            
            return {
                'plasterboard_sheets': math.ceil(plasterboard_quantity / 2.88),  # Standard 1.2m x 2.4m sheet
                'channel_length': math.ceil(channel_length),
                'acoustic_sealant': math.ceil((self.length + self.height) * 2 * 1.1)  # Perimeter x2 for both sides + 10%
            }
        except Exception as e:
            self.logger.error(f"Error calculating material quantities: {e}")
            return {}
        
    def validate_surface_type(self):
        """Validate that child classes set the surface type correctly"""
        if not self.SURFACE_TYPE or self.SURFACE_TYPE not in ['wall', 'ceiling']:
            raise BaseGenieClipSolutionError(f"Invalid surface type: {self.SURFACE_TYPE}. Must be 'wall' or 'ceiling'")

    def calculate(self, dimensions: Optional[Dict] = None, materials: Optional[List] = None) -> Dict[str, Any]:
        """Calculate solution properties with clip-specific additions"""
        try:
            # Get base calculation from parent
            base_result = super().calculate(dimensions, materials)
            if not base_result:
                return None
                
            # Calculate clip-specific properties
            clip_data = self.calculate_clip_spacing(dimensions)
            if not clip_data:
                return None
                
            # Calculate material quantities
            area = clip_data['area']
            material_quantities = self.calculate_material_quantities(area)
            
            # Calculate installation time (days)
            install_time = math.ceil(area / 20) + 1  # rough estimate: 20 sqm per day + 1 prep day
            
            # Add to result without modifying cached base calculation
            result = base_result.copy()
            result['additional_info'] = {
                **clip_data,
                **material_quantities,
                'install_time': f"{install_time} days",
                'skill_level': self.SKILL_LEVEL,
                'surface_type': self.SURFACE_TYPE,
                'plasterboard_layers': self.plasterboard_layers,
                'sp15_variant': self.IS_SP15
            }
            
            # Add SP15-specific data if applicable
            if self.IS_SP15:
                result['additional_info'].update({
                    'sp15_soundboard': True,
                    'enhanced_clips': True
                })
            
            self.logger.info(
                f"GenieClip calculation successful: "
                f"area={area:.2f}m², "
                f"clips={clip_data['clips_needed']}, "
                f"plasterboard={material_quantities.get('plasterboard_sheets', 0)} sheets, "
                f"variant={'SP15' if self.IS_SP15 else 'Standard'}"
            )
            return result
            
        except Exception as e:
            self.logger.error(f"Error in GenieClip calculation: {e}")
            return None
            
    def get_characteristics(self) -> Dict[str, Any]:
        """Get solution characteristics with enhanced logging"""
        try:
            characteristics = super().get_characteristics()
            
            # Only modify if we got valid characteristics
            if characteristics:
                # Create a copy to avoid modifying cached data
                characteristics = characteristics.copy()
                characteristics.update({
                    'variant': 'SP15' if self.IS_SP15 else 'standard',
                    'surface_type': self.SURFACE_TYPE,
                    'description': 'Enhanced GenieClip solution' if self.IS_SP15 else 'Standard GenieClip solution'
                })
            
            # Log cache and data source status
            cache_status = self.get_cache_status()
            for key, status in cache_status.items():
                self.logger.info(f"[SOLUTION DATA] {key}: {'CACHED' if status['cached'] else 'NOT CACHED'} "
                              f"(Last updated: {status['last_updated']})")
            
            if characteristics:
                self.logger.info(f"[SOLUTION DATA] {self.CODE_NAME} details: "
                              f"STC Rating: {characteristics.get('stc_rating', 'N/A')}, "
                              f"Sound Reduction: {characteristics.get('sound_reduction', 'N/A')}, "
                              f"Frequency Range: {characteristics.get('frequencyRange', 'N/A')}")
            
            return characteristics
            
        except Exception as e:
            self.logger.error(f"Error getting characteristics: {e}")
            return {}

    def calculate_acoustic_properties(self, noise_type: str, intensity: int) -> Dict[str, Any]:
        """Calculate acoustic properties with SP15 enhancements if applicable"""
        try:
            # Validate inputs
            if not noise_type:
                raise BaseGenieClipSolutionError("Noise type is required")
            
            if not isinstance(intensity, int) or intensity < 1 or intensity > 10:
                raise BaseGenieClipSolutionError(f"Intensity must be an integer between 1-10, got: {intensity}")
                
            # Get base acoustic properties
            base_properties = super().calculate_acoustic_properties(noise_type, intensity)
            
            # Add surface-specific properties
            base_properties['surface_type'] = self.SURFACE_TYPE
            base_properties[f'{self.SURFACE_TYPE}_specific_reduction'] = f'Enhanced {self.SURFACE_TYPE} isolation'
            
            # SP15 enhancements
            if self.IS_SP15:
                # Improve low frequency performance
                if 'frequency_performance' in base_properties:
                    base_properties['frequency_performance']['low'] = 'Superior'
                
                # Increase STC rating
                sp15_stc_bonus = 5  # SP15 adds approximately 5 STC points
                base_stc = base_properties.get('stc_rating', 60)
                base_properties['stc_rating'] = base_stc + sp15_stc_bonus
                base_properties['effective_reduction'] = f"{base_properties['stc_rating']}dB"
                
                # Add SP15-specific benefits
                base_properties['primary_benefit'] = 'Enhanced decoupling, mass, and damping'
                base_properties['sp15_advantage'] = 'Significant improvement in low frequency performance'
            
            logger.info(f"Retrieved {self.SURFACE_TYPE}-specific acoustic properties for {self.CODE_NAME}")
            return base_properties
            
        except BaseGenieClipSolutionError as e:
            logger.error(f"GenieClip acoustic properties error: {str(e)}")
            raise
        except Exception as e:
            error_msg = f"Error calculating acoustic properties: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise BaseGenieClipSolutionCalculationError(error_msg) from e