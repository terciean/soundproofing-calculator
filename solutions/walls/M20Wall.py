from solutions.base_calculator import BaseCalculator
import math

class M20WallStandard(BaseCalculator):
    """Calculates materials for the M20 Wall Standard solution."""
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 2  # Two layers by default

    def calculate(self, materials):
        """Calculate quantities for M20 Wall Standard solution"""
        try:
            results = []
            self.logger.info("Starting M20 Solution (Standard)")
            self.logger.info(f"Wall Dimensions: Length={self.length}m, Height={self.height}m, Area={self.area}m²")

            for material in materials:
                result = self.calculate_material_quantity(material)
                results.append(result)

            return results

        except Exception as e:
            self.logger.error(f"Error in M20 Solution (Standard) calculation: {str(e)}")
            return None

class M20WallSP15(M20WallStandard):
    """SP15 version uses single layer of plasterboard plus SP15 Soundboard."""
    
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 1  # Override to single layer

    def calculate(self, materials):
        """Calculate quantities for M20 Wall SP15 solution"""
        try:
            self.logger.info("Starting M20 Solution (SP15 Soundboard upgrade)")
            return super().calculate(materials)
        except Exception as e:
            self.logger.error(f"Error in M20 Solution (SP15 Soundboard upgrade) calculation: {str(e)}")
            return None