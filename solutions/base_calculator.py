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

    # Materials that need special handling for spacing/coverage
    SPECIAL_MATERIALS = {
        "Genie Clip": {"spacing": 0.25},  # Each clip covers 0.25m²
        "LB3 Genie Clip": {"spacing": 0.25},  # Each clip covers 0.25m²
        "Furring Channel": {"spacing": 0.50},  # Each channel covers area based on spacing
        "Resilient bar": {"spacing": 0.40},  # Each bar covers area based on spacing
        "Acoustic Sealant": {"perimeter_based": True},
        "Acoustic Mastic": {"perimeter_based": True},
        "Screws": {"min_quantity": 1}  # Minimum 1 box
    }

    # Default coverage per unit in m² if not specified in solution data
    MATERIAL_COVERAGE = {
        "12.5mm Sound Plasterboard": 2.88,  # Each board covers 2.88m²
        "SP15 Soundboard": 2.88,  # Each board covers 2.88m²
        "Rockwool RWA45 50mm": 8.64,  # Each pack covers 8.64m²
        "Rockwool RW3 100mm": 5.76,  # Each pack covers 5.76m²
        "Genie Clip": 0.25,  # Each clip covers 0.25m²
        "LB3 Genie Clip": 0.25,  # Each clip covers 0.25m²
        "Screws": 30.0,  # One box covers 30m²
        "Floor protection": 30.0  # One unit covers 30m²
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

    def parse_coverage(self, coverage_str: str) -> float:
        """Parse coverage value from string, handling both numeric and string formats."""
        try:
            # Strip any whitespace
            coverage_str = str(coverage_str).strip()
            # Convert to float, handling both "2.88" and "2 " formats
            return float(coverage_str)
        except ValueError:
            # If conversion fails, check material coverage overrides
            self.logger.warning(f"Could not parse coverage value: {coverage_str}, using default")
            return 1.0

    def calculate_material_quantity(self, material: Dict[str, Union[str, float]]) -> Dict:
        """Calculate quantity needed for a single material."""
        name = material.get('name', '')
        cost = float(material.get('cost', 0))
        
        # Get coverage from material or use override
        raw_coverage = material.get('coverage', '1')
        coverage = self.parse_coverage(raw_coverage)  # Coverage per unit in m²
        
        # Use default coverage if not specified in solution data
        if coverage <= 0 and name in self.MATERIAL_COVERAGE:
            coverage = self.MATERIAL_COVERAGE[name]
        
        self.logger.debug(f"Calculating for {name} (Coverage per unit: {coverage}m², Cost: £{cost})")

        quantity = 0
        area_needed = self.area
        units_needed = 0

        # Handle special materials
        if name in self.SPECIAL_MATERIALS:
            special_rules = self.SPECIAL_MATERIALS[name]
            
            if "perimeter_based" in special_rules:
                # Convert perimeter to area (1m wide strip)
                perimeter_area = self.calculate_perimeter()
                units_needed = math.ceil(perimeter_area / coverage)
                self.logger.debug(f"Perimeter based calculation: {perimeter_area}m² ÷ {coverage}m² per unit = {units_needed} units")
            
            elif "spacing" in special_rules:
                # For all spacing-based materials, use the coverage directly
                units_needed = math.ceil(self.area / coverage)
                self.logger.debug(f"Area based calculation: {self.area}m² ÷ {coverage}m² per unit = {units_needed} units")
            
            elif "min_quantity" in special_rules:
                units_needed = special_rules["min_quantity"]
                self.logger.debug(f"Minimum quantity applied: {units_needed} units")

        # Standard area-based calculation
        else:
            if self.needs_wastage(name):
                area_needed *= self.extra_multiplier
                self.logger.debug(f"Adding 10% wastage. Area needed: {area_needed}m²")
            
            units_needed = math.ceil(area_needed / coverage)
            self.logger.debug(f"Basic units needed: {area_needed}m² ÷ {coverage}m² per unit = {units_needed} units")

        # Set final quantity
        quantity = units_needed

        # Special case for plasterboard when 2 layers are needed
        if name == "12.5mm Sound Plasterboard" and hasattr(self, 'plasterboard_layers'):
            quantity *= self.plasterboard_layers
            self.logger.debug(f"Adjusting for {self.plasterboard_layers} layers of plasterboard: {quantity} units")

        total_cost = quantity * cost
        actual_coverage = quantity * coverage
        
        return {
            'name': name,
            'quantity': quantity,
            'coverage_per_unit': coverage,
            'total_coverage': actual_coverage,
            'unit_cost': cost,
            'total_cost': total_cost
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