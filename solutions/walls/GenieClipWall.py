import math

class GenieClipWallStandard:
    """
    Calculates materials for the Genie Clip Wall Standard solution.
    Accounts for material-specific calculations and wastage.
    """
    def __init__(self, length, height):
        self.length = float(length)
        self.height = float(height)
        self.area = self.length * self.height
        self.extra_multiplier = 1.10  # 10% extra for wastage

    def calculate(self, materials):
        """
        Calculate quantities for Genie Clip Wall Standard solution.
        
        Args:
            materials (list): List of material dictionaries from MongoDB.
            
        Returns:
            list: List of calculated material requirements with quantities and costs.
        """
        try:
            results = []
            print("\nStarting GenieClipWallStandard.calculate()")
            print(f"Wall Dimensions: Length = {self.length}m, Height = {self.height}m, Area = {self.area}m²")
            
            # Calculate perimeter for acoustic sealant
            perimeter = 2 * (self.length + self.height)
            print(f"Perimeter = {perimeter}m")

            for material in materials:
                material_name = material.get('name', '').strip().lower()
                coverage_str = material.get('coverage', '0').strip()
                coverage = float(coverage_str)
                cost = float(material.get('cost', 0))

                print(f"\nProcessing Material: {material_name}")
                print(f"Coverage per Unit: {coverage}m², Unit Cost: £{cost}")

                if coverage <= 0:
                    raise ValueError(f"Invalid coverage value for material: {material_name}")

                # Initialize variables
                quantity = 0
                area_needed = self.area
                layers = 1

                # Special handling for different materials
                if material_name == '12.5mm sound plasterboard':
                    layers = 2
                    area_needed = self.area * layers * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Plasterboard: {layers} layers with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'acoustic sealant':
                    quantity = math.ceil(perimeter / coverage)
                    print(f"Acoustic Sealant: Based on perimeter: {perimeter}m")
                
                elif material_name in ['rockwool rwa45 50mm', 'tecsound 50']:
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"{material_name}: 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'genie clips':
                    # Special calculation for Genie Clips based on area coverage
                    clips_per_sqm = 1 / coverage  # Coverage is area per clip
                    quantity = math.ceil(self.area * clips_per_sqm * self.extra_multiplier)
                    print(f"Genie Clips: {clips_per_sqm} clips per m², Total needed: {quantity}")
                
                elif material_name == 'furring channel':
                    # Calculate based on height with extra for joints
                    channels_needed = math.ceil(self.length / 0.6)  # 600mm spacing
                    quantity = math.ceil(channels_needed * self.extra_multiplier)
                    print(f"Furring Channel: {channels_needed} pieces needed with spacing")
                elif material_name == 'screws':
                    # For screws, always use 1 box
                    quantity = 1
                    print(f"Screws: Minimum 1 box required for any size wall")
                
                else:
                    quantity = math.ceil(self.area / coverage)
                    print(f"{material_name}: Standard calculation")

                total_cost = quantity * cost
                print(f"Final Quantity: {quantity}, Total Cost: £{total_cost}")

                results.append({
                    'name': material.get('name'),
                    'quantity': quantity,
                    'unit_cost': cost,
                    'total_cost': total_cost,
                    'coverage': coverage,
                    'layers': layers
                })

            return results

        except Exception as e:
            print(f"Error in Genie Clip Wall Standard calculation: {str(e)}")
            return None

class GenieClipWallSP15(GenieClipWallStandard):
    """
    SP15 version inherits from Standard but includes SP15 Soundboard calculations.
    """
    def calculate(self, materials):
        """Calculate quantities for Genie Clip Wall SP15 solution"""
        try:
            print("\nStarting Genie Clip Wall (SP15 Soundboard upgrade)")
            return super().calculate(materials)
        except Exception as e:
            print(f"Error in Genie Clip Wall SP15 calculation: {str(e)}")
            return None