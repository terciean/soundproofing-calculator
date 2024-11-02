from ..base_calculator import BaseCalculator

class GenieClipCeilingStandard(BaseCalculator):
    """
    Calculates materials for the Genie Clip Ceiling solution.
    """
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 2  # Two layers by default

    def calculate(self, materials):
        try:
            results = []
            self.logger.info("Starting Genie Clip Ceiling calculation")
            self.logger.info(f"Ceiling Dimensions: Length={self.length}m, Width={self.height}m, Area={self.area}m²")

            for material in materials:
                name = material.get('name')
                
                if name == "12.5mm Sound Plasterboard":
                    self.logger.info(f"Adjusting coverage for {self.plasterboard_layers} layers of plasterboard")
                    material['coverage'] = float(material['coverage']) / self.plasterboard_layers
                
                elif name == "Genie Clip":
                    self.logger.info("Calculating Genie Clip requirements")
                
                elif name == "Furring Channel":
                    self.logger.info("Calculating Furring Channel requirements")
                
                result = self.calculate_material_quantity(material)
                results.append(result)

            return results

        except Exception as e:
            self.logger.error(f"Error in Genie Clip Ceiling calculation: {str(e)}")
            return None


class GenieClipCeilingSP15(GenieClipCeilingStandard):
    """SP15 version uses single layer of plasterboard plus SP15 Soundboard."""
    
    def __init__(self, length, height):
        super().__init__(length, height)
        self.plasterboard_layers = 1  # Override to single layer