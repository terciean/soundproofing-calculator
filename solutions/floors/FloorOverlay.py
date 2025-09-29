from solutions.solution import BaseSolution
from typing import Dict, Any, List, Optional

class FloorOverlayStandard(BaseSolution):
    """Standard floor overlay solution."""
    
    CODE_NAME = "Floor Overlay (Standard)"
    
    def __init__(self, width: float, length: float):
        super().__init__(width, length)
        self.name = "Standard Floor Overlay"
        self.description = "A standard floor overlay solution"
        
    def calculate(self, room_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate implementation details based on room data."""
        return {
            "name": self.name,
            "description": self.description,
            "footage": self.width * self.length,
            "stc_rating": 58,
            "iic_rating": 52,
            "materials": []
        }

class FloorOverlaySP15(BaseSolution):
    """SP15 floor overlay solution."""
    
    CODE_NAME = "Floor Overlay (SP15 Soundboard Upgrade)"
    
    def __init__(self, width: float, length: float):
        super().__init__(width, length)
        self.name = "Floor Overlay with SP15"
        self.description = "A floor overlay solution with SP15 treatment"
        
    def calculate(self, room_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate implementation details based on room data."""
        return {
            "name": self.name,
            "description": self.description,
            "footage": self.width * self.length,
            "stc_rating": 65,
            "iic_rating": 57,
            "materials": []
        } 