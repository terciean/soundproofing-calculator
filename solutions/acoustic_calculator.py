"""
Acoustic Calculator for Soundproofing Recommendations

This module handles acoustic calculations including STC ratings, frequency analysis,
and room acoustic adjustments. It replaces the client-side acoustic-calculator.js
to provide more consistent and accurate calculations from the server.
"""

from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import math
import logging
import threading
from functools import lru_cache
import numpy as np
from solutions.material_properties import get_material_properties
from solutions.solution_calculator import get_solutions_manager
from solutions.cache_manager import get_cache_manager
from solutions.database import get_db
from solutions.logger import get_logger

logger = logging.getLogger(__name__)

@dataclass
class MaterialProperties:
    """Data class for material acoustic properties"""
    stc: float = 0.0
    density: float = 0.0
    thickness: float = 0.0
    absorption: Dict[str, float] = None
    damping: float = 0.0
    decoupling: float = 0.0
    
    def __post_init__(self):
        if self.absorption is None:
            self.absorption = {"low": 0.0, "mid": 0.0, "high": 0.0}

@dataclass
class NoiseProfile:
    """Data class for noise profiles"""
    typical_frequency: List[float]
    peak_frequency: float
    critical_bands: Dict[str, List[float]]
    description: str = ""

@dataclass
class RoomProfile:
    """Data class for room acoustic properties"""
    reflectivity: float = 0.5
    absorption: float = 0.5
    resonance: List[float] = None
    reverberation: float = 0.5
    
    def __post_init__(self):
        if self.resonance is None:
            self.resonance = [0.0, 0.0]

