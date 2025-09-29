"""
Material properties module for soundproofing solutions.
"""

from typing import Dict, List, Any, Optional
import time
from .logger import get_logger
from solutions.database import get_all_materials_from_db, get_solution_by_id

# Set up logging
logger = get_logger()

def get_material_properties(material_names: List[str] = None) -> Dict[str, Any]:
    """
    Get material properties from MongoDB using new utility.
    If material_names is None or empty, returns all available properties.
    """
    try:
        materials = get_all_materials_from_db()
        if not materials:
            logger.warning("No materials found in database")
            return {}
        all_properties = {}
        for material in materials:
            material_name = material.get('name')
            if material_name:
                properties = {
                    'density': material.get('density', 0),
                    'thickness': material.get('thickness', 0),
                    'stc_rating': material.get('stc_rating', 0),
                    'stc_improvement': material.get('stc_improvement', 0),
                    'acoustic_properties': material.get('acoustic_properties', {}),
                    'cost': material.get('cost', 0),
                    'description': material.get('description', ''),
                    'category': material.get('category', 'unknown')
                }
                all_properties[material_name] = properties
        if material_names is None or len(material_names) == 0:
            return all_properties
        properties = {}
        for name in material_names:
            if name in all_properties:
                properties[name] = all_properties[name]
            else:
                logger.debug(f"Requested material not found: {name}")
        return properties
    except Exception as e:
        logger.error(f"Error fetching material properties: {e}")
        return {}

def calculate_solution_stc(solution_name: str) -> Optional[int]:
    """Calculate total STC rating for a solution based on its materials using new loader."""
    try:
        solution = get_solution_by_id(solution_name)
        if not solution or 'materials' not in solution:
            logger.warning(f"Solution not found or has no materials: {solution_name}")
            return None
        material_names = []
        for material in solution['materials']:
            if isinstance(material, dict) and 'name' in material:
                material_names.append(material['name'])
            elif isinstance(material, str):
                material_names.append(material)
        material_properties = get_material_properties(material_names)
        total_stc = 0
        for material in solution['materials']:
            name = material['name'] if isinstance(material, dict) else material
            if name in material_properties:
                props = material_properties[name]
                if 'stc_rating' in props and props['stc_rating']:
                    total_stc += props['stc_rating']
                elif 'stc_improvement' in props and props['stc_improvement']:
                    total_stc += props['stc_improvement']
        return total_stc
    except Exception as e:
        logger.error(f"Error calculating STC for {solution_name}: {e}")
        return None

def get_material_frequency_response(material_name: str) -> Optional[Dict[str, float]]:
    """Get frequency response data for a material using new loader."""
    try:
        materials = get_all_materials_from_db()
        material = next((m for m in materials if m.get('name') == material_name), None)
        if not material or 'acoustic_properties' not in material:
            logger.warning(f"No acoustic properties found for material: {material_name}")
            return None
        acoustic_props = material['acoustic_properties']
        if 'frequency_response' in acoustic_props:
            return acoustic_props['frequency_response']
        return None
    except Exception as e:
        logger.error(f"Error getting frequency response for {material_name}: {e}")
        return None

def get_material_characteristics(material_name: str) -> Optional[Dict[str, Any]]:
    """Get all acoustic characteristics for a material using new loader."""
    try:
        materials = get_all_materials_from_db()
        material = next((m for m in materials if m.get('name') == material_name), None)
        if not material:
            return None
        characteristics = {
            'density': material.get('density', 0),
            'thickness': material.get('thickness', 0),
            'stc_rating': material.get('stc_rating', 0),
            'stc_improvement': material.get('stc_improvement', 0),
            'acoustic_properties': material.get('acoustic_properties', {}),
            'cost': material.get('cost', 0),
            'description': material.get('description', ''),
            'category': material.get('category', 'unknown')
        }
        return characteristics
    except Exception as e:
        logger.error(f"Error getting material characteristics for {material_name}: {e}")
        return None