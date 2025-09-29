import math
from solutions.base_calculator import BaseCalculator
from typing import Dict, List, Optional
from .logger import logger

class Room:
    """Class to handle room dimensions"""
    
    def __init__(self, dimensions: Dict[str, float], surfaces: List[str], room_type: Optional[str] = None):
        self.dimensions = dimensions
        self.surfaces = surfaces
        self.room_type = room_type
        self.calculator = BaseCalculator(dimensions['length'], dimensions['height'])
        self.walls = []
        self.ceilings = []
        self.floors = []
        self.total_cost = 0
        self.materials = []
        self.solutions = {}  # Track active solutions by surface type

    def set_dimensions(self, length: float, width: float, height: float) -> bool:
        """Set room dimensions with basic number validation"""
        try:
            # Convert to float and validate
            dimensions = {
                'length': float(length),
                'width': float(width),
                'height': float(height)
            }
            
            self.dimensions = dimensions
            logger.info(f"Set room dimensions: {self.dimensions}")
            return True
            
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid dimensions - must be valid numbers: {str(e)}")
            return False

    def get_dimensions(self) -> Dict[str, float]:
        """Get current room dimensions"""
        return self.dimensions.copy()

    def get_area(self) -> float:
        """Get total area of the room"""
        return self.calculator.area
        
    def get_perimeter(self) -> float:
        """Get perimeter of the room"""
        return self.calculator.calculate_perimeter()
        
    def get_surface_area(self, surface_type: str) -> float:
        """Get area of a specific surface"""
        if surface_type not in self.surfaces:
            return 0.0
            
        if surface_type == "walls":
            return self.dimensions['length'] * self.dimensions['height'] * 2 + \
                   self.dimensions['width'] * self.dimensions['height'] * 2
        elif surface_type == "ceiling" or surface_type == "floor":
            return self.dimensions['length'] * self.dimensions['width']
            
        return 0.0
        
    def get_total_surface_area(self) -> float:
        """Get total area of all surfaces"""
        total = 0.0
        for surface in self.surfaces:
            total += self.get_surface_area(surface)
        return total
        
    def get_volume(self) -> float:
        """Get volume of the room"""
        return self.dimensions['length'] * self.dimensions['width'] * self.dimensions['height']

    def add_wall(self, solution_data, wall_name=None):
        """Add wall solution data"""
        if solution_data:
            if wall_name:
                self.solutions[f'wall_{wall_name}'] = solution_data
            self.walls.append(solution_data)
            if 'total_cost' in solution_data:
                self.total_cost += solution_data['total_cost']
            if 'materials' in solution_data:
                self._add_materials(solution_data['materials'])

    def add_ceiling(self, solution_data, ceiling_name=None):
        """Add ceiling solution data"""
        if solution_data:
            if ceiling_name:
                self.solutions[f'ceiling_{ceiling_name}'] = solution_data
            self.ceilings.append(solution_data)
            if 'total_cost' in solution_data:
                self.total_cost += solution_data['total_cost']
            if 'materials' in solution_data:
                self._add_materials(solution_data['materials'])

    def _add_materials(self, materials):
        """Helper method to add materials with wastage calculation"""
        for material in materials:
            needs_wastage = material['name'] in BaseCalculator.WASTAGE_MATERIALS
            if needs_wastage:
                material['amount'] = math.ceil(material['amount'] * 1.1)
                material['cost'] = material['amount'] * material.get('cost', 0)
            self.materials.append(material)

    def get_solution(self, surface_type, name):
        """Get specific solution data"""
        key = f'{surface_type}_{name}'
        return self.solutions.get(key)

    def get_total_cost(self):
        """Get total cost of all solutions"""
        return self.total_cost

    def get_all_materials(self):
        """Get combined materials list with quantities"""
        combined = {}
        for material in self.materials:
            name = material['name']
            if name in combined:
                combined[name]['amount'] += material['amount']
                combined[name]['cost'] += material['cost']
            else:
                combined[name] = material.copy()
        return list(combined.values())