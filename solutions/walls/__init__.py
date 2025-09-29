"""
Wall solutions package.
Exposes wall solution classes with lazy loading to avoid circular imports.
"""

def get_independent_wall():
    """Lazy import to avoid circular dependency"""
    from .Independentwall import IndependentWallStandard, IndependentWallSP15
    return IndependentWallStandard, IndependentWallSP15

def get_resilient_bar_wall():
    """Lazy import to avoid circular dependency"""
    from .resilientbarwall import ResilientBarWallStandard, ResilientBarWallSP15
    return ResilientBarWallStandard, ResilientBarWallSP15

def get_genie_clip_wall():
    """Lazy import to avoid circular dependency"""
    from .GenieClipWall import GenieClipWallStandard, GenieClipWallSP15
    return GenieClipWallStandard, GenieClipWallSP15

def get_m20_wall():
    """Lazy import to avoid circular dependency"""
    from .M20Wall import M20WallStandard, M20WallSP15
    return M20WallStandard, M20WallSP15

# Export all wall solutions
__all__ = [
    'get_independent_wall',
    'get_resilient_bar_wall',
    'get_genie_clip_wall',
    'get_m20_wall'
]