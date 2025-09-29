"""
Centralized configuration for the soundproofing system.
Contains all static data, constants, solution profiles, and noise characteristics.
"""

from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from functools import lru_cache
import json
import math
from .material_properties import get_material_characteristics
from .acoustic_calculator import get_acoustic_calculator


# ========== NOISE PROFILES ==========

# Comprehensive noise profiles with detailed characteristics
NOISE_PROFILES = {
    "speech": {
        "typical_frequency": [500, 2000],
        "is_impact": False,
        "typical_intensity": 4,
        "description": "Human speech and conversation",
        "intensity_range": [1, 4],
        "critical_bands": {
            "low": [85, 175],
            "mid": [175, 255],
            "high": [255, 350]
        }
    },
    "music": {
        "typical_frequency": [20, 20000],
        "is_impact": False,
        "typical_intensity": 6,
        "description": "Music and entertainment systems",
        "intensity_range": [2, 5],
        "critical_bands": {
            "low": [20, 250],
            "mid": [250, 2000],
            "high": [2000, 20000]
        }
    },
    "traffic": {
        "typical_frequency": [30, 1000],
        "is_impact": False,
        "typical_intensity": 5,
        "description": "Road and transportation noise",
        "intensity_range": [2, 5],
        "critical_bands": {
            "low": [20, 63],
            "mid": [63, 125],
            "high": [125, 250]
        }
    },
    "machinery": {
        "typical_frequency": [20, 4000],
        "is_impact": True,
        "typical_intensity": 8,
        "description": "Heavy machinery and industrial equipment",
        "intensity_range": [3, 5],
        "critical_bands": {
            "low": [20, 300],
            "mid": [300, 2000],
            "high": [2000, 8000]
        }
    },
    "footsteps": {
        "typical_frequency": [63, 125],
        "description": "Impact noise from walking, running, or jumping",
        "intensity_range": [1, 5],
        "is_impact": True,
        "typical_intensity": 4,
        "critical_bands": {
            "low": [20, 125],
            "mid": [125, 250],
            "high": [250, 500]
        }
    },
    "tv": {
        "typical_frequency": [80, 12000],
        "description": "Television audio and entertainment systems",
        "intensity_range": [1, 4],
        "is_impact": False,
        "typical_intensity": 3,
        "critical_bands": {
            "low": [80, 300],
            "mid": [300, 3000],
            "high": [3000, 12000]
        }
    },
    "impact": {
        "typical_frequency": [125, 4000],
        "description": "Impact sounds like dropping objects or banging",
        "intensity_range": [2, 7],
        "is_impact": True,
        "typical_intensity": 6,
        "critical_bands": {
            "low": [125, 500],
            "mid": [500, 2000],
            "high": [2000, 4000]
        }
    },
    "industrial": {
        "typical_frequency": [20, 4000],
        "is_impact": True,
        "typical_intensity": 8,
        "description": "Heavy machinery and industrial equipment",
        "intensity_range": [5, 9],
        "critical_bands": {
            "low": [20, 300],
            "mid": [300, 2000],
            "high": [2000, 4000]
        }
    }
}

# ========== SOLUTION PROFILES ==========

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

# Solution profiles container
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

# ========== SOLUTION CATALOG ==========

