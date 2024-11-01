import math

class IndependentCeilingStandard:
    """
    Calculates materials for the Independent Ceiling solution.
    Accounts for material-specific calculations and wastage.
    """
    def __init__(self, length, height):
        self.length = float(length)
        self.height = float(height)
        self.area = self.length * self.height
        self.extra_multiplier = 1.10  # 10% extra for wastage

    def calculate(self, materials):
        """
        Calculate quantities for Independent Ceiling solution.
        
        Args:
            materials (list): List of material dictionaries from MongoDB.
            
        Returns:
            list: List of calculated material requirements with quantities and costs.
        """
        try:
            results = []
            print("\nStarting Independent Ceiling calculation")
            print(f"Ceiling Dimensions: Length = {self.length}m, Width = {self.height}m, Area = {self.area}m²")
            
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
                if material_name == '19mm plank plasterboard':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Plank Plasterboard: Single layer with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == '12.5mm sound plasterboard':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Sound Plasterboard: Single layer with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'acoustic sealant':
                    quantity = math.ceil(perimeter / coverage)
                    print(f"Acoustic Sealant: Based on perimeter: {perimeter}m")
                
                elif material_name == 'rockwool rw3 100mm':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Rockwool RW3: 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'resilient bar':
                    # One bar every 400mm of ceiling width
                    bars_needed = math.ceil(self.length / 0.4)  # 400mm spacing
                    quantity = math.ceil(bars_needed)
                    print(f"Resilient Bar: {quantity} pieces needed with 400mm spacing")
                
                elif material_name == 'timber and fixings':
                    quantity = math.ceil(self.area)  # 1m² coverage
                    print(f"Timber and Fixings: Based on ceiling area")
                
                elif material_name == 'screws':
                    # For screws, always use 1 box
                    quantity = 1
                    print(f"Screws: Minimum 1 box required for any size ceiling")
                
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
            print(f"Error in Independent Ceiling calculation: {str(e)}")
            return None


# ... (keep IndependentCeilingStandard class the same) ...

class IndependentCeilingSP15(IndependentCeilingStandard):
    """
    SP15 version inherits from Standard but includes SP15 Soundboard calculations.
    """
    def calculate(self, materials):
        """Calculate quantities for Independent Ceiling SP15 solution"""
        try:
            results = []
            print("\nStarting Independent Ceiling (SP15 Soundboard upgrade)")
            print(f"Ceiling Dimensions: Length = {self.length}m, Width = {self.height}m, Area = {self.area}m²")
            
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
                if material_name == 'sp15 soundboard':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"SP15 Soundboard: Single layer with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == '12.5mm sound plasterboard':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Sound Plasterboard: Single layer with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'acoustic sealant':
                    quantity = math.ceil(perimeter / coverage)
                    print(f"Acoustic Sealant: Based on perimeter: {perimeter}m")
                
                elif material_name == 'rockwool rw3 100mm':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Rockwool RW3: 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'resilient bar':
                    # One bar every 400mm of ceiling width
                    bars_needed = math.ceil(self.length / 0.4)  # 400mm spacing
                    quantity = math.ceil(bars_needed)
                    print(f"Resilient Bar: {quantity} pieces needed with 400mm spacing")
                
                elif material_name == 'timber and fixings':
                    quantity = math.ceil(self.area)  # 1m² coverage
                    print(f"Timber and Fixings: Based on ceiling area")
                
                elif material_name == 'screws':
                    # For screws, always use 1 box
                    quantity = 1
                    print(f"Screws: Minimum 1 box required for any size ceiling")
                
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
            print(f"Error in Independent Ceiling SP15 calculation: {str(e)}")
            return None