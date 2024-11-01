import math

class M20WallStandard:
    """
    Calculates materials for the M20 Wall Standard solution.
    """
    def __init__(self, length, height):
        self.length = float(length)
        self.height = float(height)
        self.area = self.length * self.height
        self.extra_multiplier = 1.10  # 10% extra

    def calculate(self, materials):
        """Calculate quantities for M20 Wall Standard solution"""
        try:
            results = []
            print("\nStarting M20 Solution (Standard)")  # Updated to match app.py
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
                
                elif material_name in ['rockwool rwa45 50mm', 'tecsound 50', 'panels']:
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"{material_name}: 10% extra, Area needed: {area_needed}m²")

                elif material_name == 'screws':
                    # For screws, always use 1 box
                    quantity = 1
                    print(f"Screws: Minimum 1 box required for any size wall")
                
                elif material_name == 'floor protection':
                    quantity = math.ceil(self.area / 30.0)  # 30m² per roll
                    print(f"Floor Protection: Based on 30m² coverage")
                
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
            print(f"Error in M20 Solution (Standard) calculation: {str(e)}")
            return None

class M20WallSP15(M20WallStandard):
    """
    SP15 version inherits from Standard as the calculation logic is the same.
    The parent class already handles the 10% extra for:
    - Panels
    - Plasterboard (2 layers + 10%)
    - Tecsound
    - Rockwool
    All other materials are calculated without wastage.
    """
    def calculate(self, materials):
        """Calculate quantities for M20 Wall SP15 solution"""
        try:
            print("\nStarting M20 Solution (SP15 Soundboard upgrade)")  # Changed to match app.py exactly
            return super().calculate(materials)
        except Exception as e:
            print(f"Error in M20 Solution (SP15 Soundboard upgrade) calculation: {str(e)}")  # Changed to match app.py exactly
            return None