# Complete solution catalog with material properties
SOLUTION_CATALOG = {
    'walls': {
        'standard': {
            'M20WallStandard': {
                'name': 'M20 Wall System',
                'description': 'Double-layer drywall with isolation mounting',
                'reduction_amount': '20-25dB',
                'best_for': ['music', 'voices', 'tv'],
                'solution_details': 'Cost-effective noise reduction',
                'installation_notes': 'Standard installation',
                'materials': [{
                    'name': 'Drywall',
                    'cost': 25,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.4,
                        'mass': 10,
                        'absorption': 0.3
                    }
                }]
            },
            'GenieClipWallStandard': {
                'name': 'Genie Clip Wall System',
                'description': 'Advanced wall isolation system',
                'reduction_amount': '25-30dB',
                'best_for': ['music', 'machinery', 'heavy impact'],
                'solution_details': 'Superior noise isolation',
                'installation_notes': 'Professional installation recommended',
                'materials': [{
                    'name': 'Genie Clips',
                    'cost': 65,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.8,
                        'mass': 3,
                        'absorption': 0.2
                    }
                }]
            },
            'ResilientBarWallStandard': {
                'name': 'Resilient Bar Wall System',
                'description': 'Effective decoupling using resilient bars',
                'reduction_amount': '20-25dB',
                'best_for': ['speech', 'tv'],
                'solution_details': 'Good general-purpose isolation',
                'installation_notes': 'Standard installation',
                'materials': [{
                    'name': 'Resilient Bars',
                    'cost': 35,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.6,
                        'mass': 5,
                        'absorption': 0.2
                    }
                }]
            }
        },
        'premium': {
            'M20WallSP15': {
                'name': 'M20 Wall System SP15',
                'description': 'Premium wall system with enhanced mass',
                'reduction_amount': '25-30dB',
                'best_for': ['music', 'heavy bass', 'machinery'],
                'solution_details': 'Enhanced sound isolation with SP15 layer',
                'installation_notes': 'Professional installation required',
                'materials': [{
                    'name': 'SP15 Soundboard',
                    'cost': 85,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.6,
                        'mass': 15,
                        'absorption': 0.5
                    }
                }]
            },
            'GenieClipWallSP15': {
                'name': 'Genie Clip SP15 Wall System',
                'description': 'Maximum performance clip system with SP15',
                'reduction_amount': '30-35dB',
                'best_for': ['music', 'machinery', 'heavy impact'],
                'solution_details': 'Best possible wall isolation',
                'installation_notes': 'Professional installation required',
                'materials': [{
                    'name': 'Genie Clips + SP15',
                    'cost': 110,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.9,
                        'mass': 18,
                        'absorption': 0.6
                    }
                }]
            },
            'ResilientBarWallSP15': {
                'name': 'Resilient Bar SP15 Wall System',
                'description': 'Enhanced bar system with SP15 upgrade',
                'reduction_amount': '25-30dB',
                'best_for': ['speech', 'music', 'tv'],
                'solution_details': 'Premium bar-based isolation',
                'installation_notes': 'Professional installation recommended',
                'materials': [{
                    'name': 'Premium Resilient Bars + SP15',
                    'cost': 75,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.7,
                        'mass': 16,
                        'absorption': 0.5
                    }
                }]
            }
        }
    },
    'ceiling': {
        'standard': {
            'ResilientBarCeilingStandard': {
                'name': 'Resilient Bar Ceiling System',
                'description': 'Basic ceiling isolation system',
                'reduction_amount': '20-25dB',
                'best_for': ['footsteps', 'voices'],
                'solution_details': 'Effective for basic ceiling isolation',
                'installation_notes': 'Standard installation',
                'materials': [{
                    'name': 'Resilient Bars',
                    'cost': 35,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.6,
                        'mass': 5,
                        'absorption': 0.2
                    }
                }]
            },
            'GenieClipCeilingStandard': {
                'name': 'Genie Clip Ceiling System',
                'description': 'Advanced ceiling isolation system',
                'reduction_amount': '25-30dB',
                'best_for': ['footsteps', 'music', 'impact'],
                'solution_details': 'Superior ceiling isolation',
                'installation_notes': 'Professional installation recommended',
                'materials': [{
                    'name': 'Ceiling Genie Clips',
                    'cost': 65,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.8,
                        'mass': 3,
                        'absorption': 0.2
                    }
                }]
            },
            'IndependentCeilingStandard': {
                'name': 'Independent Ceiling System',
                'description': 'Fully decoupled ceiling system',
                'reduction_amount': '30-35dB',
                'best_for': ['music', 'impact', 'machinery'],
                'solution_details': 'Maximum ceiling isolation',
                'installation_notes': 'Professional installation required',
                'materials': [{
                    'name': 'Independent Ceiling Framing',
                    'cost': 85,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.9,
                        'mass': 10,
                        'absorption': 0.3
                    }
                }]
            },
            'LB3GenieClipCeilingStandard': {
                'name': 'LB3 Genie Clip Ceiling System',
                'description': 'Premium ceiling isolation system',
                'reduction_amount': '25-30dB',
                'best_for': ['footsteps', 'music', 'impact'],
                'solution_details': 'Superior ceiling isolation',
                'installation_notes': 'Professional installation recommended',
                'materials': [{
                    'name': 'LB3 Ceiling Genie Clips',
                    'cost': 70,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.85,
                        'mass': 4,
                        'absorption': 0.25
                    }
                }]
            }
        },
        'premium': {
            'ResilientBarCeilingSP15': {
                'name': 'Resilient Bar SP15 Ceiling System',
                'description': 'Enhanced ceiling isolation system',
                'reduction_amount': '25-30dB',
                'best_for': ['heavy impact', 'music', 'machinery'],
                'solution_details': 'Premium ceiling isolation with SP15',
                'installation_notes': 'Professional installation recommended',
                'materials': [{
                    'name': 'Premium Resilient Bars',
                    'cost': 45,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.7,
                        'mass': 6,
                        'absorption': 0.3
                    }
                }]
            },
            'GenieClipCeilingSP15': {
                'name': 'Genie Clip SP15 Ceiling System',
                'description': 'Premium ceiling isolation system with SP15',
                'reduction_amount': '30-35dB',
                'best_for': ['heavy impact', 'music', 'machinery'],
                'solution_details': 'Superior ceiling isolation with SP15',
                'installation_notes': 'Professional installation required',
                'materials': [{
                    'name': 'Ceiling Genie Clips + SP15',
                    'cost': 95,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.85,
                        'mass': 18,
                        'absorption': 0.5
                    }
                }]
            },
            'IndependentCeilingSP15': {
                'name': 'Independent SP15 Ceiling System',
                'description': 'Fully decoupled ceiling system with SP15',
                'reduction_amount': '35-40dB',
                'best_for': ['heavy impact', 'music', 'machinery'],
                'solution_details': 'Maximum ceiling isolation with SP15',
                'installation_notes': 'Professional installation required',
                'materials': [{
                    'name': 'Independent Ceiling Framing + SP15',
                    'cost': 120,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.95,
                        'mass': 25,
                        'absorption': 0.6
                    }
                }]
            },
            'LB3GenieClipCeilingSP15': {
                'name': 'LB3 Genie Clip SP15 Ceiling System',
                'description': 'Premium ceiling isolation system with SP15',
                'reduction_amount': '30-35dB',
                'best_for': ['heavy impact', 'music', 'machinery'],
                'solution_details': 'Superior ceiling isolation with SP15',
                'installation_notes': 'Professional installation required',
                'materials': [{
                    'name': 'LB3 Ceiling Genie Clips + SP15',
                    'cost': 105,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.9,
                        'mass': 20,
                        'absorption': 0.55
                    }
                }]
            }
        }
    },
    'floors': {
        'standard': {
            'FloatingFloorStandard': {
                'name': 'Floating Floor System',
                'description': 'Basic floor isolation system',
                'reduction_amount': '20-25dB',
                'best_for': ['footsteps', 'impact'],
                'solution_details': 'Effective for basic floor isolation',
                'installation_notes': 'Standard installation',
                'materials': [{
                    'name': 'Isolation Underlay',
                    'cost': 25,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.6,
                        'mass': 5,
                        'absorption': 0.3
                    }
                }]
            }
        },
        'premium': {
            'IsolationMatFloor': {
                'name': 'Isolation Mat System',
                'description': 'Premium floor isolation system',
                'reduction_amount': '25-30dB',
                'best_for': ['heavy impact', 'music', 'machinery'],
                'solution_details': 'Superior floor isolation',
                'installation_notes': 'Professional installation recommended',
                'materials': [{
                    'name': 'Premium Isolation Mat',
                    'cost': 40,
                    'coverage': 100,
                    'unit': 'sqft',
                    'properties': {
                        'decoupling': 0.8,
                        'mass': 8,
                        'absorption': 0.4
                    }
                }]
            }
        }
    }
}

