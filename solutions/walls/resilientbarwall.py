import math

class ResilientBarWallStandard:
    """
    Calculates materials for the Resilient Bar Wall Standard solution.
    Accounts for material-specific calculations and wastage.
    """
    def __init__(self, length, height):
        self.length = float(length)
        self.height = float(height)
        self.area = self.length * self.height
        self.extra_multiplier = 1.10  # 10% extra for wastage

    def calculate(self, materials):
        """
        Calculate quantities for Resilient Bar Wall Standard solution.
        
        Args:
            materials (list): List of material dictionaries from MongoDB.
            
        Returns:
            list: List of calculated material requirements with quantities and costs.
        """
        try:
            results = []
            print("\nStarting ResilientBarWallStandard.calculate()")
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
                    # Single layer for resilient bar wall
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Plasterboard: Single layer with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'acoustic sealant':
                    # Based on linear meters of perimeter
                    quantity = math.ceil(perimeter / 3.0)  # 3m coverage per tube
                    print(f"Acoustic Sealant: Based on perimeter: {perimeter}m")
                
                elif material_name == 'rockwool rw3 100mm':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / 2.88)  # 2.88m² coverage per pack
                    print(f"Rockwool RW3: 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'resilient bar':
                    # One bar every 400mm of wall length
                    bars_needed = math.ceil(self.length / 0.4)  # 400mm spacing
                    quantity = math.ceil(bars_needed)
                    print(f"Resilient Bar: {quantity} pieces needed with 400mm spacing")
                
                elif material_name == 'screws':
                    # For screws, we use the coverage value from MongoDB (30m² per box)
                    # Always need at least 1 box
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
            print(f"Error in Resilient Bar Wall Standard calculation: {str(e)}")
            return None


class ResilientBarWallSP15(ResilientBarWallStandard):
    """
    SP15 version inherits from Standard but includes SP15 Soundboard calculations.
    """
    def calculate(self, materials):
        """Calculate quantities for Resilient Bar Wall SP15 solution"""
        try:
            print("\nStarting Resilient Bar Wall (SP15 Soundboard upgrade)")
            return super().calculate(materials)
        except Exception as e:
            print(f"Error in Resilient Bar Wall SP15 calculation: {str(e)}")
            return None