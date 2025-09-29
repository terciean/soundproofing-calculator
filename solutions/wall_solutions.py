from typing import Optional
from .base import BaseCalculator
from .solutions import SoundproofingSolutions
from .logger import logger
import math

class WallCalculator(BaseCalculator):
    """Base class for all wall calculators"""
    
    def __init__(self, length: float, height: float):
        super().__init__(length, height)
        self.solutions_manager = SoundproofingSolutions(materials=[])
        self.characteristics = None
        self.area = length * height
        self.initialize()
    
    def initialize(self):
        """Initialize calculator with solution characteristics"""
        try:
            self.characteristics = self.solutions_manager.get_solution_characteristics(self.CODE_NAME)
            if not self.characteristics:
                raise ValueError(f"No characteristics found for {self.CODE_NAME}")
            logger.info(f"Initialized {self.CODE_NAME} calculator with characteristics")
        except Exception as e:
            logger.error(f"Error initializing {self.CODE_NAME}: {str(e)}")
            raise
    
    def calculate(self, materials):
        """Standard calculation method for all wall solutions"""
        try:
            logger.info(f"Starting {self.CODE_NAME} calculation")
            logger.info(f"Wall Dimensions: Length={self.length}m, Height={self.height}m, Area={self.area}m²")
            
            if not self.characteristics:
                raise ValueError(f"No characteristics found for {self.CODE_NAME}")
            
            results = []
            total_material_cost = 0
            
            # Calculate quantities for each material
            for material in materials:
                quantity = math.ceil(self.area * material.get('rate', 1))
                cost = quantity * material.get('unit_cost', 0)
                total_material_cost += cost
                
                results.append({
                    'name': material.get('name', 'Unknown'),
                    'quantity': quantity,
                    'unit': material.get('unit', 'units'),
                    'cost': cost
                })
            
            # Calculate labor cost based on solution type
            labor_rate = self.get_labor_rate()
            labor_cost = total_material_cost * labor_rate
            
            result = {
                'area': self.area,
                'materials': results,
                'material_cost': total_material_cost,
                'labor_cost': labor_cost,
                'total_cost': total_material_cost + labor_cost,
                'characteristics': self.characteristics
            }
            
            logger.info(f"Completed {self.CODE_NAME} calculation: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in {self.CODE_NAME} calculation: {str(e)}")
            return None
    
    def get_labor_rate(self):
        """Get labor rate multiplier based on solution type"""
        labor_rates = {
            'M20WallStandard': 0.4,
            'M20WallSP15': 0.4,
            'GenieClipWallStandard': 0.45,
            'GenieClipWallSP15': 0.45,
            'ResilientBarWallStandard': 0.5,
            'ResilientBarWallSP15': 0.5,
            'IndependentWallStandard': 0.6,
            'IndependentWallSP15': 0.6
        }
        return labor_rates.get(self.CODE_NAME, 0.5)

class M20WallSP15(WallCalculator):
    CODE_NAME = "M20WallSP15"
    FRONTEND_NAME = "M20 SP15 Wall System"
    
    def calculate(self, materials):
        """M20 SP15 specific calculation"""
        base_result = super().calculate(materials)
        if not base_result:
            return None
            
        # Add SP15 specific calculations if needed
        return base_result

class ResilientBarWall(WallCalculator):
    CODE_NAME = "ResilientBarWallStandard"
    FRONTEND_NAME = "Resilient Bar Wall System"
    
    def calculate(self, materials):
        """Resilient Bar specific calculation"""
        base_result = super().calculate(materials)
        if not base_result:
            return None
            
        # Add any Resilient Bar specific calculations
        return base_result

class GenieClipWall(WallCalculator):
    CODE_NAME = "GenieClipWallStandard"
    FRONTEND_NAME = "Genie Clip Wall System"
    
    def calculate(self, materials):
        """Genie Clip specific calculation"""
        base_result = super().calculate(materials)
        if not base_result:
            return None
            
        # Add clip spacing calculations
        from solutions.config import CLIP_SPACING
        clip_spacing = CLIP_SPACING['genie_clip']  # Use centralized clip spacing constant
        extra_clips = math.ceil((self.length + self.height) / clip_spacing * 0.1)  # 10% extra for corners
        
        base_result['additional_info'] = {
            'clip_spacing': clip_spacing,
            'extra_clips': extra_clips
        }
        
        return base_result

class IndependentWall(WallCalculator):
    CODE_NAME = "IndependentWallStandard"
    FRONTEND_NAME = "Independent Wall System"
    
    def calculate(self, materials):
        """Independent Wall specific calculation"""
        base_result = super().calculate(materials)
        if not base_result:
            return None
        
        # Add framing and insulation calculations
        frame_cost = self.area * 15
        insulation_cost = self.area * 8
        
        base_result['material_cost'] += frame_cost + insulation_cost
        base_result['total_cost'] += frame_cost + insulation_cost
        base_result['additional_materials'] = {
            'framing': {'area': self.area, 'cost': frame_cost},
            'insulation': {'area': self.area, 'cost': insulation_cost}
        }
        
        return base_result

class IndependentWallSP15(IndependentWall):
    """Calculator for Independent Wall SP15 solutions"""
    CODE_NAME = "IndependentWallSP15"
    FRONTEND_NAME = "Independent Wall SP15 System"
    
    def calculate(self, materials):
        """Calculate quantities for Independent Wall SP15 solution"""
        try:
            base_result = super().calculate(materials)
            if not base_result:
                return None
                
            # Add SP15 specific costs
            sp15_cost = base_result['area'] * 25  # Additional £25/m² for SP15
            
            result = {
                **base_result,
                'material_cost': base_result['material_cost'] + sp15_cost,
                'total_cost': base_result['total_cost'] + sp15_cost,
                'additional_materials': {
                    **base_result['additional_materials'],
                    'sp15_board': {
                        'area': base_result['area'],
                        'cost': sp15_cost
                    }
                }
            }
            
            logger.info(f"Completed {self.FRONTEND_NAME} calculation with SP15: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in {self.FRONTEND_NAME} calculation: {str(e)}")
            return None

# After MongoDB connection is established
if db_connection_successful:
    initialize_cache()