# ========== SOLUTION MAPPINGS ==========

# Solution mappings by noise type and performance tier
SOLUTION_MAPPINGS = {
    'wall': {
        'music': {
            'low': 'ResilientBarWallStandard',
            'medium': 'GenieClipWallStandard',
            'high': 'GenieClipWallSP15'
        },
        'speech': {
            'low': 'ResilientBarWallStandard',
            'medium': 'M20WallSP15',
            'high': 'GenieClipWallSP15'
        },
        'machinery': {
            'low': 'GenieClipWallStandard',
            'medium': 'GenieClipWallSP15',
            'high': 'GenieClipWallSP15'
        },
        'impact': {
            'low': 'M20WallStandard',
            'medium': 'GenieClipWallStandard',
            'high': 'GenieClipWallSP15'
        },
        'traffic': {
            'low': 'M20WallStandard',
            'medium': 'M20WallSP15',
            'high': 'GenieClipWallSP15'
        },
        'mixed': {
            'low': 'GenieClipWallStandard',
            'medium': 'GenieClipWallSP15',
            'high': 'GenieClipWallSP15'
        }
    },
    'ceiling': {
        'music': {
            'low': 'ResilientBarCeilingStandard',
            'medium': 'GenieClipCeilingStandard',
            'high': 'IndependentCeilingSP15'
        },
        'speech': {
            'low': 'ResilientBarCeilingStandard',
            'medium': 'ResilientBarCeilingSP15',
            'high': 'GenieClipCeilingSP15'
        },
        'machinery': {
            'low': 'GenieClipCeilingStandard',
            'medium': 'IndependentCeilingStandard',
            'high': 'IndependentCeilingSP15'
        },
        'impact': {
            'low': 'GenieClipCeilingStandard',
            'medium': 'LB3GenieClipCeilingStandard',
            'high': 'IndependentCeilingSP15'
        },
        'footsteps': {
            'low': 'ResilientBarCeilingStandard',
            'medium': 'GenieClipCeilingStandard',
            'high': 'LB3GenieClipCeilingSP15'
        }
    },
    'floor': {
        'music': {
            'low': 'FloatingFloorStandard',
            'medium': 'FloatingFloorStandard',
            'high': 'IsolationMatFloor'
        },
        'impact': {
            'low': 'FloatingFloorStandard',
            'medium': 'IsolationMatFloor',
            'high': 'IsolationMatFloor'
        },
        'footsteps': {
            'low': 'FloatingFloorStandard',
            'medium': 'FloatingFloorStandard',
            'high': 'IsolationMatFloor'
        },
        'machinery': {
            'low': 'FloatingFloorStandard',
            'medium': 'IsolationMatFloor',
            'high': 'IsolationMatFloor'
        }
    }
}

