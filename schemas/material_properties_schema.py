from typing import Dict, Optional
from pydantic import BaseModel, Field

class AbsorptionProperties(BaseModel):
    low: float
    mid: float
    high: float

class MaterialProperties(BaseModel):
    density: float
    thickness: float
    absorption: AbsorptionProperties
    damping: float
    decoupling: float
    stc_improvement: Optional[int] = None
    stc_rating: Optional[int] = None

class MaterialPropertiesCollection(BaseModel):
    acoustic_properties: Dict[str, MaterialProperties]

    class Config:
        json_schema_extra = {
            "example": {
                "acoustic_properties": {
                    "Genie Clip": {
                        "density": 0.5,
                        "thickness": 10,
                        "absorption": {
                            "low": 0.1,
                            "mid": 0.1,
                            "high": 0.1
                        },
                        "damping": 0.1,
                        "decoupling": 0.8,
                        "stc_improvement": 10
                    }
                }
            }
        } 