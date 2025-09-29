"""Base solution class for all soundproofing solutions."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from solutions.base_calculator import BaseCalculator
from solutions.cache_manager import get_cache_manager
import logging
from datetime import datetime

class BaseSolution(BaseCalculator):
    """Enhanced base class that maintains compatibility with existing solutions"""
    
    def __init__(self, length: float, height: float):
        super().__init__(length, height)
        self._solution_data = None
        self._material_properties = None
        self.plasterboard_layers = 2  # Default number of layers
        # Load data in constructor to ensure it's available
        try:
            self._solution_data = self._load_solution_data(self.CODE_NAME)
        except Exception as e:
            # Handle any errors loading solution data
            self.logger.warning(f"Error loading solution data for {self.CODE_NAME}: {e}")
            self._solution_data = None
        self._load_material_properties()

    def calculate_clip_spacing(self, dimensions: Optional[Dict] = None) -> Dict[str, Any]:
        """Calculate clip spacing and quantities for clip-based solutions"""
        try:
            from solutions.config import CLIP_SPACING
            clip_spacing = CLIP_SPACING.get(self.CODE_NAME.lower().replace(' ', '_'), 600)
            
            length = dimensions.get('width', self.length) if dimensions else self.length
            height = dimensions.get('height', self.height) if dimensions else self.height
            area = length * height
            
            # Calculate clips needed
            clips_per_sqm = 1 / (clip_spacing * clip_spacing / 1e6)  # Convert mm² to m²
            clips_needed = math.ceil(area * clips_per_sqm)
            extra_clips = math.ceil(clips_needed * 0.1)  # 10% extra
            
            return {
                'clip_spacing': clip_spacing,
                'clips_needed': clips_needed,
                'extra_clips': extra_clips,
                'area': area,
                'plasterboard_layers': self.plasterboard_layers
            }
        except Exception as e:
            self.logger.error(f"Error calculating clip spacing: {e}")
            return None
        
    @property
    @abstractmethod
    def CODE_NAME(self) -> str:
        """Unique identifier for the solution"""
        pass
        
    def _load_material_properties(self) -> None:
        """Load material properties from database with caching"""
        try:
            if not self._material_properties:
                # Try to get from cache first
                cache_key = f"{self.CODE_NAME}_material_properties"
                cached = self.cache_manager.get(cache_key)
                if cached:
                    self._material_properties = cached
                    self._update_cache_status('material_properties', True)
                    return
                    
                # If not in cache, load from database
                if self.db is not None:
                    try:
                        properties = self.db.materials.find_one({"solution": self.CODE_NAME})
                        if properties:
                            if '_id' in properties:
                                del properties['_id']
                            self._material_properties = properties
                            # Cache the result
                            self.cache_manager.set(cache_key, properties, 3600)  # Cache for 1 hour
                            self._update_cache_status('material_properties', True)
                            return
                    except Exception as e:
                        self.logger.warning(f"Error loading material properties: {e}")
                        
            # If we reach here, no data was found
            self._material_properties = {}
            self._update_cache_status('material_properties', False)
            
        except Exception as e:
            self.logger.error(f"Error in _load_material_properties: {e}")
            self._update_cache_status('material_properties', False)
            

    def _load_material_properties(self) -> Dict[str, Any]:
        """Load material properties directly from solution data"""
        if not self._material_properties:
            # Use existing solution data if available, otherwise load it with proper parameter
            if self._solution_data:
                solution_data = self._solution_data
            else:
                try:
                    solution_data = self._load_solution_data(self.CODE_NAME)
                except TypeError as e:
                    self.logger.warning(f"Error loading solution data for material properties: {e}")
                    solution_data = {'materials': []}
            
            self._material_properties = solution_data.get('materials', [])
            self._update_cache_status('material_properties', True)
        return self._material_properties
            
    def calculate(self, dimensions: Optional[Dict] = None, materials: Optional[List] = None) -> Dict[str, Any]:
        """Calculate solution properties with caching"""
        try:
            # Handle both direct dimensions and dict format
            length = dimensions.get('width', self.length) if dimensions else self.length
            height = dimensions.get('height', self.height) if dimensions else self.height
            
            # Create cache parameters
            cache_params = {
                'length': length,
                'height': height,
                'materials': sorted([m.get('name', '') for m in (materials or [])])
            }
            
            # Try to get from cache
            cache_key = f"{self.CODE_NAME}_calculation"
            cached = self.cache_manager.get(cache_key)
            if cached:
                self._update_cache_status('calculations', True)
                return cached
                
            # Calculate if not cached
            characteristics = self.get_characteristics()
            if not characteristics:
                self._update_cache_status('calculations', False)
                return None
                
            # Calculate area and costs
            area = length * height
            costs = super().calculate(materials or characteristics.get('materials', []))
            
            result = {
                'area': area,
                'costs': costs,
                'characteristics': characteristics
            }
            
            # Cache the result
            self.cache_manager.set(cache_key, result, 3600)  # Cache for 1 hour
            self._update_cache_status('calculations', True)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error calculating solution: {e}")
            self._update_cache_status('calculations', False)
            return None
            
    def get_characteristics(self) -> Dict[str, Any]:
        """Get solution characteristics with caching"""
        try:
            # Try to get from cache
            cache_key = f"{self.CODE_NAME}_characteristics"
            cached = self.cache_manager.get(cache_key)
            if cached:
                self._update_cache_status('characteristics', True)
                self.logger.info(f"[SOLUTION DATA] {self.CODE_NAME}: Characteristics loaded from CACHE")
                # Add source information if not present
                if '_source' not in cached:
                    cached['_source'] = 'cache'
                return cached
                
            # Load solution data if needed
            if not self._solution_data:
                try:
                    self._solution_data = self._load_solution_data(self.CODE_NAME)
                except TypeError as e:
                    self.logger.warning(f"Error loading solution data for characteristics: {e}")
                    self._solution_data = None
                
            if not self._solution_data:
                self._update_cache_status('characteristics', False)
                self.logger.warning(f"[SOLUTION DATA] {self.CODE_NAME}: No solution data available for characteristics")
                return {}
                
            # Create characteristics directly from solution data
            characteristics = {
                'type': self._solution_data.get('type', ''),
                'displayName': self._solution_data.get('displayName', self.CODE_NAME),
                'description': self._solution_data.get('description', ''),
                'sound_reduction': self._solution_data.get('sound_reduction', 0),
                'stc_rating': self._solution_data.get('stc_rating', 0),
                'frequencyRange': self._solution_data.get('frequencyRange', '100Hz-3000Hz'),
                'materials': self._solution_data.get('materials', []),
                '_source': self._solution_data.get('_source', 'unknown')
            }
                
            # Cache the result
            self.cache_manager.set(cache_key, characteristics, 3600)  # Cache for 1 hour
            self._update_cache_status('characteristics', True)
                
            # Log characteristics details
            self.logger.info(f"[SOLUTION DATA] {self.CODE_NAME} details: "
                           f"Source: {characteristics.get('_source', 'unknown')}, "
                           f"STC Rating: {characteristics.get('stc_rating', 'N/A')}, "
                           f"Sound Reduction: {characteristics.get('sound_reduction', 'N/A')}, "
                           f"Materials: {len(characteristics.get('materials', []))}")
            
            return characteristics
            
        except Exception as e:
            self.logger.error(f"Error getting characteristics: {e}")
            self._update_cache_status('characteristics', False)
            return {}

    def log_solution_details(self) -> None:
        """
        Log detailed information about this solution's data sources and caching status.
        This is useful for debugging and monitoring which solutions have data.
        """
        try:
            # Get cache status
            cache_status = self.get_cache_status()
            
            # Get solution data
            # Get solution data
            solution_data = self._load_solution_data(self.CODE_NAME)
            characteristics = self.get_characteristics()
            
            # Log header
            self.logger.info(f"[SOLUTION DATA] ==================== SOLUTION DETAILS: {self.CODE_NAME} ====================")
            
            # Log data source
            source = "UNKNOWN"
            if solution_data and '_source' in solution_data:
                source = solution_data['_source'].upper()
            elif characteristics and '_source' in characteristics:
                source = characteristics['_source'].upper()
            
            self.logger.info(f"[DATA SOURCE] {self.CODE_NAME}: {source}")
            
            # Log cache status details
            self.logger.info(f"[SOLUTION DATA] {self.CODE_NAME} Cache Status:")
            for key, status in cache_status.items():
                self.logger.info(f"[SOLUTION DATA]   {key}: {'CACHED' if status['cached'] else 'NOT CACHED'} "
                              f"(Last updated: {status['last_updated']})")
            
            # Log solution characteristics
            if characteristics:
                self.logger.info(f"[SOLUTION DATA] {self.CODE_NAME} Characteristics:")
                self.logger.info(f"[SOLUTION DATA]   Display Name: {characteristics.get('displayName', 'N/A')}")
                self.logger.info(f"[SOLUTION DATA]   Type: {characteristics.get('type', 'N/A')}")
                self.logger.info(f"[SOLUTION DATA]   STC Rating: {characteristics.get('stc_rating', 'N/A')}")
                self.logger.info(f"[SOLUTION DATA]   Sound Reduction: {characteristics.get('sound_reduction', 'N/A')}")
                self.logger.info(f"[SOLUTION DATA]   Frequency Range: {characteristics.get('frequencyRange', 'N/A')}")
                self.logger.info(f"[SOLUTION DATA]   Materials: {len(characteristics.get('materials', []))}")
                
                # Log materials details
                if characteristics.get('materials'):
                    self.logger.info(f"[SOLUTION DATA]   Materials details:")
                    for idx, material in enumerate(characteristics['materials']):
                        self.logger.info(f"[SOLUTION DATA]     Material #{idx+1}: {material.get('name', 'Unknown')} "
                                      f"- Cost: {material.get('baseCost', 'N/A')}, "
                                      f"Unit: {material.get('unit', 'N/A')}")
            else:
                self.logger.warning(f"[SOLUTION DATA] {self.CODE_NAME}: NO CHARACTERISTICS AVAILABLE")
            
            # Log footer
            self.logger.info(f"[SOLUTION DATA] =====================================================================")
            
        except Exception as e:
            self.logger.error(f"[SOLUTION DATA] Error logging solution details: {e}")