# ========== SOLUTION DESCRIPTIONS ==========

# Brief descriptions for solutions
SOLUTION_DESCRIPTIONS = {
    'M20WallStandard': 'Standard double-layer solution with excellent cost-effectiveness',
    'GenieClipWallStandard': 'Premium isolation using specialized clip system',
    'ResilientBarWallStandard': 'Effective decoupling using resilient bars',
    'M20WallSP15': 'Enhanced performance with SP15 sound board',
    'GenieClipWallSP15': 'Maximum performance clip system with SP15',
    'ResilientBarWallSP15': 'Enhanced bar system with SP15 upgrade',
    'ResilientBarCeilingStandard': 'Standard ceiling isolation system',
    'ResilientBarCeilingSP15': 'Enhanced ceiling system with SP15',
    'GenieClipCeilingStandard': 'Advanced ceiling isolation using clip system',
    'GenieClipCeilingSP15': 'Premium ceiling isolation with SP15 and clips',
    'IndependentCeilingStandard': 'Fully decoupled ceiling for maximum isolation',
    'IndependentCeilingSP15': 'Premium fully decoupled ceiling with SP15',
    'LB3GenieClipCeilingStandard': 'Specialized LB3 clip system for ceilings',
    'LB3GenieClipCeilingSP15': 'Premium LB3 clip system with SP15 for ceilings',
    'FloatingFloorStandard': 'Basic floating floor system for impact isolation',
    'IsolationMatFloor': 'Premium floor isolation with specialized mat'
}

# ========== ACOUSTIC PROPERTIES CLASS ==========

class AcousticProperties:
    """Holds core acoustic properties for solutions"""
    
    def __init__(self, sound_reduction: int, frequency_range: Tuple[int, int], impact_resistance: float):
        self.sound_reduction = sound_reduction
        self.frequency_range = frequency_range
        self.impact_resistance = impact_resistance
        
    def to_dict(self):
        return {
            'sound_reduction': self.sound_reduction,
            'frequency_range': self.frequency_range,
            'impact_resistance': self.impact_resistance
        }

# ========== SOLUTION PROFILE CLASS ==========

@dataclass(frozen=True)
class SolutionProfile:
    """Profile for a soundproofing solution with its characteristics"""
    
    name: str
    surface_type: str
    acoustic_properties: dict
    suitable_noise_types: list
    min_intensity: int
    max_intensity: int

# ========== SOLUTION PROFILES ==========

