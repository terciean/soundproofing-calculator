#!/usr/bin/env python3
"""
Test script to check if solutions are loading properly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from solutions.walls.GenieClipWall import load_genieclipwall_solutions
from solutions.walls.M20Wall import load_m20wall_solutions
from solutions.walls.Independentwall import load_independentwall_solutions
from solutions.walls.resilientbarwall import load_resilientbarwall_solutions
from solutions.ceilings.genieclipceiling import load_genieclipceiling_solutions
from solutions.ceilings.lb3genieclipceiling import load_lb3genieclipceiling_solutions
from solutions.ceilings.independentceiling import load_independentceiling_solutions
from solutions.ceilings.resilientbarceiling import load_resilientbarceiling_solutions

def test_solution_loading():
    """Test if solutions are loading properly"""
    print("Testing solution loading...")
    
    # Test wall solutions
    print("\n=== Testing Wall Solutions ===")
    
    # GenieClip Wall
    try:
        std, pro = load_genieclipwall_solutions()
        print(f"GenieClip Wall Standard: {std.CODE_NAME}")
        print(f"GenieClip Wall SP15: {pro.CODE_NAME}")
        
        # Test characteristics
        std_chars = std.get_characteristics()
        pro_chars = pro.get_characteristics()
        
        print(f"Standard characteristics: {len(std_chars) if std_chars else 0} items")
        print(f"SP15 characteristics: {len(pro_chars) if pro_chars else 0} items")
        
        if std_chars:
            print(f"Standard STC: {std_chars.get('stc_rating', 'N/A')}")
        if pro_chars:
            print(f"SP15 STC: {pro_chars.get('stc_rating', 'N/A')}")
            
    except Exception as e:
        print(f"Error loading GenieClip Wall: {e}")
    
    # M20 Wall
    try:
        std, pro = load_m20wall_solutions()
        print(f"\nM20 Wall Standard: {std.CODE_NAME}")
        print(f"M20 Wall SP15: {pro.CODE_NAME}")
        
        # Test characteristics
        std_chars = std.get_characteristics()
        pro_chars = pro.get_characteristics()
        
        print(f"Standard characteristics: {len(std_chars) if std_chars else 0} items")
        print(f"SP15 characteristics: {len(pro_chars) if pro_chars else 0} items")
        
        if std_chars:
            print(f"Standard STC: {std_chars.get('stc_rating', 'N/A')}")
        if pro_chars:
            print(f"SP15 STC: {pro_chars.get('stc_rating', 'N/A')}")
            
    except Exception as e:
        print(f"Error loading M20 Wall: {e}")
    
    # Test ceiling solutions
    print("\n=== Testing Ceiling Solutions ===")
    
    # GenieClip Ceiling
    try:
        std, pro = load_genieclipceiling_solutions()
        print(f"GenieClip Ceiling Standard: {std.CODE_NAME}")
        print(f"GenieClip Ceiling SP15: {pro.CODE_NAME}")
        
        # Test characteristics
        std_chars = std.get_characteristics()
        pro_chars = pro.get_characteristics()
        
        print(f"Standard characteristics: {len(std_chars) if std_chars else 0} items")
        print(f"SP15 characteristics: {len(pro_chars) if pro_chars else 0} items")
        
        if std_chars:
            print(f"Standard STC: {std_chars.get('stc_rating', 'N/A')}")
        if pro_chars:
            print(f"SP15 STC: {pro_chars.get('stc_rating', 'N/A')}")
            
    except Exception as e:
        print(f"Error loading GenieClip Ceiling: {e}")

if __name__ == "__main__":
    test_solution_loading() 