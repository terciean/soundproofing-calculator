from solutions.base_calculator import BaseCalculator
import math

class GenieClipWallStandard(BaseCalculator):
    """
    Calculates materials for the Genie Clip Wall Standard solution.
    Two layers of 12.5mm Sound Plasterboard by default.
    """
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 2

    def calculate(self, materials):
        """Calculate quantities for Genie Clip Wall Standard solution"""
        try:
            results = []
            self.logger.info("Starting Genie Clip Wall Standard calculation")
            self.logger.info(f"Wall Dimensions: Length={self.length}m, Height={self.height}m, Area={self.area}m²")

            for material in materials:
                result = self.calculate_material_quantity(material)
                results.append(result)

            return results

        except Exception as e:
            self.logger.error(f"Error in Genie Clip Wall Standard calculation: {str(e)}")
            return None


class GenieClipWallSP15(GenieClipWallStandard):
    """SP15 version uses single layer of plasterboard plus SP15 Soundboard."""
    
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 1  # Override to single layer