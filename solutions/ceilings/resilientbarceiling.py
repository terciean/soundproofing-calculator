import math

class ResilientBarCeilingStandard:
    """
    Calculates materials for the Resilient Bar Ceiling solution.
    """
    def __init__(self, length, height):
        self.length = float(length)
        self.height = float(height)
        self.area = self.length * self.height
        self.extra_multiplier = 1.10  # 10% extra for wastage

    def calculate(self, materials):
        try:
            results = []
            print("\nStarting Resilient Bar Ceiling calculation")
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

                quantity = 0
                area_needed = self.area
                layers = 1

                # Special handling for different materials
                if material_name == '12.5mm sound plasterboard':
                    layers = 2  # Double layer as per notes
                    area_needed = self.area * self.extra_multiplier * layers
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Sound Plasterboard: Double layer with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'rockwool rw3 100mm':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Rockwool RW3: 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'resilient bar':
                    # Calculate based on ceiling width, bars spaced at 400mm
                    bars_per_row = math.ceil(self.length / 0.4)  # 400mm spacing
                    rows = math.ceil(self.height / 1.0)  # 1m coverage per bar
                    quantity = bars_per_row * rows
                    print(f"Resilient Bar: {quantity} bars needed ({bars_per_row} bars x {rows} rows)")
                
                elif material_name == 'acoustic sealant':
                    quantity = math.ceil(perimeter / coverage)
                    print(f"Acoustic Sealant: Based on perimeter: {perimeter}m")
                
                elif material_name == 'screws':
                    # Extra screws needed for resilient bars
                    quantity = math.ceil((self.area * 2) / coverage)  # Double for two layers
                    print(f"Screws: Double quantity for two layers")
                
                elif material_name == 'floor protection':
                    quantity = math.ceil(self.area / coverage)
                    print(f"Floor Protection: Based on ceiling area")
                
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
            print(f"Error in Resilient Bar Ceiling calculation: {str(e)}")
            return None

# ... keep the ResilientBarCeilingStandard class unchanged ...

class ResilientBarCeilingSP15:
    """
    Calculates materials for the Resilient Bar Ceiling solution with SP15 Soundboard upgrade.
    """
    def __init__(self, length, height):
        self.length = float(length)
        self.height = float(height)
        self.area = self.length * self.height
        self.extra_multiplier = 1.10  # 10% extra for wastage

    def calculate(self, materials):
        try:
            results = []
            print("\nStarting Resilient Bar Ceiling SP15 calculation")
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

                quantity = 0
                area_needed = self.area
                layers = 1

                # Special handling for different materials
                if material_name == '12.5mm sound plasterboard':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Sound Plasterboard: Single layer with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'sp15 soundboard':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"SP15 Soundboard: With 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'rockwool rw3 100mm':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Rockwool RW3: 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'resilient bar':
                    # Calculate based on ceiling width, bars spaced at 400mm
                    bars_per_row = math.ceil(self.length / 0.4)  # 400mm spacing
                    rows = math.ceil(self.height / 1.0)  # 1m coverage per bar
                    quantity = bars_per_row * rows
                    print(f"Resilient Bar: {quantity} bars needed ({bars_per_row} bars x {rows} rows)")
                
                elif material_name == 'acoustic sealant':
                    # Double the perimeter for two layers (plasterboard + SP15)
                    quantity = math.ceil((perimeter * 2) / coverage)
                    print(f"Acoustic Sealant: Based on double perimeter: {perimeter * 2}m")
                
                elif material_name == 'screws':
                    # Extra screws needed for resilient bars and two boards
                    quantity = math.ceil((self.area * 2.5) / coverage)  # 2.5x for resilient bars + two boards
                    print(f"Screws: Extra quantity for resilient bars and two boards")
                
                elif material_name == 'floor protection':
                    quantity = math.ceil(self.area / coverage)
                    print(f"Floor Protection: Based on ceiling area")
                
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
            print(f"Error in Resilient Bar Ceiling SP15 calculation: {str(e)}")
            return None