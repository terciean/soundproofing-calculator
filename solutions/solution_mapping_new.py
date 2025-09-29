class SolutionMapping:
    """Maps frontend solution names to database solution names"""
    
    SOLUTION_TYPES = {
        'wall': 'wallsolutions',
        'ceiling': 'ceilingsolutions',
        'floor': 'floorsolutions'
    }
    
    # Expanded solution mapping with all solutions
    SOLUTION_MAP = {
        # Wall solutions
        'Independent Wall (Standard)': 'IndependentWallStandard',
        'Independent Wall (SP15 Soundboard Upgrade)': 'IndependentWallSP15',
        'Resilient bar wall (Standard)': 'ResilientBarWallStandard',
        'Resilient bar wall (SP15 Soundboard Upgrade)': 'ResilientBarWallSP15',
        'Genie Clip wall (Standard)': 'GenieClipWallStandard',
        'Genie Clip wall (SP15 Soundboard Upgrade)': 'GenieClipWallSP15',
        'M20 Solution (Standard)': 'M20WallStandard',
        'M20 Solution (SP15 Soundboard upgrade)': 'M20WallSP15',
        # Ceiling solutions
        'Genie Clip ceiling': 'GenieClipCeilingStandard',
        'Genie Clip ceiling (SP15 Soundboard Upgrade)': 'GenieClipCeilingSP15',
        'LB3 Genie Clip': 'LB3GenieClipCeilingStandard',
        'LB3 Genie Clip (SP15 Soundboard Upgrade)': 'LB3GenieClipCeilingSP15',
        'Independent Ceiling': 'IndependentCeilingStandard',
        'Independent Ceiling (SP15 Soundboard Upgrade)': 'IndependentCeilingSP15',
        'Resilient Bar Ceiling': 'ResilientBarCeilingStandard',
        'Resilient Bar Ceiling with SP15 Soundboard': 'ResilientBarCeilingSP15',
        # Floor solutions
        'Floating Floor System': 'FloatingFloorStandard',
        'Isolation Mat System': 'IsolationMatFloor'
    }
    
    # Reverse mapping from code names to display names
    CODE_TO_DISPLAY = {v: k for k, v in SOLUTION_MAP.items()}



    @classmethod
    def get_db_name(cls, code_name):
        """Get database name for a frontend solution name"""
        return cls.SOLUTION_MAP.get(code_name)
        
    @classmethod
    def get_code_name(cls, db_name):
        """Get code name for a database solution name"""
        return cls.CODE_TO_DISPLAY.get(db_name)
        

            
    @classmethod
    def get_calculator(cls, solution_name: str, length: float = 0, height: float = 0):
        """Get solution calculator class for a solution name
        
        Args:
            solution_name: Name of the solution
            length: Length in meters
            height: Height in meters
            
        Returns:
            Instance of the calculator class or None if not found
        """
        # Import here to avoid circular imports
        try:
            from solutions.walls.M20Wall import M20WallStandard, M20WallSP15
            from solutions.walls.GenieClipWall import GenieClipWallStandard, GenieClipWallSP15
            from solutions.walls.resilientbarwall import ResilientBarWallStandard, ResilientBarWallSP15
            
            # Import ceiling solutions
            from solutions.ceilings.resilientbarceiling import ResilientBarCeilingStandard, ResilientBarCeilingSP15
            from solutions.ceilings.genieclipceiling import GenieClipCeilingStandard, GenieClipCeilingSP15
            from solutions.ceilings.independentceiling import IndependentCeilingStandard, IndependentCeilingSP15
            from solutions.ceilings.lb3genieclipceiling import LB3GenieClipCeilingStandard, LB3GenieClipCeilingSP15
            
            # Import floor solutions
            from solutions.floors.FloorSolutions import FloatingFloorStandard, IsolationMatFloor
            
            # Map solution names to calculator classes
            calculators = {
                # Wall solutions
                'M20WallStandard': M20WallStandard,
                'M20WallSP15': M20WallSP15,
                'GenieClipWallStandard': GenieClipWallStandard,
                'GenieClipWallSP15': GenieClipWallSP15,
                'ResilientBarWallStandard': ResilientBarWallStandard,
                'ResilientBarWallSP15': ResilientBarWallSP15,
                
                # Ceiling solutions
                'ResilientBarCeilingStandard': ResilientBarCeilingStandard,
                'ResilientBarCeilingSP15': ResilientBarCeilingSP15,
                'GenieClipCeilingStandard': GenieClipCeilingStandard,
                'GenieClipCeilingSP15': GenieClipCeilingSP15,
                'IndependentCeilingStandard': IndependentCeilingStandard,
                'IndependentCeilingSP15': IndependentCeilingSP15,
                'LB3GenieClipCeilingStandard': LB3GenieClipCeilingStandard,
                'LB3GenieClipCeilingSP15': LB3GenieClipCeilingSP15,
                
                # Floor solutions
                'FloatingFloorStandard': FloatingFloorStandard,
                'IsolationMatFloor': IsolationMatFloor
            }
            
            # Get the calculator class
            calculator_class = calculators.get(solution_name)
            if calculator_class is None:
                import logging
                logging.getLogger(__name__).warning(f"Calculator not found for {solution_name}")
                return None
                
            # Create and return calculator instance with dimensions
            return calculator_class(length, height)
            
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Error creating calculator for {solution_name}: {e}")
            return None