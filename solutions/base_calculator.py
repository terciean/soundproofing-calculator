from typing import List, Dict, Union, Optional, Any
from schemas.solution_schema import Solution
from schemas.material_properties_schema import MaterialProperties
import math
import logging
from dataclasses import dataclass
from solutions.config import WASTAGE_MATERIALS, SPECIAL_MATERIALS, MATERIAL_COVERAGE, LABOR_COST_PERCENTAGE
from solutions.cache_manager import get_cache_manager
from datetime import datetime
from solutions.database import get_db

class BaseCalculator:
    """Base calculator for all sound insulation solutions."""
    
    def __init__(self, length, height):
        self.length = float(length)
        self.height = float(height)
        self.area = self.length * self.height
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db = get_db()
        self.cache_manager = get_cache_manager()
        self._cache_status = {
            'solution_data': {'cached': False, 'last_updated': None},
            'material_properties': {'cached': False, 'last_updated': None},
            'characteristics': {'cached': False, 'last_updated': None},
            'calculations': {'cached': False, 'last_updated': None}
        }

    def calculate_material_quantity(self, material: Dict) -> float:
        """Calculate quantity needed for a material with support for special cases"""
        try:
            name = material.get('name', '')
            
            # Check for special material handling
            if name in self.SPECIAL_MATERIALS:
                special = self.SPECIAL_MATERIALS[name]
                if "perimeter_based" in special:
                    return math.ceil(self.calculate_perimeter())
                elif "spacing" in special:
                    return math.ceil(self.area / special["spacing"])
                elif "min_quantity" in special:
                    base_quantity = self.area * material.get('unitsPerM2', 1.0)
                    return max(special["min_quantity"], math.ceil(base_quantity))
            
            # Standard material calculation
            base_quantity = self.area * material.get('unitsPerM2', 1.0)
            
            # Add wastage if needed
            if name in self.WASTAGE_MATERIALS:
                base_quantity *= 1.1  # Add 10% wastage
                
            return math.ceil(base_quantity)
            
        except Exception as e:
            self.logger.error(f"Error calculating material quantity: {str(e)}")
            return 0.0

    def calculate_perimeter(self) -> float:
        """Calculate perimeter of the surface."""
        return 2 * (self.length + self.height)

    def get_characteristics(self):
        """Override this in child classes"""
        return {
            "type": None,
            "displayName": None,
            "sound_reduction": 0,
            "stc_rating": 0,
            "frequencyRange": [0, 0],
            "materials": [],
            "baseCost": 0,
            "unitsPerM2": 0,
            "unit": None
        }

    def get_cache_status(self) -> Dict[str, Any]:
        """Get current cache status for this calculator"""
        return self._cache_status
        
    def _update_cache_status(self, cache_type: str, is_cached: bool) -> None:
        """Update cache status for a specific type"""
        self._cache_status[cache_type] = {
            'cached': is_cached,
            'last_updated': datetime.now() if is_cached else None
        }

    def _load_solution_data(self, solution_code: str) -> Dict[str, Any]:
        """Load solution data from MongoDB with caching"""
        try:
            # Try to get from cache first
            cache_key = f"{solution_code}_solution_data"
            cached = self.cache_manager.get(cache_key)
            if cached:
                self._update_cache_status('solution_data', True)
                self.logger.info(f"[DATA SOURCE] {solution_code}: Loaded from CACHE")
                return cached
                
            # If not in cache, load from database
            if self.db is not None:
                # Try collections in order
                for collection_name in ['wallsolutions', 'ceilingsolutions', 'floorsolutions']:
                    try:
                        solution = self.db[collection_name].find_one({"solution": solution_code})
                        if solution is not None:
                            if '_id' in solution:
                                del solution['_id']
                            # Cache the result
                            self.cache_manager.set(cache_key, solution, 3600)  # Cache for 1 hour
                            self._update_cache_status('solution_data', True)
                            self.logger.info(f"[DATA SOURCE] {solution_code}: Loaded from DATABASE ({collection_name})")
                            return solution
                    except Exception as e:
                        self.logger.warning(f"Error accessing {collection_name}: {e}")
        
            # If we reach here, no data was found
            self.logger.warning(f"[DATA SOURCE] {solution_code}: No data found")
            self._update_cache_status('solution_data', False)
            return None
            
        except Exception as e:
            self.logger.error(f"Error loading solution data: {e}")
            self._update_cache_status('solution_data', False)
            return None

    def calculate_costs(self, area):
        """Calculate costs for both single and multi-material solutions"""
        costs = {
            "materials": [],
            "breakdown": {
                "surfaces": [],
                "adjustments": [],
                "totalArea": area,
                "laborCost": 0,
                "materialsCost": 0,
                "totalCost": 0
            }
        }

        characteristics = self.get_characteristics()
        surface_cost = {
            "type": characteristics["type"],
            "area": round(area, 2),
            "solution": characteristics["displayName"],
            "materials": [],
            "totalCost": 0
        }

        try:
            if "materials" in characteristics:
                # Multi-material solution
                for material in characteristics["materials"]:
                    quantity = self.calculate_material_quantity(material)
                    material_cost = quantity * material["baseCost"]
                    
                    material_data = {
                        "name": material["name"],
                        "coverage": {
                            "perUnit": round(1 / material["unitsPerM2"], 2),
                            "total": round(area, 2)
                        },
                        "quantity": quantity,
                        "unit": material["unit"],
                        "costs": {
                            "perUnit": round(material["baseCost"], 2),
                            "total": round(material_cost, 2)
                        }
                    }
                    
                    surface_cost["materials"].append(material_data)
                    surface_cost["totalCost"] += material_cost
                    costs["materials"].append({
                        "name": material["name"],
                        "quantity": quantity,
                        "unit": material["unit"],
                        "cost": material_cost
                    })
            else:
                # Single-material solution
                quantity = math.ceil(area * characteristics["unitsPerM2"])
                material_cost = quantity * characteristics["baseCost"]
                
                material_data = {
                    "name": characteristics["displayName"],
                    "coverage": {
                        "perUnit": round(1 / characteristics["unitsPerM2"], 2),
                        "total": round(area, 2)
                    },
                    "quantity": quantity,
                    "unit": characteristics["unit"],
                    "costs": {
                        "perUnit": round(characteristics["baseCost"], 2),
                        "total": round(material_cost, 2)
                    }
                }
                
                surface_cost["materials"].append(material_data)
                surface_cost["totalCost"] = material_cost
                costs["materials"].append({
                    "name": characteristics["displayName"],
                    "quantity": quantity,
                    "unit": characteristics["unit"],
                    "cost": material_cost
                })

            costs["breakdown"]["surfaces"].append(surface_cost)
            costs["breakdown"]["materialsCost"] += surface_cost["totalCost"]
            costs["breakdown"]["laborCost"] = round(costs["breakdown"]["materialsCost"] * LABOR_COST_PERCENTAGE, 2)
            costs["breakdown"]["totalCost"] = costs["breakdown"]["materialsCost"] + costs["breakdown"]["laborCost"]
            costs["total"] = costs["breakdown"]["totalCost"]

            return costs
            
        except Exception as e:
            self.logger.error(f"Error calculating costs: {str(e)}")
            return None