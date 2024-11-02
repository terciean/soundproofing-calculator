import math

class IndependentWallStandard:
    """
    Calculates materials for the Independent Wall (Standard) solution.
    Accounts for 2 layers of 12.5mm Sound Plasterboard and applies material-specific wastage.
    """
def calculate(self, materials):
    try:
        results = []
        print("\nStarting IndependentWallStandard.calculate()")
        print(f"Wall Dimensions: Length = {self.length}m, Height = {self.height}m, Area = {self.area}m²")
        
        # Calculate perimeter for acoustic sealant
        perimeter = 2 * (self.length + self.height)
        print(f"Perimeter = {perimeter}m")

        for material in materials:
            # Convert material name to lowercase for comparison, but keep original for display
            original_name = material.get('name', '')
            material_name = original_name.strip().lower()
            coverage_str = str(material.get('coverage', '0')).strip()
            coverage = float(coverage_str)
            cost = float(material.get('cost', 0))

            print(f"\nProcessing Material: {original_name}")
            print(f"Coverage per Unit: {coverage}m², Unit Cost: £{cost}")

            if coverage <= 0:
                raise ValueError(f"Invalid coverage value for material: {original_name}")

            # Initialize variables
            quantity = 0
            area_needed = self.area
            layers = 1

            # Special handling for different materials - using lowercase for comparison
            if '12.5mm sound plasterboard' in material_name:
                layers = 2
                area_needed = self.area * layers * self.extra_multiplier
                quantity = math.ceil(area_needed / coverage)
                print(f"Plasterboard: {layers} layers with 10% extra, Area needed: {area_needed}m²")
            
            elif 'acoustic sealant' in material_name:
                quantity = math.ceil(perimeter / coverage)
                print(f"Acoustic Sealant: Based on perimeter: {perimeter}m")
            
            elif 'rockwool rwa45' in material_name or 'tecsound' in material_name:
                area_needed = self.area * self.extra_multiplier
                quantity = math.ceil(area_needed / coverage)
                print(f"{original_name}: 10% extra, Area needed: {area_needed}m²")
            
            elif any(x in material_name for x in ['metal frame', 'resilient bar', 'floor protection']):
                quantity = math.ceil(self.area / coverage)
                print(f"{original_name}: Standard calculation")
            
            elif 'screws' in material_name:
                quantity = 1
                print(f"Screws: Minimum 1 box required for any size wall")
            
            else:
                quantity = math.ceil(self.area / coverage)
                print(f"{original_name}: Default calculation")

            total_cost = quantity * cost
            print(f"Final Quantity: {quantity}, Total Cost: £{total_cost}")

            results.append({
                'name': original_name,
                'quantity': quantity,
                'unit_cost': cost,
                'total_cost': total_cost,
                'coverage': coverage,
                'layers': layers
            })

        return results

    except Exception as e:
        print(f"Error in Independent Wall Standard calculation: {str(e)}")
        return None
class IndependentWallSP15(IndependentWallStandard):
    def calculate(self, materials):
        """
        Calculate quantities for Independent Wall Standard solution.
        Includes 10% extra allowance for panels, plasterboard, Tecsound, and Rockwool.
        """
        try:
            results = []
            print(f"\nStarting IndependentWallStandard.calculate()")
            print(f"Wall Dimensions: Length = {self.length}m, Height = {self.height}m, Area = {self.area}m²")
            
            # Calculate perimeter for acoustic sealant
            perimeter = 2 * (self.length + self.height)
            print(f"Perimeter = {perimeter}m")

            for material in materials:
                material_name = material.get('name', '').strip().lower()
                coverage = float(material.get('coverage', 0))
                cost = float(material.get('cost', 0))

                print(f"\nProcessing Material: {material_name}")
                print(f"Coverage per Unit: {coverage}m², Unit Cost: £{cost}")

                if coverage <= 0:
                    raise ValueError(f"Invalid coverage value for material: {material_name}")

                # Initialize variables
                quantity = 0
                area_needed = self.area
                
                # Special handling for different materials
                if material_name == '12.5mm sound plasterboard':
                    # Two layers with 10% extra
                    area_needed = self.area * 2 * 1.10
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Plasterboard: 2 layers with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'acoustic sealant':
                    # Calculate based on perimeter
                    quantity = math.ceil(perimeter / coverage)
                    print(f"Acoustic Sealant: Based on perimeter: {perimeter}m")
                
                elif material_name in ['rockwool rwa45 50mm', 'tecsound 50']:
                    # 10% extra for offcuts
                    area_needed = self.area * 1.10
                    quantity = math.ceil(area_needed / coverage)
                    print(f"{material_name}: 10% extra, Area needed: {area_needed}m²")
                
                elif material_name in ['metal frame work', 'resilient bar']:
                    # Standard calculation without extra
                    quantity = math.ceil(self.area / coverage)
                    print(f"{material_name}: Standard calculation")
                
                elif material_name in ['screws', 'floor protection']:
                    # Standard calculation without extra
                    quantity = math.ceil(self.area / coverage)
                    print(f"{material_name}: Standard calculation")
                
                else:
                    # Default calculation
                    quantity = math.ceil(self.area / coverage)
                    print(f"{material_name}: Default calculation")

                total_cost = quantity * cost
                print(f"Final Quantity: {quantity}, Total Cost: £{total_cost}")

                results.append({
                    'name': material.get('name'),
                    'quantity': quantity,
                    'unit_cost': cost,
                    'total_cost': total_cost,
                    'coverage': coverage
                })

            return results

        except Exception as e:
            print(f"Error in Independent Wall Standard calculation: {str(e)}")
            return None