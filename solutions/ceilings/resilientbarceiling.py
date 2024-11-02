import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_calculator import BaseCalculator
import math

class ResilientBarCeilingStandard(BaseCalculator):
    """
    Calculates materials for the Resilient Bar Ceiling solution.
    """
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 2  # Two layers by default
        self.bar_spacing = 0.4  # 400mm spacing for resilient bars

    def calculate_bar_quantity(self):
        """Calculate number of resilient bars needed"""
        bars_per_row = math.ceil(self.length / self.bar_spacing)
        rows = math.ceil(self.height / 1.0)  # 1m coverage per bar
        quantity = bars_per_row * rows
        self.logger.info(f"Calculated {quantity} resilient bars ({bars_per_row} bars x {rows} rows)")
        return quantity

    def calculate(self, materials):
        try:
            results = []
            self.logger.info("Starting Resilient Bar Ceiling calculation")
            self.logger.info(f"Ceiling Dimensions: Length={self.length}m, Width={self.height}m, Area={self.area}m²")

            for material in materials:
                name = material.get('name')
                
                if name == "12.5mm Sound Plasterboard":
                    self.logger.info(f"Adjusting coverage for {self.plasterboard_layers} layers of plasterboard")
                    material['coverage'] = float(material['coverage']) / self.plasterboard_layers
                
                elif name == "Resilient bar":
                    quantity = self.calculate_bar_quantity()
                    result = {
                        'name': name,
                        'quantity': quantity,
                        'unit_cost': float(material.get('cost', 0)),
                        'total_cost': quantity * float(material.get('cost', 0)),
                        'coverage': float(material.get('coverage', 0))
                    }
                    results.append(result)
                    continue
                
                result = self.calculate_material_quantity(material)
                results.append(result)

            return results

        except Exception as e:
            self.logger.error(f"Error in Resilient Bar Ceiling calculation: {str(e)}")
            return None


class ResilientBarCeilingSP15(ResilientBarCeilingStandard):
    """SP15 version uses single layer of plasterboard plus SP15 Soundboard."""
    
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 1  # Override to single layer

    def calculate(self, materials):
        try:
            self.logger.info("Starting Resilient Bar Ceiling (SP15 Soundboard upgrade)")
            return super().calculate(materials)
        except Exception as e:
            self.logger.error(f"Error in Resilient Bar Ceiling SP15 calculation: {str(e)}")
            return None