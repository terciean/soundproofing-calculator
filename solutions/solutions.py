"""Solution management module for soundproofing solutions."""

from typing import Dict, List, Optional, Any
from solutions.base_solution import BaseSolution   
from solutions.cache_manager import get_cache_manager

from solutions.logger import get_logger

logger = get_logger()

class SoundproofingSolutions:
    """Manages all soundproofing solution instances"""
    
    def __init__(self):
        self.solutions: Dict[str, BaseSolution] = {}
        self.db = None
        self.cache_manager = get_cache_manager()
        self._recommendation_engine = None
        
    def register_solution(self, solution_id: str, solution_instance: BaseSolution) -> None:
        """Register a solution instance"""
        self.solutions[solution_id] = solution_instance
        
    def get_solution(self, solution_id: str) -> Optional[BaseSolution]:
        """Get a solution instance by ID"""
        return self.solutions.get(solution_id)
        
    def get_all_solutions(self) -> Dict[str, BaseSolution]:
        """Get all registered solutions"""
        return self.solutions
        
    def get_solution_characteristics(self, solution_id: str) -> Optional[Dict[str, Any]]:
        """Get characteristics for a solution by ID
        
        Args:
            solution_id: The solution identifier
            
        Returns:
            Dictionary of solution characteristics or None if not found
        """
        try:
            # Get solution instance
            solution = self.get_solution(solution_id)
            if not solution:
                logger.warning(f"Solution not found for characteristics: {solution_id}")
                return None
                
            # Get characteristics from solution
            if hasattr(solution, 'get_characteristics'):
                return solution.get_characteristics()
            else:
                logger.warning(f"Solution {solution_id} has no get_characteristics method")
                return None
                
        except Exception as e:
            logger.error(f"Error getting solution characteristics for {solution_id}: {e}")
            return None
        
    def get_solution_types(self, surface_type=None) -> List[str]:
        """Get list of all solution types"""
        solution_types = set()
        for solution in self.solutions.values():
            if hasattr(solution, '_collection'):
                collection_name = solution._collection
                # If surface_type is specified, only include matching collections
                if surface_type is None or surface_type in collection_name:
                    solution_types.add(collection_name)
        return list(solution_types)
        
    def get_solutions_by_type(self, surface_type: str) -> List[Dict]:
        """Get solutions filtered by surface type using the cache manager.

        Args:
            surface_type: The surface type to filter by (wall, ceiling, floor)

        Returns:
            List of serializable solution dictionaries
        """
        # Normalize surface type
        normalized_type = surface_type.lower().rstrip('s')
        cache_key = f"{normalized_type}_solutions"

        # Get solutions from cache
        cached_solutions = self.cache_manager.get(cache_key)
        
        logger.info(f"[DEBUG] Solutions manager: Looking for cache key '{cache_key}'")
        logger.info(f"[DEBUG] Solutions manager: Found {len(cached_solutions) if cached_solutions else 0} solutions in cache")

        if cached_solutions:
            logger.info(f"Loaded {len(cached_solutions)} solutions for '{normalized_type}' from cache.")
            return cached_solutions
        else:
            logger.warning(f"No cached solutions found for '{normalized_type}'."
                             f"Consider running `_init_solution_caches`.")
            return []
        
    def generate_recommendations(self, noise_profile, room_profile):
        """Generate recommendations based on noise and room profiles
        
        This method delegates to the RecommendationEngine class to generate recommendations.
        
        Args:
            noise_profile: The noise profile containing type, intensity, and direction
            room_profile: The room profile containing dimensions and other properties
            
        Returns:
            Dict containing recommendations
        """
        # Import here to avoid circular imports
        from solutions.recommendation_engine import RecommendationEngine
        
        # Initialize recommendation engine if not already done
        if self._recommendation_engine is None:
            self._recommendation_engine = RecommendationEngine(solutions_manager=self, db=None)
            
        # Generate recommendations using the engine
        return self._recommendation_engine.generate_recommendations(noise_profile, room_profile)
        
    def load_solutions_from_db(self) -> None:
        """Load solutions from the cache"""
        logger.info("Loading solutions from cache...")
        
    def cache_material_to_solutions_mapping(self):
        """Build and cache a mapping from each material to all solutions that use it."""
        material_to_solutions = {}
        for solution_id, solution in self.solutions.items():
            if hasattr(solution, 'get_characteristics'):
                characteristics = solution.get_characteristics()
                materials = characteristics.get('materials', []) if characteristics else []
                for material in materials:
                    name = material.get('name')
                    if name:
                        if name not in material_to_solutions:
                            material_to_solutions[name] = []
                        material_to_solutions[name].append(solution_id)
        if self.cache_manager:
            self.cache_manager.set('material_to_solutions', material_to_solutions, 3600 * 24)
            logger.info(f"Cached material-to-solutions mapping with {len(material_to_solutions)} materials.")
        return material_to_solutions
    
    def register_solution_with_characteristics(self, solution_id: str, solution_instance: BaseSolution) -> None:
        """Register a solution instance and ensure it has characteristics cached"""
        try:
            # Register the solution
            self.register_solution(solution_id, solution_instance)
            
            # Ensure characteristics are available
            if hasattr(solution_instance, 'get_characteristics'):
                characteristics = solution_instance.get_characteristics()
                if characteristics:
                    logger.info(f"Registered solution {solution_id} with characteristics")
                else:
                    logger.warning(f"Solution {solution_id} has no characteristics")
            else:
                logger.warning(f"Solution {solution_id} has no get_characteristics method")
                
        except Exception as e:
            logger.error(f"Error registering solution {solution_id}: {e}")
    
    def get_solution_characteristics_by_type(self, surface_type: str) -> List[Dict[str, Any]]:
        """Get solution characteristics filtered by surface type"""
        solutions = self.get_solutions_by_type(surface_type)
        characteristics = []
        
        for solution in solutions:
            if isinstance(solution, dict) and 'solution_id' in solution:
                # Solution is already in characteristic format
                characteristics.append(solution)
            else:
                # Get characteristics from solution instance
                if hasattr(solution, 'get_characteristics'):
                    char = solution.get_characteristics()
                    if char:
                        characteristics.append(char)
        
        return characteristics

# Global solutions manager instance
_solutions_manager = None

def get_solutions_manager() -> SoundproofingSolutions:
    """Get the global solutions manager instance"""
    global _solutions_manager
    if _solutions_manager is None:
        _solutions_manager = SoundproofingSolutions()
        _solutions_manager.load_solutions_from_db()
    return _solutions_manager