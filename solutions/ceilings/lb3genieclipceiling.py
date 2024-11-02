from ..base_calculator import BaseCalculator

class LB3GenieClipCeilingStandard(BaseCalculator):
    """
    Calculates materials for the LB3 Genie Clip Ceiling solution.
    """
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 2  # Two layers by default

    def calculate(self, materials):
        try:
            results = []
            self.logger.info("Starting LB3 Genie Clip Ceiling calculation")
            self.logger.info(f"Ceiling Dimensions: Length={self.length}m, Width={self.height}m, Area={self.area}m²")

            for material in materials:
                name = material.get('name')
                
                # Handle double layer of plasterboard
                if name == "12.5mm Sound Plasterboard":
                    self.logger.info(f"Adjusting coverage for {self.plasterboard_layers} layers of plasterboard")
                    material['coverage'] = float(material['coverage']) / self.plasterboard_layers
                
                # Special handling for LB3 Genie Clips
                elif name == "LB3 Genie Clip":
                    self.logger.info("Calculating LB3 Genie Clip requirements")
                
                result = self.calculate_material_quantity(material)
                results.append(result)

            return results

        except Exception as e:
            self.logger.error(f"Error in LB3 Genie Clip Ceiling calculation: {str(e)}")
            return None


class LB3GenieClipCeilingSP15(LB3GenieClipCeilingStandard):
    """SP15 version uses single layer of plasterboard plus SP15 Soundboard."""
    
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 1  # Override to single layer

    def calculate(self, materials):
        try:
            self.logger.info("Starting LB3 Genie Clip Ceiling (SP15 Soundboard upgrade)")
            return super().calculate(materials)
        except Exception as e:
            self.logger.error(f"Error in LB3 Genie Clip Ceiling SP15 calculation: {str(e)}")
            return None