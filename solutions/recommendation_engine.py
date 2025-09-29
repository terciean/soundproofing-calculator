from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging
from solutions.solution_mapping_new import SolutionMapping
from solutions.cost_calculator import calculate_solution_costs
from solutions.cache_manager import get_cache_manager, CacheManager
from solutions.acoustic_calculator import get_acoustic_calculator
from solutions.database import get_db

from solutions.material_properties import get_material_properties
from solutions.solutions import get_solutions_manager
from solutions.config import SOLUTION_MAPPINGS, SOLUTION_DESCRIPTIONS
from solutions.logger import get_logger

# Set up logging
logger = get_logger()

# DEBUG: Log module load
logger.debug("recommendation_engine.py loaded")

# Get SOLUTION_TYPES from SolutionMapping class
SOLUTION_TYPES = SolutionMapping.SOLUTION_TYPES



class NoiseType(Enum):
    """Enum for different types of noise."""
    AIRBORNE = "airborne"
    IMPACT = "impact"
    STRUCTURAL = "structural"
    FLANKING = "flanking"
    REVERBERATION = "reverberation"
    UNKNOWN = "unknown"

@dataclass
class RoomProfile:
    """Data class for room profile information."""
    length: float = 10.0
    width: float = 10.0 
    height: float = 10.0
    room_type: Optional[str] = None
    surfaces: Optional[List[str]] = None
    blockages: Optional[Dict[str, List[Dict]]] = None
    surface_features: Optional[Dict[str, List[str]]] = None

    def __init__(self, length: float = 10.0, width: float = 10.0, height: float = 10.0, room_type: Optional[str] = None, dimensions: Optional[Dict[str, float]] = None, blockages: Optional[Dict[str, List[Dict]]] = None, surface_features: Optional[Dict[str, List[str]]] = None, surfaces: Optional[List[str]] = None, **kwargs):
        if dimensions is not None:
            self.length = dimensions.get('length', length)
            self.width = dimensions.get('width', width)
            self.height = dimensions.get('height', height)
        else:
            self.length = length
            self.width = width
            self.height = height
        self.room_type = room_type
        self.blockages = blockages if blockages is not None else {}
        self.surface_features = surface_features if surface_features is not None else {}
        self.surfaces = surfaces if surfaces is not None else ["walls", "ceiling", "floor"]
        self.__post_init__()

    @property
    def dimensions(self) -> Dict[str, float]:
        return {"length": self.length, "width": self.width, "height": self.height}

    def __post_init__(self):
        if not all(d > 0 for d in [self.length, self.width, self.height]):
            raise ValueError("All dimensions must be positive")
        valid_surfaces = ["walls", "ceiling", "floor"]
        if self.surfaces is not None:
            for s in self.surfaces:
                if s not in valid_surfaces:
                    raise ValueError(f"Invalid surface: {s}")
        if self.blockages is None:
            self.blockages = {}
        if self.surface_features is None:
            self.surface_features = {}

    def __getitem__(self, key):
        if key == 'length':
            return self.length
        elif key == 'width':
            return self.width
        elif key == 'height':
            return self.height
        elif key == 'room_type':
            return self.room_type
        elif key == 'dimensions':
            return self.dimensions
        else:
            raise KeyError(f"RoomProfile has no attribute '{key}'")

    def to_dict(self):
        return {
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'room_type': self.room_type,
            'dimensions': self.dimensions
        }

@dataclass
class RoomInputs:
    """Data class for room input parameters."""
    room_type: str
    noise_type: str
    noise_level: float
    room_dimensions: Dict[str, float]
    surface_areas: Dict[str, float]
    existing_construction: Dict[str, str]
    budget_constraints: Optional[Dict[str, float]] = None
    priority_surfaces: Optional[List[str]] = None
    special_requirements: Optional[List[str]] = None

@dataclass
class NoiseProfile:
    """Data class for noise profile information."""
    type: str
    intensity: int
    direction: List[str]
    time: Optional[List[str]] = None
    frequency: Optional[float] = None
    is_impact: bool = False

    def __post_init__(self):
        if self.type not in VALID_NOISE_TYPES:
            raise ValueError(f"Invalid noise type: {self.type}")
        if not 0 <= self.intensity <= 10:
            raise ValueError(f"Intensity must be between 0 and 10, got {self.intensity}")
        if not all(d in VALID_DIRECTIONS for d in self.direction):
            invalid_dirs = [d for d in self.direction if d not in VALID_DIRECTIONS]
            raise ValueError(f"Invalid directions: {invalid_dirs}")

    def __getitem__(self, key):
        if key == 'type':
            return self.type
        elif key == 'intensity':
            return self.intensity
        elif key == 'direction':
            return self.direction
        elif key == 'time':
            return self.time
        else:
            raise KeyError(f"NoiseProfile has no attribute '{key}'")

    def to_dict(self):
        return {
            'type': self.type,
            'intensity': self.intensity,
            'direction': self.direction,
            'time': self.time
        }

# Valid noise types and their characteristics
VALID_NOISE_TYPES = {
    "speech": {"frequency_range": [100, 8000], "peak_frequency": 1000},
    "music": {"frequency_range": [20, 20000], "peak_frequency": 500},
    "tv": {"frequency_range": [50, 15000], "peak_frequency": 800},
    "traffic": {"frequency_range": [30, 1000], "peak_frequency": 200},
    "impact": {"frequency_range": [100, 10000], "peak_frequency": 2000},
    "footsteps": {"frequency_range": [50, 5000], "peak_frequency": 1000},
    "machinery": {"frequency_range": [20, 10000], "peak_frequency": 500}
}

# Valid directions and their affected surfaces
VALID_DIRECTIONS = {
    "north": "walls",
    "south": "walls",
    "east": "walls",
    "west": "walls",
    "above": "ceiling",
    "below": "floor"
}

def get_noise_type_reasoning(noise_type: str) -> str:
    """Get the reasoning for a noise type."""
    reasonings = {
        'speech': 'Optimized for voice frequency ranges (100Hz-8kHz)',
        'music': 'Enhanced low frequency treatment for music and bass',
        'tv': 'Balanced treatment for mixed media frequencies',
        'traffic': 'Focus on low-mid frequency road noise reduction',
        'aircraft': 'Enhanced high frequency and impact noise treatment',
        'footsteps': 'Specialized impact noise reduction',
        'furniture': 'Impact noise and structural transmission reduction',
        'machinery': 'Vibration isolation and broadband noise treatment'
    }
    return reasonings.get(noise_type, 'General purpose noise reduction')

