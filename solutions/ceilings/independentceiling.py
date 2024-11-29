from solutions.base_calculator import BaseCalculator
import math

class IndependentCeilingStandard(BaseCalculator):

    """
    Calculates materials for the Independent Ceiling solution.
    """
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 1  # Single layer by default
        self.bar_spacing = 0.4  # 400mm spacing for resilient bars

    def calculate_bar_quantity(self):
        """Calculate number of resilient bars needed"""
        bars_needed = math.ceil(self.length / self.bar_spacing)
        self.logger.info(f"Calculated {bars_needed} resilient bars at {self.bar_spacing}m spacing")
        return bars_needed

    def calculate(self, materials):
        try:
            results = []
            self.logger.info("Starting Independent Ceiling calculation")
            self.logger.info(f"Ceiling Dimensions: Length={self.length}m, Width={self.height}m, Area={self.area}m²")

            for material in materials:
                name = material.get('name')
                
                if name == "19mm Plank Plasterboard":
                    self.logger.info("Calculating Plank Plasterboard requirements")
                
                elif name == "12.5mm Sound Plasterboard":
                    self.logger.info(f"Calculating Sound Plasterboard requirements")
                
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
            self.logger.error(f"Error in Independent Ceiling calculation: {str(e)}")
            return None


class IndependentCeilingSP15(IndependentCeilingStandard):
    """SP15 version uses SP15 Soundboard."""
    
    def calculate(self, materials):
        try:
            self.logger.info("Starting Independent Ceiling (SP15 Soundboard upgrade)")
            return super().calculate(materials)
        except Exception as e:
            self.logger.error(f"Error in Independent Ceiling SP15 calculation: {str(e)}")
            return None