# Detailed technical profiles for specific solutions
SOLUTION_PROFILES = {
    "M20WallStandard": SolutionProfile(
        name="M20 Wall Treatment (Standard)",
        surface_type="wall",
        acoustic_properties=AcousticProperties(
            sound_reduction=45,
            frequency_range=(125, 4000),
            impact_resistance=0.7
        ).__dict__,
        suitable_noise_types=["speech", "music", "traffic"],
        min_intensity=3,
        max_intensity=7
    ),
    "GenieClipWallStandard": SolutionProfile(
        name="Genie Clip Wall Treatment (Standard)",
        surface_type="wall",
        acoustic_properties=AcousticProperties(
            sound_reduction=50,
            frequency_range=(63, 8000),
            impact_resistance=0.8
        ).__dict__,
        suitable_noise_types=["speech", "music", "traffic", "machinery"],
        min_intensity=4,
        max_intensity=8
    ),
    "ResilientBarCeilingStandard": SolutionProfile(
        name="Resilient Bar Ceiling Treatment (Standard)",
        surface_type="ceiling",
        acoustic_properties=AcousticProperties(
            sound_reduction=35,
            frequency_range=(250, 4000),
            impact_resistance=0.5
        ).__dict__,
        suitable_noise_types=["speech", "music"],
        min_intensity=2,
        max_intensity=6
    )
}

# ========== UTILITY FUNCTIONS ==========

@lru_cache(maxsize=64)
def get_solution_profile(solution_id: str) -> Optional[SolutionProfile]:
    """
    Retrieve a solution profile by its ID.
    
    Args:
        solution_id (str): The identifier for the solution
        
    Returns:
        SolutionProfile: The solution profile or None if not found
    """
    return SOLUTION_PROFILES.get(solution_id)

def get_noise_profile(noise_type: str) -> Optional[Dict]:
    """
    Retrieve a noise profile by its type.
    
    Args:
        noise_type (str): The type of noise
        
    Returns:
        dict: The noise profile or None if not found
    """
    return NOISE_PROFILES.get(noise_type)

def get_compatible_solutions(noise_type: str, intensity: int) -> List[str]:
    """
    Find solutions compatible with a given noise type and intensity.
    
    Args:
        noise_type (str): The type of noise
        intensity (int): The noise intensity level
        
    Returns:
        list: List of compatible solution IDs
    """
    compatible = []
    for solution_id, profile in SOLUTION_PROFILES.items():
        if (noise_type in profile.suitable_noise_types and
            profile.min_intensity <= intensity <= profile.max_intensity):
            compatible.append(solution_id)
    return compatible

def get_display_name(solution_id: str) -> str:
    """
    Get a display name for a solution ID.
    
    Args:
        solution_id (str): The solution identifier
        
    Returns:
        str: The display name or the original ID if not found
    """
    for surface_type in SOLUTION_CATALOG:
        for tier in SOLUTION_CATALOG[surface_type]:
            if solution_id in SOLUTION_CATALOG[surface_type][tier]:
                return SOLUTION_CATALOG[surface_type][tier][solution_id].get('name', solution_id)
    return solution_id

def get_solution_description(solution_id: str) -> str:
    """
    Get the description for a solution ID.
    
    Args:
        solution_id (str): The solution identifier
        
    Returns:
        str: The description or an empty string if not found
    """
    return SOLUTION_DESCRIPTIONS.get(solution_id, "")

def get_solution_mapping(noise_type: str, tier: str = 'medium') -> Optional[str]:
    """
    Get the recommended solution for a noise type and tier.
    
    Args:
        noise_type (str): The type of noise
        tier (str): Performance tier ('low', 'medium', 'high')
        
    Returns:
        str: The solution ID or None if not found
    """
    for surface_type in SOLUTION_MAPPINGS:
        if noise_type in SOLUTION_MAPPINGS[surface_type]:
            return SOLUTION_MAPPINGS[surface_type][noise_type].get(tier)
    return None

# Export constants for JavaScript (used by the frontend)
JS_CONSTANTS = {
    'SOLUTION_CATALOG': SOLUTION_CATALOG,
    'SOLUTION_MAPPINGS': SOLUTION_MAPPINGS,
    'SOLUTION_DESCRIPTIONS': SOLUTION_DESCRIPTIONS,
    'NOISE_PROFILES': NOISE_PROFILES
}