def rank_solutions(solutions: List[Dict], inputs: RoomInputs, noise_profile: NoiseProfile) -> List[Dict]:
    """Rank solutions based on acoustic effectiveness, cost, compatibility and room acoustics."""
    if not solutions or not inputs or not noise_profile:
        logger.error("Invalid input parameters for solution ranking")
        raise ValueError("Missing required parameters for solution ranking")

    ranked = []
    needed_reduction = inputs.noise_level
    try:
        solutions_manager = get_solutions_manager()
        acoustic_calculator = get_acoustic_calculator()
        if not solutions_manager or not acoustic_calculator:
            logger.error("Failed to initialize core components for solution ranking")
            raise RuntimeError("Core components initialization failed")
        
        # Get room profile for acoustic calculations
        room_profile = acoustic_calculator.get_room_profile(inputs.room_type) if inputs.room_type else None
        
        # Get noise profile characteristics
        noise_characteristics = acoustic_calculator.get_noise_profile(noise_profile.type)
    except RuntimeError as re:
        logger.error(f"Runtime error during initialization: {str(re)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error during initialization: {str(e)}")
        logger.debug(f"Error details: {e.__class__.__name__}, {str(e)}", exc_info=True)
        return []
    
    for solution in solutions:
        try:
            score = 0
            if isinstance(solution, dict):
                solution_data = solution
            else:
                # Get characteristics from solutions manager
                pass
            solution_data = solutions_manager.get_solution_characteristics(solution)
            
            if solution_data and acoustic_calculator:
                # Get acoustic profile and material properties
                solution_id = solution_data.get('solution_id', solution_data.get('solution', 'unknown'))
                dimensions = inputs.room_dimensions
                acoustic_profile = acoustic_calculator.calculate_properties(solution_id, dimensions)
                material_props = acoustic_calculator.calculate_material_properties(solution_data.get('materials', []))
                
                if acoustic_profile and material_props:
                    # Validate and score based on sound reduction needs (0-30 points)
                    stc_rating = material_props.get('stc', 0)
                    if not isinstance(stc_rating, (int, float)) or stc_rating < 0:
                        logger.warning(f"Invalid STC rating for solution {solution}: {stc_rating}")
                        continue
                    
                    if stc_rating > 0 and needed_reduction > 0:
                        reduction_score = min(30, (stc_rating / needed_reduction) * 30)
                        score += reduction_score
                    else:
                        logger.warning(f"Invalid reduction calculation parameters: STC={stc_rating}, needed={needed_reduction}")
                    
                    # Enhanced frequency response matching (0-25 points)
                    if noise_characteristics:
                        freq_response = material_props.get('frequency_response', {})
                        if freq_response:
                            # Calculate match for each critical band
                            band_scores = []
                            for band, range_ in noise_characteristics.critical_bands.items():
                                band_match = acoustic_calculator.calculate_frequency_match(
                                    freq_response,
                                    range_,
                                    weight=2.0 if band == 'mid' else 1.0  # Weight mid frequencies higher
                                )
                                band_scores.append(band_match)
                            
                            # Average the band scores
                            freq_match = sum(band_scores) / len(band_scores)
                            score += freq_match * 25
                    
                    # Score based on absorption and damping with room acoustics (0-25 points)
                    absorption = material_props.get('absorption', {})
                    damping = material_props.get('damping', 0)
                    
                    if absorption and damping and room_profile:
                        # Adjust absorption score based on room reflectivity
                        room_factor = 1 + (room_profile.reflectivity * 0.5)
                        absorption_score = (sum(absorption.values()) / len(absorption)) * room_factor * 15
                        
                        # Adjust damping score based on room resonance
                        resonance_factor = 1
                        if room_profile.resonance:
                            if any(freq in range(int(room_profile.resonance[0]), int(room_profile.resonance[1])) 
                                  for freq in noise_characteristics.typical_frequency):
                                resonance_factor = 1.5
                        damping_score = damping * 10 * resonance_factor
                        
                        score += min(25, absorption_score + damping_score)
                    
                    # Score based on budget if provided (0-10 points)
                    if inputs.budget_constraints and 'budget' in inputs.budget_constraints:
                        costs = calculate_solution_costs(solution_data, inputs)
                        if costs <= inputs.budget_constraints['budget']:
                            budget_score = ((inputs.budget_constraints['budget'] - costs) / 
                                          inputs.budget_constraints['budget']) * 10
                            score += budget_score
                    
                    # Score based on installation complexity and special requirements (0-10 points)
                    complexity_base = (10 - solution_data.get('installation_complexity', 5)) / 10 * 8
                    
                    # Adjust for special requirements
                    if inputs.special_requirements:
                        meets_requirements = all(req in solution_data.get('features', []) 
                                                for req in inputs.special_requirements)
                        if meets_requirements:
                            complexity_base += 2
                    
                    score += complexity_base
                    
                    ranked.append({
                        "solution": solution,
                        "score": round(score, 2),
                        "details": {
                            **(solution_data.to_dict() if hasattr(solution_data, 'to_dict') and not isinstance(solution_data, dict) else solution_data),
                            "acoustic_profile": acoustic_profile if isinstance(acoustic_profile, dict) else (acoustic_profile.__dict__ if hasattr(acoustic_profile, '__dict__') else None),
                            "frequency_match": round(freq_match * 100, 1) if 'freq_match' in locals() else 0,
                            "estimated_cost": costs if 'costs' in locals() else None,
                            "complexity_score": round(complexity_base, 1),
                            "room_acoustics": {
                                "reflectivity_factor": round(room_factor, 2) if 'room_factor' in locals() else 1.0,
                                "resonance_factor": round(resonance_factor, 2) if 'resonance_factor' in locals() else 1.0
                            }
                        }
                    })
        except ValueError as ve:
            logger.error(f"Validation error in solution {solution}: {str(ve)}")
            continue
        except TypeError as te:
            logger.error(f"Type error in solution {solution}: {str(te)}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error ranking solution {solution}: {str(e)}")
            logger.debug(f"Error details: {e.__class__.__name__}, {str(e)}", exc_info=True)
            continue
    
    return sorted(ranked, key=lambda x: x["score"], reverse=True)