class AcousticCalculator:
    """
    Performs acoustic calculations for soundproofing solutions
    """
    def _calculate_material_properties(self, materials: List[Dict]) -> Dict:
        """Calculate combined material properties"""
        total_stc = 0.0
        total_density = 0.0
        total_thickness = 0.0
        total_absorption = {"low": 0.0, "mid": 0.0, "high": 0.0}
        total_damping = 0.0
        total_decoupling = 0.0
        total_coverage = 0.0
        
        for material in materials:
            material_name = material.get('name', '')
            coverage = float(material.get('coverage', 100))
            
            if not material_name:
                continue
                
            props = self.get_material_properties(material_name)
            
            # Weight properties by coverage
            total_stc += props.stc * coverage
            total_density += props.density * coverage
            total_thickness += props.thickness * coverage
            total_absorption["low"] += props.absorption["low"] * coverage
            total_absorption["mid"] += props.absorption["mid"] * coverage
            total_absorption["high"] += props.absorption["high"] * coverage
            total_damping += props.damping * coverage
            total_decoupling += props.decoupling * coverage
            total_coverage += coverage
        
        # Normalize by total coverage
        if total_coverage > 0:
            return {
                "stc": total_stc / total_coverage,
                "density": total_density / total_coverage,
                "thickness": total_thickness / total_coverage,
                "absorption": {
                    k: v / total_coverage for k, v in total_absorption.items()
                },
                "damping": total_damping / total_coverage,
                "decoupling": total_decoupling / total_coverage
            }
            
        return self._get_empty_properties()
    
    def __init__(self):
        """Initialize the acoustic calculator with empty data structures"""
        self.logger = get_logger()
        self.db = None
        self.cache_manager = get_cache_manager()
        self.solutions_manager = None
        
        # Initialize empty data structures
        self.material_properties = {}
        self.noise_profiles = {}
        self.room_profiles = {}
        self.logger.info("Acoustic calculator initialized with empty data structures")
    
    @lru_cache(maxsize=100)
    def get_material_properties(self, material_name: str) -> MaterialProperties:
        """Get material properties with caching"""
        try:
            # Try cache first
            if self.cache_manager is not None:
                cached = self.cache_manager.get(f"material_props_{material_name}")
                if cached:
                    return MaterialProperties(**cached)
            
            # Try database
            if self.db is not None:
                material = self.db.materials.find_one({"name": material_name})
                if material:
                    props = MaterialProperties(
                        stc=float(material.get("stc_rating", 0)),
                        density=float(material.get("density", 0)),
                        thickness=float(material.get("thickness", 0)),
                        absorption=material.get("absorption", {"low": 0, "mid": 0, "high": 0}),
                        damping=float(material.get("damping", 0)),
                        decoupling=float(material.get("decoupling", 0))
                    )
                    
                    # Cache the result
                    if self.cache_manager is not None:
                        self.cache_manager.set(f"material_props_{material_name}", props.__dict__)
                    
                    return props
            
            # Return empty properties if not found
            self.logger.warning(f"No material properties found for {material_name}")
            return MaterialProperties()
            
        except Exception as e:
            self.logger.error(f"Error getting material properties for {material_name}: {e}")
            return MaterialProperties()
    
    @lru_cache(maxsize=50)
    def get_noise_profile(self, noise_type: str) -> NoiseProfile:
        """Get noise profile with caching"""
        try:
            # Try cache first
            if self.cache_manager is not None:
                cached = self.cache_manager.get(f"noise_profile_{noise_type}")
                if cached:
                    return NoiseProfile(**cached)
            
            # Try database
            if self.db is not None:
                profile = self.db.noise.find_one({"type": "profile", "profile_id": noise_type})
                if profile:
                    return NoiseProfile(
                        typical_frequency=profile.get("typical_frequency", [100, 8000]),
                        peak_frequency=float(profile.get("peak_frequency", 1000)),
                        critical_bands=profile.get("critical_bands", {
                            "low": [100, 500],
                            "mid": [500, 2000],
                            "high": [2000, 8000]
                        }),
                        description=profile.get("description", "")
                    )
            
            # Return default noise profile if not found
            self.logger.warning(f"No noise profile found for {noise_type}")
            return NoiseProfile(
                typical_frequency=[100, 1000],
                peak_frequency=500,
                critical_bands={"low": [100, 250], "mid": [500, 1000], "high": [2000, 4000]},
                description=f"Default profile for {noise_type} noise"
            )
            
        except Exception as e:
            self.logger.error(f"Error getting noise profile for {noise_type}: {e}")
            return NoiseProfile(
                typical_frequency=[100, 8000],
                peak_frequency=1000,
                critical_bands={"low": [100, 500], "mid": [500, 2000], "high": [2000, 8000]}
            )
    
    @lru_cache(maxsize=50)
    def get_room_profile(self, room_type: str) -> RoomProfile:
        """Get room profile with caching"""
        try:
            # Try cache first
            if self.cache_manager is not None:
                cached = self.cache_manager.get(f"room_profile_{room_type}")
                if cached:
                    return RoomProfile(**cached)
            
            # Try database
            if self.db is not None:
                room = self.db.noise.find_one({"type": "room", "room_type": room_type})
                if room:
                    return RoomProfile(
                        reflectivity=float(room.get("reflectivity", 0.5)),
                        absorption=float(room.get("absorption", 0.5)),
                        resonance=room.get("resonance", [100, 200]),
                        reverberation=float(room.get("reverberation", 0.5))
                    )
            
            # Fall back to static data
            return self.room_profiles.get(room_type, RoomProfile())
            
        except Exception as e:
            self.logger.error(f"Error getting room profile for {room_type}: {e}")
            return RoomProfile()
    
    def calculate_material_properties(self, materials: List[Dict]) -> Dict:
        """Calculate combined material properties with caching"""
        if not materials:
            return self._get_empty_properties()
            
        # Create cache key
        cache_key = f"material_props_{'_'.join(sorted(m.get('name', '') for m in materials))}"
        
        # Try cache first
        if self.cache_manager:
            cached = self.cache_manager.get(cache_key)
            if cached:
                return cached
        
        # Calculate properties
        properties = self._calculate_material_properties(materials)
        
        # Cache result
        if self.cache_manager is not None:
            self.cache_manager.set(cache_key, properties)
        
        return properties
    
    def _calculate_material_properties(self, materials: List[Dict]) -> Dict:
        """Calculate combined material properties"""
        total_stc = 0.0
        total_density = 0.0
        total_thickness = 0.0
        total_absorption = {"low": 0.0, "mid": 0.0, "high": 0.0}
        total_damping = 0.0
        total_decoupling = 0.0
        total_coverage = 0.0
        
        for material in materials:
            material_name = material.get('name', '')
            coverage = float(material.get('coverage', 100))
            
            if not material_name:
                continue
                
            props = self.get_material_properties(material_name)
            
            # Weight properties by coverage
            total_stc += props.stc * coverage
            total_density += props.density * coverage
            total_thickness += props.thickness * coverage
            total_absorption["low"] += props.absorption["low"] * coverage
            total_absorption["mid"] += props.absorption["mid"] * coverage
            total_absorption["high"] += props.absorption["high"] * coverage
            total_damping += props.damping * coverage
            total_decoupling += props.decoupling * coverage
            total_coverage += coverage
        
        # Normalize by total coverage
        if total_coverage > 0:
            return {
                "stc": total_stc / total_coverage,
                "density": total_density / total_coverage,
                "thickness": total_thickness / total_coverage,
                "absorption": {
                    k: v / total_coverage for k, v in total_absorption.items()
                },
                "damping": total_damping / total_coverage,
                "decoupling": total_decoupling / total_coverage
            }
            
        return self._get_empty_properties()
    
    def estimate_stc_rating(self, solution_id: str, intensity: int) -> int:
        """Estimate STC rating for a solution with caching"""
        try:
            # Create cache key
            cache_key = f"stc_rating_{solution_id}_{intensity}"
            
            # Try cache first
            if self.cache_manager is not None:
                cached = self.cache_manager.get(cache_key)
                if cached:
                    return int(cached)
            
            # Calculate STC rating
            stc_rating = self._calculate_stc_rating(solution_id, intensity)
            
            # Cache result
            if self.cache_manager is not None:
                self.cache_manager.set(cache_key, stc_rating)
            
            return stc_rating
            
        except Exception as e:
            self.logger.error(f"Error estimating STC rating for {solution_id}: {e}")
            return 0
    
    def _calculate_stc_rating(self, solution_id: str, intensity: int) -> int:
        """Calculate STC rating based on solution and intensity"""
        try:
            # Get solution characteristics
            if self.solutions_manager is None:
                self.logger.warning(f"Solutions manager not available for STC calculation: {solution_id}")
                return 0
                
            # Get solution instance
            solution = self.solutions_manager.get_solution(solution_id)
            if not solution:
                self.logger.warning(f"Solution not found: {solution_id}")
                return 0
                
            # Get characteristics from solution
            characteristics = solution.get_characteristics() if hasattr(solution, 'get_characteristics') else None
            if not characteristics:
                self.logger.warning(f"No characteristics found for solution: {solution_id}")
                return 0
            
            # Get base STC rating
            base_stc = characteristics.get('stc_rating', 0)
            
            # Adjust for intensity
            intensity_factor = min(intensity / 10.0, 1.0)
            stc_adjustment = -5 * intensity_factor  # Reduce STC by up to 5 points for high intensity
            
            # Calculate final STC
            final_stc = max(0, min(100, base_stc + stc_adjustment))
            
            return int(final_stc)
            
        except Exception as e:
            self.logger.error(f"Error calculating STC rating for {solution_id}: {e}")
            return 0
    
    def _get_empty_properties(self) -> Dict:
        """Get empty material properties"""
        return {
            "stc": 0.0,
            "density": 0.0,
            "thickness": 0.0,
            "absorption": {"low": 0.0, "mid": 0.0, "high": 0.0},
            "damping": 0.0,
            "decoupling": 0.0
        }
    
    def calculate_surface_areas(self, dimensions: Dict) -> Dict:
        """Calculate surface areas with caching"""
        try:
            # Create cache key
            cache_key = f"surface_areas_{'_'.join(str(v) for v in dimensions.values())}"
            
            # Try cache first
            if self.cache_manager is not None:
                cached = self.cache_manager.get(cache_key)
                if cached:
                    return cached
            
            # Calculate areas
            length = float(dimensions.get('length', 0))
            width = float(dimensions.get('width', 0))
            height = float(dimensions.get('height', 0))
            
            areas = {
                "floor": length * width,
                "ceiling": length * width,
                "walls": 2 * (length + width) * height
            }
            
            # Cache result
            if self.cache_manager is not None:
                self.cache_manager.set(cache_key, areas)
            
            return areas
            
        except Exception as e:
            self.logger.error(f"Error calculating surface areas: {e}")
            return {"floor": 0.0, "ceiling": 0.0, "walls": 0.0}
    
    def adjust_for_room_acoustics(self, solution: Dict, room_type: str, noise_type: str) -> Dict:
        """Adjust solution for room acoustics with caching"""
        try:
            # Create cache key
            cache_key = f"room_adjustment_{solution.get('solution', '')}_{room_type}_{noise_type}"
            
            # Try cache first
            if self.cache_manager is not None:
                cached = self.cache_manager.get(cache_key)
                if cached:
                    return cached
            
            # Get profiles
            room_profile = self.get_room_profile(room_type)
            noise_profile = self.get_noise_profile(noise_type)
            
            # Calculate adjustments
            adjustments = self._calculate_room_adjustments(solution, room_profile, noise_profile)
            
            # Cache result
            if self.cache_manager is not None:
                self.cache_manager.set(cache_key, adjustments)
            
            return adjustments
            
        except Exception as e:
            self.logger.error(f"Error adjusting for room acoustics: {e}")
            return solution
    
    def _calculate_room_adjustments(self, solution: Dict, room: RoomProfile, noise: NoiseProfile) -> Dict:
        """Calculate room acoustic adjustments"""
        adjusted = solution.copy()
        
        # Adjust for room reflectivity
        reflectivity_factor = 1.0 - room.reflectivity
        adjusted["stc_rating"] *= reflectivity_factor
        
        # Adjust for room absorption
        absorption_factor = 1.0 + room.absorption
        adjusted["stc_rating"] *= absorption_factor
        
        # Check for resonance issues
        if self._is_resonance_issue(noise.peak_frequency, room.resonance):
            adjusted["stc_rating"] *= 0.9  # Reduce effectiveness by 10%
        
        # Adjust for reverberation
        reverb_factor = 1.0 - (room.reverberation * 0.5)
        adjusted["stc_rating"] *= reverb_factor
        
        return adjusted
    
    def _is_resonance_issue(self, noise_frequency: float, room_resonance: List[float]) -> bool:
        """Check if noise frequency matches room resonance"""
        if not room_resonance or len(room_resonance) != 2:
            return False
            
        return room_resonance[0] <= noise_frequency <= room_resonance[1]
        
    @lru_cache(maxsize=50)
    def get_frequency_response(self, solution_name: str) -> Dict[str, float]:
        """Get frequency response data for a solution with caching"""
        try:
            # Try cache first
            if self.cache_manager:
                cached = self.cache_manager.get(f"freq_response_{solution_name}")
                if cached:
                    return cached
            
            # Try to find solution in cached solutions
            solution_data = None
            for surface_type in ['wall', 'ceiling', 'floor']:
                cache_key_surface = f"{surface_type}_solutions"
                cached_solutions = self.cache_manager.get(cache_key_surface) if self.cache_manager else None
                if cached_solutions:
                    for cached_solution in cached_solutions:
                        if isinstance(cached_solution, dict) and cached_solution.get('solution_id') == solution_name:
                            solution_data = cached_solution
                            break
                    if solution_data:
                        break
            
            # Try database if not found in cache
            if not solution_data and self.db is not None:
                # Try to find in materials collection first
                material = self.db.materials.find_one({"name": solution_name})
                if material and "acoustic_properties" in material and "frequency_response" in material["acoustic_properties"]:
                    response = material["acoustic_properties"]["frequency_response"]
                    
                    # Cache the result
                    if self.cache_manager:
                        self.cache_manager.set(f"freq_response_{solution_name}", response)
                    
                    return response
                
                # Try to find in solutions collections
                for collection in ["wallsolutions", "ceilingsolutions", "floorsolutions"]:
                    solution = self.db[collection].find_one({"solution": solution_name})
                    if solution and "acoustic_properties" in solution and "frequency_response" in solution["acoustic_properties"]:
                        response = solution["acoustic_properties"]["frequency_response"]
                        
                        # Cache the result
                        if self.cache_manager:
                            self.cache_manager.set(f"freq_response_{solution_name}", response)
                        
                        return response
            
            # Generate realistic frequency response based on STC rating
            stc_rating = 0
            if solution_data:
                stc_rating = solution_data.get('stc_rating', 0)
            else:
                # Try to estimate STC rating
                stc_rating = self.estimate_stc_rating(solution_name, 5)
            
            # Generate frequency response based on STC
            # Higher STC = better response across all frequencies
            base_response = min(stc_rating / 100.0, 1.0)  # Normalize to 0-1
            response = {
                "125": base_response * 0.7,   # Lower response at low frequencies
                "250": base_response * 0.8,
                "500": base_response * 0.9,
                "1000": base_response,        # Best response at mid frequencies
                "2000": base_response * 0.95,
                "4000": base_response * 0.9   # Slightly lower at high frequencies
            }
            
            # Cache the result
            if self.cache_manager:
                self.cache_manager.set(f"freq_response_{solution_name}", response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error getting frequency response for {solution_name}: {e}")
            return {
                "125": 0.0,
                "250": 0.0,
                "500": 0.0,
                "1000": 0.0,
                "2000": 0.0,
                "4000": 0.0
            }
    
    @lru_cache(maxsize=50)
    def get_transmission_loss(self, solution_name: str) -> Dict[str, float]:
        """Get transmission loss data for a solution with caching"""
        try:
            # Try cache first
            if self.cache_manager:
                cached = self.cache_manager.get(f"trans_loss_{solution_name}")
                if cached:
                    return cached
            
            # Try to find solution in cached solutions
            solution_data = None
            for surface_type in ['wall', 'ceiling', 'floor']:
                cache_key_surface = f"{surface_type}_solutions"
                cached_solutions = self.cache_manager.get(cache_key_surface) if self.cache_manager else None
                if cached_solutions:
                    for cached_solution in cached_solutions:
                        if isinstance(cached_solution, dict) and cached_solution.get('solution_id') == solution_name:
                            solution_data = cached_solution
                            break
                    if solution_data:
                        break
            
            # Try database if not found in cache
            if not solution_data and self.db is not None:
                # Try to find in materials collection first
                material = self.db.materials.find_one({"name": solution_name})
                if material and "acoustic_properties" in material and "transmission_loss" in material["acoustic_properties"]:
                    trans_loss = material["acoustic_properties"]["transmission_loss"]
                    
                    # Cache the result
                    if self.cache_manager:
                        self.cache_manager.set(f"trans_loss_{solution_name}", trans_loss)
                    
                    return trans_loss
                
                # Try to find in solutions collections
                for collection in ["wallsolutions", "ceilingsolutions", "floorsolutions"]:
                    solution = self.db[collection].find_one({"solution": solution_name})
                    if solution and "acoustic_properties" in solution and "transmission_loss" in solution["acoustic_properties"]:
                        trans_loss = solution["acoustic_properties"]["transmission_loss"]
                        
                        # Cache the result
                        if self.cache_manager:
                            self.cache_manager.set(f"trans_loss_{solution_name}", trans_loss)
                        
                        return trans_loss
            
            # Generate realistic transmission loss based on STC rating
            stc_rating = 0
            if solution_data:
                stc_rating = solution_data.get('stc_rating', 0)
            else:
                # Try to estimate STC rating
                stc_rating = self.estimate_stc_rating(solution_name, 5)
            
            # Use the existing method to estimate transmission loss from STC
            trans_loss = self._estimate_transmission_loss_from_stc(stc_rating)
            
            # Cache the result
            if self.cache_manager:
                self.cache_manager.set(f"trans_loss_{solution_name}", trans_loss)
            
            return trans_loss
            
        except Exception as e:
            self.logger.error(f"Error getting transmission loss for {solution_name}: {e}")
            return {
                "125": 0.0,
                "250": 0.0,
                "500": 0.0,
                "1000": 0.0,
                "2000": 0.0,
                "4000": 0.0
            }
    
    def _estimate_transmission_loss_from_stc(self, stc: int) -> Dict[str, float]:
        """Estimate transmission loss values based on STC rating"""
        # Simple model: STC roughly equals TL at 500 Hz
        # TL increases ~5dB per octave above 500 Hz
        # TL decreases ~5dB per octave below 500 Hz
        # This is a standard acoustic engineering approximation
        base_tl = float(stc)
        return {
            "125": max(0, base_tl - 10),
            "250": max(0, base_tl - 5),
            "500": base_tl,
            "1000": base_tl + 5,
            "2000": base_tl + 10,
            "4000": base_tl + 15
        }
    
    @lru_cache(maxsize=50)
    def calculate_compatibility(self, solution_name: str, room_type: str = None, noise_type: str = None) -> float:
        """Calculate compatibility score for a solution with caching
        
        Args:
            solution_name: Name of the solution to evaluate
            room_type: Optional room type to check compatibility with
            noise_type: Optional noise type to check compatibility with
            
        Returns:
            float: Compatibility score between 0.0 and 1.0
        """
        try:
            # Create cache key based on parameters
            cache_key = f"compatibility_{solution_name}"
            if room_type:
                cache_key += f"_{room_type}"
            if noise_type:
                cache_key += f"_{noise_type}"
            
            # Try cache first
            if self.cache_manager:
                cached = self.cache_manager.get(cache_key)
                if cached is not None:
                    return float(cached)
            
            # If no room or noise type specified, try to get static compatibility from database
            if not room_type and not noise_type:
                if self.db is not None:
                    # Try to find in solutions collections
                    for collection in ["wallsolutions", "ceilingsolutions", "floorsolutions"]:
                        solution = self.db[collection].find_one({"solution": solution_name})
                        if solution and "compatibility" in solution:
                            compatibility = float(solution["compatibility"])
                            
                            # Cache the result
                            if self.cache_manager:
                                self.cache_manager.set(cache_key, compatibility)
                            
                            return compatibility
                
                # Return default compatibility score if not found
                self.logger.warning(f"No static compatibility data found for {solution_name}")
                return 0.8  # Default moderate compatibility
            
            # Calculate dynamic compatibility based on room and noise types
            compatibility = self._calculate_dynamic_compatibility(solution_name, room_type, noise_type)
            
            # Cache the result
            if self.cache_manager:
                self.cache_manager.set(cache_key, compatibility)
            
            return compatibility
            
        except Exception as e:
            self.logger.error(f"Error calculating compatibility for {solution_name}: {e}")
            return 0.8  # Default moderate compatibility
    
    def _calculate_dynamic_compatibility(self, solution_name: str, room_type: str, noise_type: str) -> float:
        """Calculate dynamic compatibility score based on solution, room, and noise characteristics"""
        try:
            # Get solution characteristics
            solution_data = None
            for collection in ["wallsolutions", "ceilingsolutions", "floorsolutions"]:
                if self.db is not None:
                    solution_data = self.db[collection].find_one({"solution": solution_name})
                    if solution_data:
                        break
            
            if not solution_data:
                self.logger.warning(f"No solution data found for {solution_name}")
                return 0.8  # Default moderate compatibility
            
            # Get room profile
            room_profile = self.get_room_profile(room_type) if room_type else None
            
            # Get noise profile
            noise_profile = self.get_noise_profile(noise_type) if noise_type else None
            
            # Base compatibility score
            compatibility = 0.8  # Start with moderate compatibility
            
            # Adjust for solution type vs. room type
            if room_profile and "surface_type" in solution_data:
                surface_type = solution_data["surface_type"]
                
                # Check if solution is appropriate for room's acoustic challenges
                if room_profile.reflectivity > 0.7 and surface_type == "walls":
                    compatibility += 0.1  # Wall treatments good for reflective rooms
                elif room_profile.reverberation > 0.7 and surface_type == "ceiling":
                    compatibility += 0.1  # Ceiling treatments good for reverberant rooms
                elif room_profile.resonance and surface_type == "floor":
                    compatibility += 0.1  # Floor treatments good for resonance issues
            
            # Adjust for solution vs. noise type
            if noise_profile and "acoustic_properties" in solution_data:
                acoustic_props = solution_data["acoustic_properties"]
                
                # Check if solution addresses the frequency range of the noise
                if "frequency_response" in acoustic_props:
                    freq_response = acoustic_props["frequency_response"]
                    
                    # Calculate how well solution addresses noise frequency range
                    if noise_profile.typical_frequency and len(noise_profile.typical_frequency) == 2:
                        low_freq, high_freq = noise_profile.typical_frequency
                        
                        # Check if solution has good response in noise frequency range
                        low_match = False
                        high_match = False
                        
                        for freq_str, response in freq_response.items():
                            freq = float(freq_str)
                            if low_freq <= freq <= high_freq and response > 0.5:
                                if freq < 500:
                                    low_match = True
                                else:
                                    high_match = True
                        
                        if low_match and high_match:
                            compatibility += 0.1  # Good frequency match
                        elif low_match or high_match:
                            compatibility += 0.05  # Partial frequency match
                
                # Check if solution addresses impact vs. airborne noise appropriately
                if "is_impact" in solution_data and noise_profile.description:
                    solution_impact = solution_data["is_impact"]
                    noise_impact = "impact" in noise_profile.description.lower()
                    
                    if solution_impact == noise_impact:
                        compatibility += 0.1  # Solution matches noise type
            
            # Ensure compatibility is within valid range
            compatibility = max(0.0, min(1.0, compatibility))
            
            return compatibility
            
        except Exception as e:
            self.logger.error(f"Error calculating dynamic compatibility: {e}")
            return 0.8  # Default moderate compatibility

    def calculate_properties(self, solution_id: str, dimensions: Dict) -> Dict:
        """Calculate acoustic properties for a solution
        Args:
            solution_id: The solution identifier
            dimensions: Room dimensions (length, width, height)
        Returns:
            Dictionary with acoustic properties
        """
        try:
            # Create cache key
            cache_key = f"acoustic_props_{solution_id}_{'_'.join(str(v) for v in dimensions.values())}"
            
            # Try cache first
            if self.cache_manager is not None:
                cached = self.cache_manager.get(cache_key)
                if cached:
                    return cached
            
            # Get solution data from solutions manager
            if self.solutions_manager is None:
                self.logger.warning(f"Solutions manager not available for properties calculation: {solution_id}")
                return self._get_empty_acoustic_properties()
            
            # Try to get solution from solutions manager
            solution = self.solutions_manager.get_solution(solution_id)
            solution_data = None
            
            if solution and hasattr(solution, '_solution_data') and solution._solution_data:
                solution_data = solution._solution_data
            elif solution and hasattr(solution, 'get_characteristics'):
                # Use characteristics if no _solution_data
                solution_data = solution.get_characteristics()
            else:
                # Try to find solution in cache by surface type
                for surface_type in ['wall', 'ceiling', 'floor']:
                    cache_key_surface = f"{surface_type}_solutions"
                    cached_solutions = self.cache_manager.get(cache_key_surface) if self.cache_manager else None
                    if cached_solutions:
                        for cached_solution in cached_solutions:
                            if isinstance(cached_solution, dict) and cached_solution.get('solution_id') == solution_id:
                                solution_data = cached_solution
                                break
                        if solution_data:
                            break
            
            if not solution_data:
                self.logger.warning(f"No solution data found for {solution_id}")
                return self._get_empty_acoustic_properties()
            
            # Calculate surface areas
            surface_areas = self.calculate_surface_areas(dimensions)
            
            # Get STC rating
            stc_rating = solution_data.get('stc_rating', 0)
            if not stc_rating and 'materials' in solution_data:
                # Calculate STC from materials
                materials = solution_data['materials']
                material_props = self.calculate_material_properties(materials)
                stc_rating = material_props.get('stc', 0)
            
            # Get frequency response
            frequency_response = self.get_frequency_response(solution_id)
            
            # Get transmission loss
            transmission_loss = self.get_transmission_loss(solution_id)
            
            # Compile properties
            properties = {
                "solution_id": solution_id,
                "stc_rating": stc_rating,
                "surface_areas": surface_areas,
                "frequency_response": frequency_response,
                "transmission_loss": transmission_loss,
                "materials": solution_data.get('materials', []),
                "thickness": solution_data.get('thickness', 0),
                "weight": solution_data.get('weight', 0)
            }
            
            # Cache result
            if self.cache_manager is not None:
                self.cache_manager.set(cache_key, properties)
            
            return properties
            
        except Exception as e:
            self.logger.error(f"Error calculating acoustic properties for {solution_id}: {e}")
            return self._get_empty_acoustic_properties()

    def _get_empty_acoustic_properties(self) -> Dict:
        """Get empty acoustic properties structure"""
        return {
            "solution_id": "",
            "stc_rating": 0,
            "surface_areas": {"floor": 0.0, "ceiling": 0.0, "walls": 0.0},
            "frequency_response": {
                "125": 0.0,
                "250": 0.0,
                "500": 0.0,
                "1000": 0.0,
                "2000": 0.0,
                "4000": 0.0
            },
            "transmission_loss": {
                "125": 0.0,
                "250": 0.0,
                "500": 0.0,
                "1000": 0.0,
                "2000": 0.0,
                "4000": 0.0
            },
            "materials": [],
            "thickness": 0,
            "weight": 0
        }
    
    def cleanup(self):
        """Cleanup resources and clear caches"""
        try:
            # Clear LRU cache
            if hasattr(self.get_material_properties, 'cache_clear'):
                self.get_material_properties.cache_clear()
            
            # Clear internal caches
            self.material_properties.clear()
            self.noise_profiles.clear()
            self.room_profiles.clear()
            
            self.logger.info("AcousticCalculator cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during AcousticCalculator cleanup: {e}")

# Thread safety lock for singleton creation
_acoustic_calculator_lock = threading.Lock()
_acoustic_calculator_instance = None

def get_acoustic_calculator():
    """Get singleton instance of AcousticCalculator with thread safety"""
    global _acoustic_calculator_instance
    
    if _acoustic_calculator_instance is None:
        with _acoustic_calculator_lock:
            # Double-check locking pattern
            if _acoustic_calculator_instance is None:
                _acoustic_calculator_instance = AcousticCalculator()
    return _acoustic_calculator_instance

def reset_acoustic_calculator():
    """Reset the singleton instance for testing purposes"""
    global _acoustic_calculator_instance
    with _acoustic_calculator_lock:
        if _acoustic_calculator_instance is not None:
            # Cleanup any resources if needed
            if hasattr(_acoustic_calculator_instance, 'cleanup'):
                _acoustic_calculator_instance.cleanup()
        _acoustic_calculator_instance = None

def cleanup_acoustic_calculator():
    """Cleanup the singleton instance and its resources"""
    global _acoustic_calculator_instance
    with _acoustic_calculator_lock:
        if _acoustic_calculator_instance is not None:
            try:
                # Clear caches
                if hasattr(_acoustic_calculator_instance, 'get_material_properties'):
                    _acoustic_calculator_instance.get_material_properties.cache_clear()
                # Cleanup any other resources
                if hasattr(_acoustic_calculator_instance, 'cleanup'):
                    _acoustic_calculator_instance.cleanup()
            except Exception as e:
                logger.error(f"Error during acoustic calculator cleanup: {e}")
            finally:
                _acoustic_calculator_instance = None