def get_js_constants() -> str:
    """
    Get constants as a JavaScript string for use in the frontend.
    
    Returns:
        str: JavaScript code defining constants
    """
    return f"const CONSTANTS = {json.dumps(JS_CONSTANTS, indent=2)};"

# ========== CONSTRUCTION CONSTANTS ==========

# Clip spacing constants used across multiple solution files
CLIP_SPACING = {
    'genie_clip': 0.6,  # 600mm spacing for Genie Clips
    'lb3_genie_clip': 0.6,  # 600mm spacing for LB3 Genie Clips
    'resilient_bar': 0.4,  # 400mm spacing for Resilient Bars
    'furring_channel': 0.5  # 500mm spacing for Furring Channels
}

# Cost calculation constants
LABOR_COST_PERCENTAGE = 0.4  # Labor cost is 40% of material cost

# Materials that always need 10% extra
WASTAGE_MATERIALS = [
    "12.5mm Sound Plasterboard",
    "SP15 Soundboard",
    "Rockwool RWA45 50mm",
    "Rockwool RW3 100mm",
    "Tecsound 50",
    "M20 Rubber wall panel"
]

# Materials that need special handling for spacing/coverage
SPECIAL_MATERIALS = {
    "Genie Clip": {"spacing": CLIP_SPACING['genie_clip'], "coverage": CLIP_SPACING['genie_clip']},
    "LB3 Genie Clip": {"spacing": CLIP_SPACING['lb3_genie_clip'], "coverage": CLIP_SPACING['lb3_genie_clip']},
    "Furring Channel": {"spacing": CLIP_SPACING['furring_channel'], "coverage": CLIP_SPACING['furring_channel']},
    "Resilient bar": {"spacing": CLIP_SPACING['resilient_bar'], "coverage": CLIP_SPACING['resilient_bar']},
    "Acoustic Sealant": {"perimeter_based": True},
    "Acoustic Mastic": {"perimeter_based": True},
    "Screws": {"min_quantity": 1}  # Minimum 1 box
}

# Default coverage per unit in m² if not specified in solution data
MATERIAL_COVERAGE = {
    "12.5mm Sound Plasterboard": 2.4,  # Each board covers 2.4m²
    "SP15 Soundboard": 2.4,  # Each board covers 2.4m²
    "Rockwool RWA45 50mm": 8.64,  # Each pack covers 8.64m²
    "Rockwool RW3 100mm": 5.76,  # Each pack covers 5.76m²
    "Genie Clip": 0.6,  # Each clip covers 0.6m
    "LB3 Genie Clip": 0.6,  # Each clip covers 0.6m
    "Screws": 30.0,  # One box covers 30m²
    "Floor protection": 30.0  # One unit covers 30m²
}

# ========== SOLUTION VARIANT MONGO IDS ========== 
# Centralized mapping of solution variant names to MongoDB document IDs (placeholders)
SOLUTION_VARIANT_MONGO_IDS = {
    'walls': {
        'GenieClipWallStandard': '671bae0fc10b2e4a14c90e31',
        'GenieClipWallSP15': '671baf56c10b2e4a14c90e37',
        'M20WallStandard': '671baf8ec10b2e4a14c90e42',
        'M20WallSP15': '671bae62c10b2e4a14c90e33',
        'IndependentWallStandard': '671baf8ec10b2e4a14c90e39',
        'IndependentWallSP15': '671baf8ec10b2e4a14c90e39',
        'ResilientBarWallStandard': '671baf8ec10b2e4a14c90e40',
        'ResilientBarWallSP15': '671bae62c10b2e4a14c90e33',
    },
    'ceilings': {
        'GenieClipCeilingStandard': '671baf8ec10b2e4a14c90e43',
        'GenieClipCeilingSP15': '671baf8ec10b2e4a14c90e44',
        'LB3GenieClipCeilingStandard': '671baf8ec10b2e4a14c90e45',  
        'LB3GenieClipCeilingSP15': '671baf8ec10b2e4a14c90e46',      
        'IndependentCeilingStandard': '671baf8ec10b2e4a14c90e47',
        'IndependentCeilingSP15': '671baf8ec10b2e4a14c90e48',
        'ResilientBarCeilingStandard': '671baf8ec10b2e4a14c90e49',
        'ResilientBarCeilingSP15': '671baf8ec10b2e4a14c90e50',
    }
}