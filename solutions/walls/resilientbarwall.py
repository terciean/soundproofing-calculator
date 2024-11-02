from solutions.base_calculator import BaseCalculator
import math

class ResilientBarWallStandard(BaseCalculator):
    """Calculates materials for the Resilient Bar Wall Standard solution."""
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 2  # Two layers by default
        self.bar_spacing = 0.4  # 400mm spacing for resilient bars

    def calculate_bar_quantity(self):
        """Calculate number of resilient bars needed based on wall dimensions"""
        bars_needed = math.ceil(self.length / self.bar_spacing)
        self.logger.info(f"Calculated {bars_needed} resilient bars at {self.bar_spacing}m spacing")
        return bars_needed

    def calculate(self, materials):
        """Calculate quantities for Resilient Bar Wall Standard solution"""
        try:
            results = []
            self.logger.info("Starting Resilient Bar Wall Standard calculation")
            self.logger.info(f"Wall Dimensions: Length={self.length}m, Height={self.height}m, Area={self.area}m²")

            for material in materials:
                result = self.calculate_material_quantity(material)
                results.append(result)

            return results

        except Exception as e:
            self.logger.error(f"Error in Resilient Bar Wall Standard calculation: {str(e)}")
            return None


class ResilientBarWallSP15(ResilientBarWallStandard):
    """SP15 version uses single layer of plasterboard plus SP15 Soundboard."""
    
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 1  # Override to single layer

    def calculate(self, materials):
        """Calculate quantities for Resilient Bar Wall SP15 solution"""
        try:
            self.logger.info("Starting Resilient Bar Wall (SP15 Soundboard upgrade)")
            return super().calculate(materials)
        except Exception as e:
            self.logger.error(f"Error in Resilient Bar Wall SP15 calculation: {str(e)}")
            return None