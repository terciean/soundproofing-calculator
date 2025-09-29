from typing import Dict, List, Optional
from dataclasses import dataclass
from functools import lru_cache
from .material_properties import get_material_characteristics
from .acoustic_calculator import get_acoustic_calculator

@dataclass
class AcousticProfile:
    stc_rating: int
    frequency_response: Dict[str, float]
    absorption_coefficient: float
    transmission_loss: Dict[str, float]

@dataclass
class SolutionProfile:
    name: str
    surface_type: str
    acoustic_profile: AcousticProfile
    material_requirements: List[str]
    installation_complexity: int
    compatibility_score: float

SOLUTION_PROFILES = {
    'walls': {},
    'ceilings': {},
    'floors': {}
}

@lru_cache(maxsize=128)
def get_solution_profile(solution_name: str, surface_type: str) -> Optional[SolutionProfile]:
    """Get cached solution profile or generate new one."""
    if solution_name in SOLUTION_PROFILES[surface_type]:
        return SOLUTION_PROFILES[surface_type][solution_name]
    
    calculator = get_acoustic_calculator()
    characteristics = get_material_characteristics(solution_name)
    
    if not calculator or not characteristics:
        return None
        
    acoustic_profile = AcousticProfile(
        stc_rating=characteristics.get('stc', 0),
        frequency_response=calculator.get_frequency_response(solution_name),
        absorption_coefficient=characteristics.get('absorption', 0.0),
        transmission_loss=calculator.get_transmission_loss(solution_name)
    )
    
    return SolutionProfile(
        name=solution_name,
        surface_type=surface_type,
        acoustic_profile=acoustic_profile,
        material_requirements=characteristics.get('materials', []),
        installation_complexity=characteristics.get('complexity', 1),
        compatibility_score=calculator.calculate_compatibility(solution_name)
    )

def initialize_profiles():
    """Initialize solution profiles from database."""
    from .database import get_solution_names
    
    for surface_type in ['walls', 'ceilings', 'floors']:
        solutions = get_solution_names(surface_type)
        for solution in solutions:
            profile = get_solution_profile(solution, surface_type)
            if profile:
                SOLUTION_PROFILES[surface_type][solution] = profile

# Initialize profiles when module is imported
initialize_profiles()