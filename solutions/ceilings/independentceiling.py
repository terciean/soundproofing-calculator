from solutions.base_calculator import BaseCalculator
import math

class IndependentCeilingStandard(BaseCalculator):
    """
    Calculates materials for the Independent Ceiling solution.
    """
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 1  # Single layer by default

    def calculate(self, materials):
        try:
            results = []
            self.logger.info("Starting Independent Ceiling calculation")
            self.logger.info(f"Ceiling Dimensions: Length={self.length}m, Width={self.height}m, Area={self.area}m²")

            for material in materials:
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