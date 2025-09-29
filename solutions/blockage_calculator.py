"""
Blockage calculator module for calculating blockage areas and summaries.
"""

import logging
from typing import Dict, Any, List

# Set up logging
logger = logging.getLogger(__name__)

def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert a value to float.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        float: Converted value or default
    """
    try:
        if value is None:
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def calculate_blockage_area(blockage: Dict[str, Any], surface: str) -> float:
    """
    Calculate the area of a single blockage.
    
    Args:
        blockage: Dictionary containing blockage details
        surface: Surface type (wall, floor, ceiling)
        
    Returns:
        float: Area in square meters
    """
    try:
        if surface == 'wall':
            width = safe_float(blockage.get('width'))
            height = safe_float(blockage.get('height'))
            return width * height
        else:
            width = safe_float(blockage.get('width'))
            length = safe_float(blockage.get('length'))
            return width * length
    except Exception as e:
        logger.error(f"Error calculating blockage area: {e}")
        return 0.0

def calculate_blockage_summary(surface: str, blockages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate summary of blockages for a surface.
    
    Args:
        surface: Surface type (wall, floor, ceiling)
        blockages: List of blockage dictionaries
        
    Returns:
        Dict containing total count and area
    """
    try:
        if not isinstance(blockages, list):
            logger.error(f"Invalid blockages format: {blockages}")
            return {
                'totalCount': 0,
                'totalArea': 0.0
            }
            
        total_area = 0.0
        total_count = len(blockages)
        
        for blockage in blockages:
            if not isinstance(blockage, dict):
                logger.warning(f"Invalid blockage format: {blockage}")
                continue
                
            # Extract only the fields needed for area calculation
            area_data = {
                'width': blockage.get('width'),
                'height': blockage.get('height'),
                'length': blockage.get('length')
            }
            
            area = calculate_blockage_area(area_data, surface)
            total_area += area
            
        return {
            'totalCount': total_count,
            'totalArea': total_area
        }
    except Exception as e:
        logger.error(f"Error calculating blockage summary: {e}")
        return {
            'totalCount': 0,
            'totalArea': 0.0
        } 