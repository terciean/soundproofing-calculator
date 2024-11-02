from solutions.base_calculator import BaseCalculator
import math



class IndependentWallStandard(BaseCalculator):
    """Calculates materials for the Independent Wall Standard solution."""
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 2  # Two layers by default

    def calculate(self, materials):
        """Calculate quantities for Independent Wall Standard solution"""
        try:
            results = []
            self.logger.info("Starting Independent Wall Standard calculation")
            self.logger.info(f"Wall Dimensions: Length={self.length}m, Height={self.height}m, Area={self.area}m²")

            for material in materials:
                result = self.calculate_material_quantity(material)
                results.append(result)

            return results

        except Exception as e:
            self.logger.error(f"Error in Independent Wall Standard calculation: {str(e)}")
            return None


class IndependentWallSP15(IndependentWallStandard):
    """SP15 version uses single layer of plasterboard plus SP15 Soundboard."""
    
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 1  # Override to single layer

    def calculate(self, materials):
        """Calculate quantities for Independent Wall SP15 solution"""
        try:
            self.logger.info("Starting Independent Wall (SP15 Soundboard upgrade)")
            return super().calculate(materials)
        except Exception as e:
            self.logger.error(f"Error in Independent Wall SP15 calculation: {str(e)}")
            return None