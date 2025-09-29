from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Material(BaseModel):
    name: str
    cost: float
    coverage: str  # Stored as string in MongoDB (e.g. "4 ", "0.25", "30")

class Solution(BaseModel):
    solution: str
    surface_type: str = Field(..., description="Plural form: 'walls' or 'ceilings'")
    materials: List[Material]
    total_cost: Optional[float] = None
    notes: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "solution": "Genie Clip wall (Standard)",
                "surface_type": "walls",
                "materials": [
                    {
                        "name": "Genie Clip",
                        "cost": 3.4,
                        "coverage": "4 "
                    }
                ],
                "total_cost": 159.55,
                "notes": ["2 layers of 12.5mm plasterboard for this system."]
            }
        }

class SolutionCharacteristics(BaseModel):
    type: str
    displayName: str
    description: str
    sound_reduction: float
    stc_rating: float
    frequencyRange: str
    baseCost: float
    unitsPerM2: float
    unit: str
    materials: List[Dict[str, Any]]

    class Config:
        json_schema_extra = {
            "example": {
                "type": "wall",
                "displayName": "Genie Clip Wall",
                "description": "High performance wall isolation system",
                "sound_reduction": 65.0,
                "stc_rating": 63,
                "frequencyRange": "100Hz-3000Hz",
                "baseCost": 50.0,
                "unitsPerM2": 1.0,
                "unit": "unit",
                "materials": [
                    {"name": "Genie Clip", "quantity": 4, "unit": "pieces"}
                ]
            }
        }