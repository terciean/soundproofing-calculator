import math

class LB3GenieClipCeilingStandard:
    """
    Calculates materials for the LB3 Genie Clip Ceiling solution.
    """
    def __init__(self, length, height):
        self.length = float(length)
        self.height = float(height)
        self.area = self.length * self.height
        self.extra_multiplier = 1.10  # 10% extra for wastage

    def calculate(self, materials):
        try:
            results = []
            print("\nStarting LB3 Genie Clip Ceiling calculation")
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
                    layers = 2  # Two layers as per notes
                    area_needed = self.area * self.extra_multiplier * layers
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Sound Plasterboard: Double layer with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'lb3 genie clip':
                    # One clip every 0.25m² as per coverage
                    quantity = math.ceil(self.area / coverage)
                    print(f"LB3 Genie Clips: {quantity} clips needed (1 per {coverage}m²)")
                
                elif material_name == 'furring channel':
                    quantity = math.ceil(self.area / coverage)
                    print(f"Furring Channel: {quantity} pieces needed")
                
                elif material_name == 'resilient bar':
                    quantity = math.ceil(self.area / coverage)
                    print(f"Resilient Bar: {quantity} pieces needed")
                
                elif material_name == 'rockwool rw3 100mm':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Rockwool RW3: 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'acoustic sealant':
                    quantity = math.ceil(perimeter / coverage)
                    print(f"Acoustic Sealant: Based on perimeter: {perimeter}m")
                
                elif material_name == 'screws':
                    quantity = math.ceil(self.area / coverage)
                    print(f"Screws: Based on ceiling area")
                
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
            print(f"Error in LB3 Genie Clip Ceiling calculation: {str(e)}")
            return None
        
class LB3GenieClipCeilingSP15:
    """
    Calculates materials for the LB3 Genie Clip Ceiling solution with SP15 Soundboard upgrade.
    """
    def __init__(self, length, height):
        self.length = float(length)
        self.height = float(height)
        self.area = self.length * self.height
        self.extra_multiplier = 1.10  # 10% extra for wastage

    def calculate(self, materials):
        try:
            results = []
            print("\nStarting LB3 Genie Clip Ceiling SP15 calculation")
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
                    # One layer as per notes for SP15 version
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Sound Plasterboard: Single layer with 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'sp15 soundboard':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"SP15 Soundboard: Area needed with 10% extra: {area_needed}m²")
                
                elif material_name == 'lb3 genie clip':
                    quantity = math.ceil(self.area / coverage)
                    print(f"LB3 Genie Clips: {quantity} clips needed (1 per {coverage}m²)")
                
                elif material_name == 'furring channel':
                    quantity = math.ceil(self.area / coverage)
                    print(f"Furring Channel: {quantity} pieces needed")
                
                elif material_name == 'resilient bar':
                    quantity = math.ceil(self.area / coverage)
                    print(f"Resilient Bar: {quantity} pieces needed")
                
                elif material_name == 'rockwool rw3 100mm':
                    area_needed = self.area * self.extra_multiplier
                    quantity = math.ceil(area_needed / coverage)
                    print(f"Rockwool RW3: 10% extra, Area needed: {area_needed}m²")
                
                elif material_name == 'acoustic sealant':
                    quantity = math.ceil(perimeter / coverage)
                    print(f"Acoustic Sealant: Based on perimeter: {perimeter}m")
                
                elif material_name == 'screws':
                    quantity = math.ceil(self.area / coverage)
                    print(f"Screws: Based on ceiling area")
                
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
            print(f"Error in LB3 Genie Clip Ceiling SP15 calculation: {str(e)}")
            return None