class RecommendationEngine:
    def __init__(self, solutions_manager=None, db=None):
        self.logger = logging.getLogger(__name__)
        
        try:
            self.db = db if db is not None else get_db()
            if self.db is not None:
                self.logger.info("Successfully connected to MongoDB")
            else:
                self.logger.warning("Failed to connect to MongoDB")
        except Exception as e:
            self.logger.error(f"Error connecting to database: {e}")
            self.db = None
        
        self.logger.info("Initializing core components")
        
        # Initialize solutions manager
        if solutions_manager is not None:
            self.solutions_manager = solutions_manager
        else:
            self.solutions_manager = get_solutions_manager()
            if not self.solutions_manager:
                self.logger.error("Failed to initialize solutions manager")
                raise RuntimeError("Solutions manager initialization failed")
        
        # Initialize other components after solutions manager
        self.cache_manager = get_cache_manager()
        self.logger.info("Cache manager initialized")
        
        try:
            self.acoustic_calculator = get_acoustic_calculator()
            self.logger.info("Acoustic calculator initialized")
        except Exception as e:
            self.logger.error(f"Error initializing acoustic calculator: {e}")
            self.acoustic_calculator = None
            
        self.solution_mappings = SOLUTION_MAPPINGS
        self.solution_descriptions = SOLUTION_DESCRIPTIONS
        self.cache = CacheManager()
        self.solution_calculator = SolutionCalculator()
    def _get_materials(self):
        """Get materials from cache first, then database with validation and cache warming"""
        materials = []
        cache_key = "all_materials"
        cache_ttl = 3600 * 24  # 24 hour TTL
        
        # Try cache first with validation and TTL check
        if self.cache_manager:
            try:
                cache_data = self.cache_manager.get(cache_key)
                if cache_data and isinstance(cache_data, dict):
                    # Check if cache is still valid
                    if datetime.now().timestamp() < cache_data.get('expires_at', 0):
                        valid_materials = [m for m in cache_data.get('materials', []) if self._validate_material(m)]
                        if valid_materials:
                            self.logger.info(f"Using {len(valid_materials)} validated materials from cache")
                            # Update material-to-solutions mapping
                            solutions_manager = get_solutions_manager()
                            solutions_manager.cache_material_to_solutions_mapping()
                            return valid_materials
                    else:
                        self.logger.info("Cache expired, refreshing from database")
            except Exception as e:
                self.logger.warning(f"Error accessing materials from cache: {e}")
        
        # Try database with validation and cache warming
        if self.db is not None:
            try:
                if 'materials' in self.db.list_collection_names():
                    db_materials = list(self.db.materials.find({}, {'_id': 0}))
                    valid_materials = [m for m in db_materials if self._validate_material(m)]
                    
                    if valid_materials:
                        self.logger.info(f"Loaded {len(valid_materials)} validated materials from database")
                        
                        # Cache validated materials with metadata
                        if self.cache_manager:
                            try:
                                cache_data = {
                                    'materials': valid_materials,
                                    'created_at': datetime.now().timestamp(),
                                    'expires_at': datetime.now().timestamp() + cache_ttl,
                                    'version': '1.0'
                                }
                                self.cache_manager.set(cache_key, cache_data, cache_ttl)
                                self.logger.info("Cached validated materials with metadata")
                                
                                # Warm up related caches
                                self._warm_related_caches(valid_materials)
                                # Update material-to-solutions mapping
                                solutions_manager = get_solutions_manager()
                                solutions_manager.cache_material_to_solutions_mapping()
                            except Exception as e:
                                self.logger.warning(f"Error caching materials: {e}")
                        return valid_materials
                    else:
                        self.logger.warning("No valid materials found in database")
                else:
                    self.logger.warning("No materials collection found in database")
            except Exception as e:
                self.logger.warning(f"Failed to load materials from database: {e}")
        
        # Return empty list if no valid materials found
        self.logger.warning("No valid materials found in cache or database")
        return materials
        
    def _warm_related_caches(self, materials):
        """Warm up related caches for frequently accessed data"""
        try:
            # Warm up material properties cache
            for material in materials:
                props_key = f"material_props_{material['name']}"
                if not self.cache_manager.has(props_key):
                    props = get_material_properties(material['name'])
                    if props:
                        self.cache_manager.set(props_key, props, 3600 * 24)
            
            # Warm up acoustic profiles cache
            acoustic_calculator = get_acoustic_calculator()
            if acoustic_calculator:
                for material in materials:
                    profile_key = f"acoustic_profile_{material['name']}"
                    if not self.cache_manager.has(profile_key):
                        profile = acoustic_calculator.get_acoustic_profile(material['name'])
                        if profile:
                            self.cache_manager.set(profile_key, profile, 3600 * 24)
                            
            self.logger.info("Successfully warmed up related caches")
        except Exception as e:
            self.logger.warning(f"Error warming up caches: {e}")

    def _validate_material(self, material):
        """Validate material data structure"""
        if not isinstance(material, dict):
            return False
            
        required_fields = ['name', 'type', 'properties']
        if not all(field in material for field in required_fields):
            return False
            
        if not isinstance(material['properties'], dict):
            return False
            
        # Validate acoustic properties if present
        if 'acoustic' in material['properties']:
            acoustic = material['properties']['acoustic']
            if not isinstance(acoustic, dict):
                return False
            if 'stc' in acoustic and not isinstance(acoustic['stc'], (int, float)):
                return False
                
        return True
        
    def generate_recommendations(self, noise_profile_data: Dict, room_profile_data: Dict) -> Dict:
        """Generate recommendations for the given noise and room profile."""
        self.logger.info("Generating recommendations for noise profile: %s, room profile: %s", noise_profile_data, room_profile_data)

        try:
            # Convert input dictionaries to dataclass instances
            noise_profile = NoiseProfile(**noise_profile_data)
            room_profile = RoomProfile(**room_profile_data)

            # Generate cache key
            cache_key = self._generate_cache_key(noise_profile, room_profile)

            # Try cache first
            if self.cache_manager:
                cached_recommendations = self.cache_manager.get(cache_key)
                if cached_recommendations:
                    self.logger.info(f"Returning cached recommendations for {cache_key}")
                    return cached_recommendations

            # Validate profiles
            if not self._validate_profiles(noise_profile, room_profile):
                self.logger.error("Invalid noise or room profile provided.")
                return {
                    'primary': {},
                    'alternatives': [],
                    'reasoning': ["Invalid noise or room profile provided. Please check your inputs."]
                }

            all_solutions = self.solutions_manager.get_all_solutions()
            if not all_solutions:
                self.logger.warning("No solutions found in the system.")
                return {
                    'primary': {},
                    'alternatives': [],
                    'reasoning': ["No soundproofing solutions are currently available."]
                }

            affected_surfaces = self._get_affected_surfaces(noise_profile.direction)
            recommendations = {"primary": {}, "alternatives": [], "reasoning": []}

            # Prepare RoomInputs for ranking
            room_inputs = RoomInputs(
                room_type=room_profile.room_type,
                noise_type=noise_profile.type,
                noise_level=noise_profile.intensity,
                room_dimensions=room_profile.dimensions,
                surface_areas={}, # This needs to be calculated or passed from frontend
                existing_construction={}, # Not used in current context, but part of dataclass
            )

            for surface_type, is_affected in affected_surfaces.items():
                if is_affected:
                    surface_solutions = self.solutions_manager.get_solutions_by_type(surface_type)
                    if not surface_solutions:
                        self.logger.warning(f"No solutions found for surface type: {surface_type}")
                        continue

                    # Filter and rank solutions for the current surface
                    # The rank_solutions function expects a list of solution objects (or dicts)
                    # and will internally get their characteristics.
                    ranked_surface_solutions = rank_solutions(
                        surface_solutions,
                        room_inputs,
                        noise_profile
                    )

                    if ranked_surface_solutions:
                        # Primary recommendation: top 1-2 solutions
                        if surface_type == 'walls':
                            recommendations['primary'][surface_type] = ranked_surface_solutions[:2]
                            recommendations['alternatives'].extend(ranked_surface_solutions[2:])
                        else:
                            recommendations['primary'][surface_type] = ranked_surface_solutions[0]
                            recommendations['alternatives'].extend(ranked_surface_solutions[1:])
                    else:
                        self.logger.info(f"No suitable solutions found for {surface_type} based on ranking criteria.")
                        recommendations['primary'][surface_type] = None # Indicate no primary solution

            # Generate reasoning
            recommendations['reasoning'] = self._generate_reasoning(
                recommendations,
                noise_profile.to_dict(), # Pass dict for reasoning function
                room_profile
            )

            # Cache the results
            if self.cache_manager:
                self.cache_manager.set(cache_key, recommendations)
                self.logger.info(f"Cached recommendations for {cache_key}")

            return recommendations

        except ValueError as ve:
            self.logger.error(f"Validation error in generate_recommendations: {str(ve)}")
            return {
                'primary': {},
                'alternatives': [],
                'reasoning': [f"Input validation error: {str(ve)}"]
            }
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}", exc_info=True)
            return {
                'primary': {},
                'alternatives': [],
                'reasoning': [f"An unexpected error occurred: {str(e)}. Please try again."]
            }
        
    def get_recommendations(self, noise_profile, room_profile, target_wall=None):
        """Generate recommendations filtered for a specific wall direction if provided."""
        recommendations = self.generate_recommendations(noise_profile, room_profile)
        if target_wall:
            filtered = {}
            for key, value in recommendations.items():
                if key == 'walls' and isinstance(value, dict):
                    filtered['walls'] = {target_wall: value.get(target_wall)} if target_wall in value else {}
                elif key == 'costs' and isinstance(value, dict):
                    filtered['costs'] = {target_wall: value.get(target_wall)} if target_wall in value else {}
                else:
                    filtered[key] = value
            return filtered
        return recommendations
        
        
    def _validate_profiles(self, noise_profile: NoiseProfile, room_profile: RoomProfile) -> bool:
        """Validate noise and room profiles"""
        try:
            # Validate noise profile
            if not noise_profile or not isinstance(noise_profile, NoiseProfile):
                return False
            if not noise_profile.type or not noise_profile.intensity:
                return False

            # Validate room profile
            if not room_profile or not isinstance(room_profile, RoomProfile):
                return False
            if not all(dim > 0 for dim in [room_profile.length, room_profile.width, room_profile.height]):
                return False

            return True
        except Exception as e:
            self.logger.error(f"Error validating profiles: {e}")
            return False

    def _validate_recommendations(self, recommendations: Dict) -> bool:
        """Validate recommendation data structure"""
        try:
            if not isinstance(recommendations, dict):
                return False

            required_fields = ['solutions', 'reasoning']
            if not all(field in recommendations for field in required_fields):
                return False

            if not isinstance(recommendations['solutions'], list):
                return False

            # Validate each solution
            for solution in recommendations['solutions']:
                if not isinstance(solution, dict):
                    return False
                if not all(field in solution for field in ['name', 'type', 'effectiveness']):
                    return False

            return True
        except Exception as e:
            self.logger.error(f"Error validating recommendations: {e}")
            return False
                    
            # Get solutions for recommendation
            solutions = self._get_solutions_for_recommendation(noise_profile)
            
            # Generate recommendations
            recommendations = {
                'recommendations': {
                    'primary': {},
                    'alternatives': [],
                    'reasoning': []
                }
            }
            
            # Add primary recommendations
            for surface_type, surface_solutions in solutions.items():
                if surface_type == 'walls':
                    recommendations['recommendations']['primary']['walls'] = surface_solutions[:2]
                elif surface_type == 'ceiling':
                    recommendations['recommendations']['primary']['ceiling'] = surface_solutions[0]
                elif surface_type == 'floor':
                    recommendations['recommendations']['primary']['floor'] = surface_solutions[0]
                    
            # Add alternatives
            for surface_type, surface_solutions in solutions.items():
                if surface_type == 'walls':
                    recommendations['recommendations']['alternatives'].extend(surface_solutions[2:])
                elif surface_type in ['ceiling', 'floor']:
                    recommendations['recommendations']['alternatives'].extend(surface_solutions[1:])
                    
            # Add reasoning
            recommendations['recommendations']['reasoning'] = self._generate_reasoning(
                recommendations['recommendations'],
                noise_profile.to_dict(),
                room_profile
            )
            
            # Cache results
            if self.cache_manager:
                self.cache_manager.set(cache_key, recommendations)
                
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return {
                'recommendations': {
                    'primary': {},
                    'alternatives': [],
                    'reasoning': [f"Error generating recommendations: {e}"]
                }
            }
        
    def _generate_cache_key(self, noise: NoiseProfile, room: RoomProfile) -> str:
        """Generate a consistent cache key from noise and room profiles"""
        import hashlib
        import json
        
        # Convert profiles to dict
        noise_dict = {
            "type": noise.type,
            "intensity": noise.intensity,
            "direction": sorted(noise.direction),
            "time": sorted(noise.time) if noise.time else []
        }
        
        room_dict = {
            "dimensions": room.dimensions,
            "room_type": room.room_type
        }
        
        # Create a consistent string representation
        data_str = json.dumps({"noise": noise_dict, "room": room_dict}, sort_keys=True)
        
        # Generate hash
        return f"recommendations_{hashlib.md5(data_str.encode()).hexdigest()}"
        
    def _get_solutions_for_recommendation(self, noise_profile: NoiseProfile) -> Dict[str, List[Dict]]:
        """Get solutions for recommendation based on noise profile"""
        try:
            # Get all solutions
            all_solutions = self.solutions_manager.get_all_solutions()
            
            # Get affected surfaces
            affected_surfaces = self._get_affected_surfaces(noise_profile.direction)
            
            # Get solutions for each surface
            solutions = {}
            for surface_type, is_affected in affected_surfaces.items():
                if is_affected:
                    surface_solutions = self.solutions_manager.get_solutions_by_type(surface_type)
                    if surface_solutions:
                        solutions[surface_type] = surface_solutions
                    else:
                        solutions[surface_type] = []
                        self.logger.warning(f"No solutions found for {surface_type}")
                else:
                    solutions[surface_type] = []
                    
            return solutions
            
        except Exception as e:
            self.logger.error(f"Error getting solutions for recommendation: {e}")
            return {'wall': [], 'ceiling': [], 'floor': []}

    def _get_noise_characteristics(self, noise: NoiseProfile) -> Dict:
        """Get detailed characteristics for the noise type"""
        try:
            # Get base characteristics from valid noise types
            base_characteristics = VALID_NOISE_TYPES.get(noise.type, {
                'frequency_range': [100, 8000],
                'peak_frequency': 1000
            })
            
            # Get additional characteristics from acoustic calculator
            noise_profile = self.acoustic_calculator.get_noise_profile(noise.type)
            if noise_profile:
                base_characteristics.update({
                    'frequency_range': noise_profile.get('frequency_range', base_characteristics['frequency_range']),
                    'peak_frequency': noise_profile.get('peak_frequency', base_characteristics['peak_frequency']),
                    'characteristics': noise_profile.get('characteristics', [])
                })
                
            return {
                'type': noise.type,
                'intensity': noise.intensity,
                'frequency_range': base_characteristics['frequency_range'],
                'peak_frequency': base_characteristics['peak_frequency'],
                'characteristics': base_characteristics.get('characteristics', [])
            }
            
        except Exception as e:
            self.logger.error(f"Error getting noise characteristics: {str(e)}")
            return {
                'type': noise.type,
                'intensity': noise.intensity,
                'frequency_range': [100, 8000],
                'peak_frequency': 1000,
                'characteristics': []
            }

    def _get_affected_surfaces(self, directions: List[str]) -> Dict[str, bool]:
        """Get which surfaces are affected by noise directions"""
        affected = {
            'walls': False,
            'ceiling': False,
            'floor': False
        }
        
        for direction in directions:
            surface = VALID_DIRECTIONS.get(direction)
            if surface:
                affected[surface] = True
                
        return affected

    def _get_solution_for_noise(self, noise_type: str, intensity_level: str) -> Optional[str]:
        """Get solution ID based on noise type and intensity"""
        try:
            # Try to get solution from database if available
            if self.db is not None:
                try:
                    solution_doc = self.db['solutions'].find_one({
                        'noise_type': noise_type,
                        'intensity_level': intensity_level
                    })
                    if solution_doc:
                        return solution_doc.get('solution_id')
                except Exception as e:
                    self.logger.error(f"Error fetching solution from database: {e}")
            
            # No fallback - return None if no database solution found
            self.logger.warning(f"No solution found for {noise_type} noise at {intensity_level} intensity")
            return None
            
        except Exception as e:
            self.logger.error(f"Error in _get_solution_for_noise: {e}")
            return None
            
    def _get_alternative_solution(self, noise_type: str, intensity_level: str) -> Optional[str]:
        """Get alternative solution ID"""
        try:
            # Try to get solution from database if available
            if self.db is not None:
                try:
                    solution_doc = self.db['solutions'].find_one({
                        'noise_type': noise_type,
                        'intensity_level': intensity_level,
                        'is_alternative': True
                    })
                    if solution_doc:
                        return solution_doc.get('solution_id')
                except Exception as e:
                    self.logger.error(f"Error fetching alternative solution from database: {e}")
            
            # No fallback - return None if no database solution found
            self.logger.warning(f"No alternative solution found for {noise_type} noise at {intensity_level} intensity")
            return None
            
        except Exception as e:
            self.logger.error(f"Error in _get_alternative_solution: {e}")
            return None

    def _get_intensity_level(self, intensity: int) -> str:
        """Convert numeric intensity to level"""
        if intensity >= 7:
            return 'high'
        elif intensity >= 4:
            return 'medium'
        return 'low'

    def _get_affected_walls(self, directions: List[str]) -> List[str]:
        """Get walls affected by noise direction"""
        wall_mapping = {
            'north': 'south_wall',
            'south': 'north_wall',
            'east': 'west_wall',
            'west': 'east_wall'
        }
        return [wall_mapping.get(d) for d in directions if d in wall_mapping]

    def _get_solutions_with_characteristics(self) -> List[Dict]:
        """Get all solutions with their material characteristics from MongoDB"""
        try:
            solutions = []
            
            if self.db is None:
                self.logger.warning("Database connection not available, returning empty solutions")
                return []
            
            collections_map = {
                'wall': 'wallsolutions',
                'ceiling': 'ceilingsolutions',
                'floor': 'floorsolutions'
            }
            
            for solution_type, collection_name in collections_map.items():
                try:
                    collection = self.db[collection_name]
                    found_solutions = list(collection.find({}))
                    self.logger.info(f"Found {len(found_solutions)} {solution_type} solutions")
                    
                    for solution in found_solutions:
                        solution['type'] = solution_type
                        solution['materials'] = self._get_material_characteristics(solution.get('materials', []))
                        # Ensure required fields are present with sensible defaults
                        if 'effectiveness' not in solution or solution['effectiveness'] is None:
                            solution['effectiveness'] = 0.0
                        if 'score' not in solution or solution['score'] is None:
                            solution['score'] = 0.0
                        if 'materials' not in solution:
                            solution['materials'] = []
                        if self._validate_solution(solution):
                            solutions.append(solution)
                except Exception as e:
                    self.logger.warning(f"Error accessing {solution_type} solutions: {e}")
            
            if not solutions:
                self.logger.warning("No solutions found in database, returning empty list")
                return []
                
            return solutions
                
        except Exception as e:
            self.logger.error(f"Error in _get_solutions_with_characteristics: {e}")
            return []
            
    def _validate_solution(self, solution: Dict) -> bool:
        """
        Validate that a solution has all required fields and proper structure
        Returns True if valid, False otherwise
        """
        try:
            # Check for required fields
            required_fields = ['type', 'materials']
            
            # Handle MongoDB document format with 'solution' field (from schema)
            if 'solution' in solution and isinstance(solution['solution'], str):
                # If solution name is available, verify it's not empty
                if not solution['solution'].strip():
                    self.logger.warning(f"Solution has empty name: {solution}")
                    return False
            
            # Check for required fields
            for field in required_fields:
                if field not in solution:
                    self.logger.warning(f"Solution missing required field '{field}': {solution}")
                    return False
            
            # Ensure materials is a list with at least one item
            if not isinstance(solution.get('materials', []), list) or len(solution.get('materials', [])) == 0:
                self.logger.warning(f"Solution has no materials: {solution}")
                return False
                
            # If we have surface_type from MongoDB, map it to our 'type' field if needed
            if 'surface_type' in solution and 'type' not in solution:
                # Map MongoDB field to our internal format
                surface_map = {
                    'walls': 'wall',
                    'ceilings': 'ceiling',
                    'floors': 'floor'
                }
                solution['type'] = surface_map.get(solution['surface_type'], solution['surface_type'])
            
            # Ensure type is valid
            valid_types = ['wall', 'ceiling', 'floor']
            if solution.get('type') not in valid_types:
                self.logger.warning(f"Solution has invalid type '{solution.get('type')}': {solution}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating solution: {e}")
            return False
            
    def _get_material_characteristics(self, materials: List[Dict]) -> List[Dict]:
        """Enhance the materials with their characteristics"""
        
        # Handle case when no materials are provided
        if not materials or len(materials) == 0:
            return []
            
        try:
            material_props = get_material_properties()
            
            # Handle different MongoDB document formats
            enhanced_materials = []
            for material in materials:
                # Handle possible MongoDB BSON format where material might be a dict with 'name' key
                if isinstance(material, dict):
                    material_name = material.get('name', '')
                    
                    # If it's a complete material object with properties already
                    if 'stc' in material or 'density' in material:
                        enhanced_material = {**material}  # Create a copy
                    else:
                        # Find properties for this material
                        material_characteristics = material_props.get(material_name, {})
                        enhanced_material = {
                            **material,  # Keep original material data
                            **material_characteristics  # Add material properties
                        }
                        
                    # Ensure cost is a number
                    if 'cost' in enhanced_material and not isinstance(enhanced_material['cost'], (int, float)):
                        try:
                            # Handle $numberDouble or $numberInt format from MongoDB
                            if isinstance(enhanced_material['cost'], dict) and '$numberDouble' in enhanced_material['cost']:
                                enhanced_material['cost'] = float(enhanced_material['cost']['$numberDouble'])
                            elif isinstance(enhanced_material['cost'], dict) and '$numberInt' in enhanced_material['cost']:
                                enhanced_material['cost'] = int(enhanced_material['cost']['$numberInt'])
                            else:
                                # Try to convert string to float
                                enhanced_material['cost'] = float(str(enhanced_material['cost']).strip())
                        except (ValueError, TypeError):
                            enhanced_material['cost'] = 0.0
                            
                    # Ensure coverage is a number
                    if 'coverage' in enhanced_material and not isinstance(enhanced_material['coverage'], (int, float)):
                        try:
                            # Handle $numberDouble or $numberInt format from MongoDB
                            if isinstance(enhanced_material['coverage'], dict) and '$numberDouble' in enhanced_material['coverage']:
                                enhanced_material['coverage'] = float(enhanced_material['coverage']['$numberDouble'])
                            elif isinstance(enhanced_material['coverage'], dict) and '$numberInt' in enhanced_material['coverage']:
                                enhanced_material['coverage'] = int(enhanced_material['coverage']['$numberInt'])
                            else:
                                # Parse string coverage value (e.g., "4 " -> 4)
                                enhanced_material['coverage'] = float(str(enhanced_material['coverage']).strip())
                        except (ValueError, TypeError):
                            enhanced_material['coverage'] = 1.0
                            
                    enhanced_materials.append(enhanced_material)
                    
                # Handle case where material is just a string (material name)
                elif isinstance(material, str):
                    material_name = material
                    material_characteristics = material_props.get(material_name, {})
                    
                    enhanced_material = {
                        'name': material_name,
                        **material_characteristics
                    }
                    enhanced_materials.append(enhanced_material)
                    
            return enhanced_materials
            
        except Exception as e:
            self.logger.error(f"Error enhancing materials: {e}")
            return materials  # Return original materials if enhancement fails
            
    def _find_best_wall_solutions(self, solutions: List[Dict], noise: Dict, dimensions: Dict) -> List[Dict]:
        """Find best wall solutions based on material characteristics and noise profile"""
        wall_solutions = [s for s in solutions if s['type'] == 'wall']
        if not wall_solutions:
            return []
            
        # Score each solution based on material characteristics
        scored_solutions = []
        for solution in wall_solutions:
            score = self._score_solution(solution, noise, dimensions)
            if score > 0:
                scored_solutions.append((solution, score))
                
        # Sort by score
        scored_solutions.sort(key=lambda x: x[1], reverse=True)
        
        # Get top solutions
        top_solutions = []
        for solution, score in scored_solutions[:3]:  # Get top 3 solutions
            solution_data = {
                'solution': solution['solution'],
                'name': solution.get('displayName', solution['solution']),
                'description': solution.get('description', ''),
                'materials': solution['materials'],
                'score': score,
                'stc_rating': solution.get('stc_rating', 0),
                'effectiveness': self._calculate_effectiveness(solution, noise)
            }
            top_solutions.append(solution_data)
            
        return top_solutions
        
    def _find_best_ceiling_solution(self, solutions: List[Dict], noise: Dict, dimensions: Dict) -> Optional[Dict]:
        """Find best ceiling solution based on material characteristics and noise profile"""
        ceiling_solutions = [s for s in solutions if s['type'] == 'ceiling']
        if not ceiling_solutions:
            return None
            
        # Score each solution
        scored_solutions = []
        for solution in ceiling_solutions:
            score = self._score_solution(solution, noise, dimensions)
            if score > 0:
                scored_solutions.append((solution, score))
                
        # Sort by score
        scored_solutions.sort(key=lambda x: x[1], reverse=True)
        
        # Get top solution
        if scored_solutions:
            solution, score = scored_solutions[0]
            return {
                'solution': solution['solution'],
                'name': solution.get('displayName', solution['solution']),
                'description': solution.get('description', ''),
                'materials': solution['materials'],
                'score': score,
                'stc_rating': solution.get('stc_rating', 0),
                'effectiveness': self._calculate_effectiveness(solution, noise)
            }
            
        return None
        
    def _find_best_floor_solution(self, solutions: List[Dict], noise: Dict, dimensions: Dict) -> Optional[Dict]:
        """Find best floor solution based on material characteristics and noise profile"""
        floor_solutions = [s for s in solutions if s['type'] == 'floor']
        if not floor_solutions:
            return None
            
        # Score each solution
        scored_solutions = []
        for solution in floor_solutions:
            score = self._score_solution(solution, noise, dimensions)
            if score > 0:
                scored_solutions.append((solution, score))
                
        # Sort by score
        scored_solutions.sort(key=lambda x: x[1], reverse=True)
        
        # Get top solution
        if scored_solutions:
            solution, score = scored_solutions[0]
            return {
                'solution': solution['solution'],
                'name': solution.get('displayName', solution['solution']),
                'description': solution.get('description', ''),
                'materials': solution['materials'],
                'score': score,
                'stc_rating': solution.get('stc_rating', 0),
                'effectiveness': self._calculate_effectiveness(solution, noise)
            }
            
        return None
        
    def _score_solution(self, solution: Dict, noise: Dict, dimensions: Dict = None) -> float:
        """
        Score a solution based on material characteristics, noise profile, and room dimensions
        
        This uses a comprehensive scoring matrix with weighted factors:
        - Noise type compatibility (40%)
        - Frequency response match (25%)
        - Material properties (25%) 
        - Room dimension factors (10%)
        """
        try:
            # Initialize scoring components
            noise_compatibility_score = 0.0
            frequency_response_score = 0.0
            material_properties_score = 0.0
            room_dimensions_score = 0.0
            
            # Get material characteristics
            materials = solution.get('materials', [])
            if not materials:
                return 0.0
                
            # 1. NOISE TYPE COMPATIBILITY (40%)
            # Check if solution is suitable for this noise type
            suitable_noise_types = solution.get('suitable_noise_types', [])
            if noise['type'] in suitable_noise_types:
                noise_compatibility_score = 1.0
            else:
                # Check for partial matches - some solutions work well for multiple noise types
                if noise['type'] in ['music', 'machinery'] and any(t in suitable_noise_types for t in ['music', 'machinery']):
                    noise_compatibility_score = 0.8
                elif noise['type'] in ['speech', 'tv'] and any(t in suitable_noise_types for t in ['speech', 'tv']):
                    noise_compatibility_score = 0.8
                elif noise['type'] in ['impact', 'footsteps'] and any(t in suitable_noise_types for t in ['impact', 'footsteps']):
                    noise_compatibility_score = 0.8
                else:
                    noise_compatibility_score = 0.5  # Base score for general effectiveness
            
            # 2. FREQUENCY RESPONSE MATCH (25%)
            material_freq_scores = []
            for material in materials:
                characteristics = material.get('characteristics', {})
                if not characteristics:
                    continue
                    
                # Get frequency response
                freq_response = characteristics.get('frequency_response', {})
                if freq_response:
                    min_freq = freq_response.get('min', 0)
                    max_freq = freq_response.get('max', 0)
                    
                    # Perfect match - material handles the entire noise frequency range
                    if (min_freq <= noise['frequency_range'][0] and max_freq >= noise['frequency_range'][1]):
                        material_freq_scores.append(1.0)
                    # Good match - material handles the peak frequency of the noise
                    elif (min_freq <= noise['peak_frequency'] <= max_freq):
                        material_freq_scores.append(0.8)
                    # Partial match - material handles part of the noise frequency range
                    elif (min_freq <= noise['frequency_range'][0] <= max_freq or 
                          min_freq <= noise['frequency_range'][1] <= max_freq):
                        material_freq_scores.append(0.6)
                    # Poor match - material doesn't handle noise frequencies well
                    else:
                        material_freq_scores.append(0.3)
                        
            # Average the frequency response scores across materials
            if material_freq_scores:
                frequency_response_score = sum(material_freq_scores) / len(material_freq_scores)
            
            # 3. MATERIAL PROPERTIES SCORE (25%)
            material_property_scores = []
            for material in materials:
                characteristics = material.get('characteristics', {})
                if not characteristics:
                    continue
                    
                # Get material properties
                density = characteristics.get('density', 0)
                thickness = characteristics.get('thickness', 0)
                stc_contribution = characteristics.get('stc_contribution', 0)
                
                # Calculate material property score
                property_score = 0.0
                
                # Density factor - higher density is better for soundproofing
                if density > 0:
                    property_score += min(density / 2000.0, 1.0) * 0.4
                    
                # Thickness factor - thicker materials generally perform better
                if thickness > 0:
                    property_score += min(thickness / 100.0, 1.0) * 0.3
                    
                # STC contribution factor - higher contribution is better
                if stc_contribution > 0:
                    property_score += min(stc_contribution / 50.0, 1.0) * 0.3
                    
                material_property_scores.append(property_score)
                
            # Average the material property scores
            if material_property_scores:
                material_properties_score = sum(material_property_scores) / len(material_property_scores)
                
            # 4. ROOM DIMENSIONS SCORE (10%)
            if dimensions:
                # Calculate room volume
                volume = dimensions.get('length', 0) * dimensions.get('width', 0) * dimensions.get('height', 0)
                
                # Surface area of room
                surface_area = 2 * (
                    dimensions.get('length', 0) * dimensions.get('width', 0) +
                    dimensions.get('length', 0) * dimensions.get('height', 0) +
                    dimensions.get('width', 0) * dimensions.get('height', 0)
                )
                
                # Room proportions factor - rooms with ideal proportions (golden ratio) perform better acoustically
                length = dimensions.get('length', 0)
                width = dimensions.get('width', 0)
                height = dimensions.get('height', 0)
                
                # Calculate how close dimensions are to ideal ratios (e.g., 1:1.6:2.6)
                if length > 0 and width > 0 and height > 0:
                    # Normalize dimensions to height = 1
                    l_ratio = length / height
                    w_ratio = width / height
                    
                    # Ideal ratios are around 1.6 and 2.6 for length and width (when height = 1)
                    # Calculate how close we are to ideal ratios
                    ratio_factor = 1.0 - (abs(l_ratio - 1.6) / 3.0 + abs(w_ratio - 2.6) / 3.0) / 2.0
                    ratio_factor = max(0.0, ratio_factor)
                    
                    # Room size factor - different solutions work better in different sized rooms
                    size_factor = 0.0
                    if volume < 30:  # Small room (<30m³)
                        if solution.get('type') == 'wall' and "GenieClip" in solution.get('solution', ''):
                            size_factor = 0.8  # GenieClip good for small rooms
                        else:
                            size_factor = 0.6
                    elif volume < 100:  # Medium room (30-100m³)
                        size_factor = 0.9  # Most solutions work well
                    else:  # Large room (>100m³)
                        if solution.get('type') == 'ceiling' and "Independent" in solution.get('solution', ''):
                            size_factor = 0.9  # Independent ceilings good for large rooms
                        else:
                            size_factor = 0.7
                            
                    room_dimensions_score = (ratio_factor * 0.4) + (size_factor * 0.6)
                else:
                    room_dimensions_score = 0.5  # Default if dimensions are invalid
                    
            # Apply weights to each component for final score
            final_score = (
                noise_compatibility_score * 0.4 +
                frequency_response_score * 0.25 +
                material_properties_score * 0.25 +
                room_dimensions_score * 0.1
            )
            
            # Adjust for intensity - higher intensity noise may reduce effectiveness
            intensity_factor = noise.get('intensity', 5) / 10.0
            intensity_adjustment = 1.0 - (intensity_factor * 0.2)  # Reduce score by up to 20% for high intensity
            
            return final_score * intensity_adjustment
            
        except Exception as e:
            self.logger.error(f"Error calculating solution score: {e}")
            return 0.0
            
    def _calculate_effectiveness(self, solution: Dict, noise: Dict) -> float:
        """Calculate solution effectiveness based on material characteristics and noise profile"""
        try:
            effectiveness = 0.0
            
            # Get material characteristics
            materials = solution.get('materials', [])
            if not materials:
                return 0.0
                
            # Calculate base effectiveness from STC rating
            stc_rating = solution.get('stc_rating', 0)
            if stc_rating > 0:
                effectiveness += min(stc_rating / 100.0, 1.0) * 0.4
                
            # Calculate material effectiveness
            material_effectiveness = 0.0
            for material in materials:
                characteristics = material.get('characteristics', {})
                if not characteristics:
                    continue
                    
                # Check frequency response
                freq_response = characteristics.get('frequency_response', {})
                if freq_response:
                    min_freq = freq_response.get('min', 0)
                    max_freq = freq_response.get('max', 0)
                    peak_freq = freq_response.get('peak', 0)
                    
                    # Calculate frequency match
                    if (min_freq <= noise['peak_frequency'] <= max_freq):
                        material_effectiveness += 0.4
                    elif (min_freq <= noise['frequency_range'][0] <= max_freq or 
                          min_freq <= noise['frequency_range'][1] <= max_freq):
                        material_effectiveness += 0.2
                        
                # Check density and thickness
                density = characteristics.get('density', 0)
                thickness = characteristics.get('thickness', 0)
                if density > 0 and thickness > 0:
                    # Higher density and thickness generally better for soundproofing
                    material_effectiveness += min(density / 1000.0, 1.0) * 0.3
                    material_effectiveness += min(thickness / 50.0, 1.0) * 0.3
                    
            # Normalize material effectiveness
            material_effectiveness = min(material_effectiveness / len(materials), 1.0)
            effectiveness += material_effectiveness * 0.6
            
            # Adjust based on noise intensity
            intensity_factor = min(noise['intensity'] / 10.0, 1.0)
            effectiveness *= (1 - intensity_factor * 0.3)
            
            return effectiveness
            
        except Exception as e:
            self.logger.error(f"Error calculating effectiveness: {str(e)}")
            return 0.0
            
    def _generate_reasoning(self, recommendations: Dict, noise: Dict, room: RoomProfile) -> List[str]:
        """Generate reasoning for recommendations"""
        reasoning = []
        # Add noise type reasoning
        noise_type = noise.get('type', None)
        if noise_type:
            noise_reason = get_noise_type_reasoning(noise_type)
            reasoning.append(f"Noise type '{noise_type}': {noise_reason}")
        else:
            reasoning.append("Noise type not specified; using general noise reduction principles.")

        # Add surface-specific reasoning with more detail
        primary = recommendations.get('primary', {})
        for surface_type, solutions in primary.items():
            if isinstance(solutions, list):
                for solution in solutions:
                    solution_name = solution.get('solution', 'Unknown')
                    stc = solution.get('stc_rating') or solution.get('stc_improvement')
                    stc_str = f" (STC: {stc})" if stc else ""
                    mat_list = solution.get('materials', [])
                    mat_names = ', '.join([m['name'] if isinstance(m, dict) and 'name' in m else str(m) for m in mat_list])
                    reason = f"Selected '{solution_name}' for {surface_type}{stc_str} due to suitability for {noise_type} noise and room needs. Materials used: {mat_names}."
                    reasoning.append(reason)
            elif isinstance(solutions, dict):
                solution_name = solutions.get('solution', 'Unknown')
                stc = solutions.get('stc_rating') or solutions.get('stc_improvement')
                stc_str = f" (STC: {stc})" if stc else ""
                mat_list = solutions.get('materials', [])
                mat_names = ', '.join([m['name'] if isinstance(m, dict) and 'name' in m else str(m) for m in mat_list])
                reason = f"Selected '{solution_name}' for {surface_type}{stc_str} due to suitability for {noise_type} noise and room needs. Materials used: {mat_names}."
                reasoning.append(reason)
            else:
                reasoning.append(f"Selected solution for {surface_type} based on noise type and intensity.")

        # Add room-specific reasoning with more context
        if hasattr(room, 'room_type') and room.room_type:
            reasoning.append(f"Room type '{room.room_type}' considered in solution selection for optimal acoustic performance.")
        if hasattr(room, 'dimensions') and room.dimensions:
            dims = room.dimensions
            dims_str = ', '.join([f"{k}: {v}" for k, v in dims.items()])
            reasoning.append(f"Room dimensions ({dims_str}) influenced the choice of solutions to ensure adequate coverage and effectiveness.")
        if hasattr(room, 'special_requirements') and room.special_requirements:
            reasoning.append(f"Special room requirements: {room.special_requirements} were factored into the recommendations.")

        # If no meaningful reasoning generated, provide a default
        if not reasoning:
            reasoning.append("No specific reasoning could be generated for this recommendation.")
        return reasoning

def get_solutions_manager():
    """Lazy import to avoid circular dependency"""
    from solutions.solutions import get_solutions_manager
    return get_solutions_manager()