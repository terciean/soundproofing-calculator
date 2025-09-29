"""
Ceiling solutions package.
Exposes ceiling solution classes with lazy loading to avoid circular imports.
"""

def get_resilient_bar_ceiling():
    """Lazy import to avoid circular dependency"""
    from .resilientbarceiling import ResilientBarCeilingStandard, ResilientBarCeilingSP15
    return ResilientBarCeilingStandard, ResilientBarCeilingSP15

def get_genie_clip_ceiling():
    """Lazy import to avoid circular dependency"""
    from .genieclipceiling import GenieClipCeilingStandard, GenieClipCeilingSP15
    return GenieClipCeilingStandard, GenieClipCeilingSP15

def get_independent_ceiling():
    """Lazy import to avoid circular dependency"""
    from .independentceiling import IndependentCeilingStandard, IndependentCeilingSP15
    return IndependentCeilingStandard, IndependentCeilingSP15

def get_lb3_genie_clip_ceiling():
    """Lazy import to avoid circular dependency"""
    from .lb3genieclipceiling import LB3GenieClipCeilingStandard, LB3GenieClipCeilingSP15
    return LB3GenieClipCeilingStandard, LB3GenieClipCeilingSP15

# Export all ceiling solutions
__all__ = [
    'get_resilient_bar_ceiling',
    'get_genie_clip_ceiling',
    'get_independent_ceiling',
    'get_lb3_genie_clip_ceiling'
]
