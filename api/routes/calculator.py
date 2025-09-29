from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from solutions.solution_mapping_new import SolutionMapping
from solutions.walls.M20Wall import M20WallStandard
from solutions.walls.GenieClipWall import GenieClipWallStandard
from solutions.walls.Independentwall import IndependentWallStandard
from solutions.ceilings.resilientbarceiling import ResilientBarCeilingStandard
from solutions.ceilings.independentceiling import IndependentCeilingStandard

router = APIRouter()

class CalculationRequest(BaseModel):
    solution_name: str
    dimensions: Dict[str, float]

@router.post("/calculate")
async def calculate_solution(request: CalculationRequest):
    try:
        # Map frontend name to calculator class
        calculator_class = SolutionMapping.get_calculator(request.solution_name)
        if not calculator_class:
            raise HTTPException(status_code=404, message="Solution not found")
            
        # Initialize calculator with dimensions
        calculator = calculator_class(
            length=request.dimensions['length'],
            height=request.dimensions['height']
        )
        
        # Calculate results
        results = calculator.calculate()
        if not results:
            raise HTTPException(status_code=500, message="Calculation failed")
            
        return {
            "success": True,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 