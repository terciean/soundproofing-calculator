from typing import List, Dict, Union
import math
import logging

class BaseCalculator:
    """Base calculator for all sound insulation solutions."""
    
    # Materials that always need 10% extra
    WASTAGE_MATERIALS = [
        "12.5mm Sound Plasterboard",
        "SP15 Soundboard",
        "Rockwool RWA45 50mm",
        "Rockwool RW3 100mm",
        "Tecsound 50",
        "M20 Rubber wall panel"
    ]

    # Materials that need special handling
    SPECIAL_MATERIALS = {
        "Genie Clip": {"spacing": 0.25},  # m² per clip
        "LB3 Genie Clip": {"spacing": 0.25},  # m² per clip
        "Furring Channel": {"spacing": 0.50},  # m spacing
        "Resilient bar": {"spacing": 0.40},  # 400mm spacing
        "Acoustic Sealant": {"perimeter_based": True},
        "Acoustic Mastic": {"perimeter_based": True},
        "Screws": {"min_quantity": 1}  # Minimum 1 box
    }

    def __init__(self, length: float, height: float):
        """Initialize calculator with dimensions."""
        self.length = float(length)
        self.height = float(height)
        self.area = self.length * self.height
        self.extra_multiplier = 1.10
        self.logger = logging.getLogger(self.__class__.__name__)

    def calculate_perimeter(self) -> float:
        """Calculate perimeter of the surface."""
        return 2 * (self.length + self.height)

    def needs_wastage(self, material_name: str) -> bool:
        """Check if material needs 10% wastage."""
        return material_name in self.WASTAGE_MATERIALS

    def calculate_material_quantity(self, material: Dict[str, Union[str, float]]) -> Dict:
        """Calculate quantity needed for a single material."""
        name = material.get('name', '')
        coverage = float(str(material.get('coverage', '0')).strip())
        cost = float(material.get('cost', 0))
        
        self.logger.debug(f"Calculating for {name} (Coverage: {coverage}m², Cost: £{cost})")

        quantity = 0
        area_needed = self.area

        # Handle special materials
        if name in self.SPECIAL_MATERIALS:
            special_rules = self.SPECIAL_MATERIALS[name]
            
            if "perimeter_based" in special_rules:
                perimeter = self.calculate_perimeter()
                quantity = math.ceil(perimeter / coverage)
                self.logger.debug(f"Perimeter based calculation: {perimeter}m ÷ {coverage} = {quantity}")
            
            elif "spacing" in special_rules:
                spacing = special_rules["spacing"]
                quantity = math.ceil(self.area / spacing)
                self.logger.debug(f"Spacing based calculation: {self.area}m² ÷ {spacing} = {quantity}")
            
            elif "min_quantity" in special_rules:
                quantity = special_rules["min_quantity"]
                self.logger.debug(f"Minimum quantity applied: {quantity}")

        # Standard area-based calculation
        else:
            if self.needs_wastage(name):
                area_needed *= self.extra_multiplier
                self.logger.debug(f"Adding 10% wastage. Area needed: {area_needed}m²")
            
            quantity = math.ceil(area_needed / coverage)

        total_cost = quantity * cost
        
        return {
            'name': name,
            'quantity': quantity,
            'unit_cost': cost,
            'total_cost': total_cost,
            'coverage': coverage
        }

    def calculate(self, materials: List[Dict]) -> List[Dict]:
        """Calculate quantities for all materials."""
        try:
            results = []
            self.logger.info(f"Starting calculation for {self.__class__.__name__}")
            self.logger.info(f"Dimensions: Length={self.length}m, Height={self.height}m, Area={self.area}m²")

            for material in materials:
                result = self.calculate_material_quantity(material)
                results.append(result)

            return results

        except Exception as e:
            self.logger.error(f"Error in calculation: {str(e)}")
            return None