

import os
from pathlib import Path
from dotenv import load_dotenv 
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import sys
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import certifi
import dns.resolver
import time
import math
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from bson import json_util

from solutions.logger import get_logger
from solutions.base_solution import BaseSolution
from solutions.cost_calculator import calculate_solution_costs, calculate_material_cost
from solutions.material_properties import get_material_characteristics, get_material_properties
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solutions.config import SOLUTION_MAPPINGS, SOLUTION_DESCRIPTIONS, SOLUTION_CATALOG, NOISE_PROFILES, SOLUTION_VARIANT_MONGO_IDS
from solutions.solution_mapping_new import SolutionMapping
from functools import lru_cache
from flask_caching import Cache
from solutions.acoustic_calculator import get_acoustic_calculator
import requests
from solutions.cache_manager import get_cache_manager

from solutions.walls import get_genie_clip_wall, get_m20_wall, get_independent_wall, get_resilient_bar_wall
from solutions.ceilings import get_genie_clip_ceiling, get_independent_ceiling, get_resilient_bar_ceiling
from solutions.walls.GenieClipWall import load_genieclipwall_solutions
from solutions.walls.M20Wall import load_m20wall_solutions
from solutions.walls.Independentwall import load_independentwall_solutions
from solutions.walls.resilientbarwall import load_resilientbarwall_solutions
from solutions.ceilings.genieclipceiling import load_genieclipceiling_solutions
from solutions.ceilings.lb3genieclipceiling import load_lb3genieclipceiling_solutions
from solutions.ceilings.independentceiling import load_independentceiling_solutions
from solutions.ceilings.resilientbarceiling import load_resilientbarceiling_solutions

import traceback
import uuid
import re
from datetime import datetime, timedelta

from solutions.solutions import get_solutions_manager
from solutions.recommendation_engine import rank_solutions, RoomInputs, NoiseProfile
from solutions.database import get_all_materials_from_db, get_solution_by_id

# Add before Flask app initialization
@dataclass
class NoiseData:
    type: str
    intensity: int
    direction: List[str]
    time: Optional[List[str]] = None

# Initialize Flask app first
app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize cache manager first
app.logger.info("Initializing cache manager...")
from solutions.cache_manager import CacheManager
cache_manager = get_cache_manager()
if cache_manager is None:
    app.logger.error("Cache manager initialization failed")
else:
    app.logger.info("Cache manager initialized successfully")

# Initialize solutions manager after cache manager
app.logger.info("Initializing solutions manager...")
solutions_manager = get_solutions_manager()
if solutions_manager is None:
    app.logger.error("Solutions manager initialization failed, will retry on first request")
else:
    app.logger.info("Solutions manager initialized successfully with cached solutions")

def ensure_solutions_manager():
    """Ensure solutions manager is initialized with proper caching"""
    global solutions_manager, cache_manager
    
    # Ensure cache manager is initialized first
    if cache_manager is None:
        app.logger.info("Attempting to initialize cache manager...")
        cache_manager = get_cache_manager()
        if cache_manager:
            app.logger.info("Cache manager initialized successfully")
        else:
            app.logger.error("Cache manager initialization failed")
    
    # Then initialize solutions manager
    if solutions_manager is None:
        app.logger.info("Attempting to initialize solutions manager...")
        solutions_manager = get_solutions_manager()
        if solutions_manager:
            app.logger.info("Solutions manager initialized successfully")
        else:
            app.logger.error("Solutions manager initialization failed")
    
    return solutions_manager is not None

# Load environment variables before any other imports
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a file handler for detailed solution logging
solution_file_handler = logging.FileHandler('solution_data.log')
solution_file_handler.setLevel(logging.INFO)
solution_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
solution_file_handler.setFormatter(solution_formatter)

# Add a filter to only log solution data messages
class SolutionDataFilter(logging.Filter):
    def filter(self, record):
        return '[SOLUTION DATA]' in record.getMessage() or '[DATA SOURCE]' in record.getMessage()

solution_file_handler.addFilter(SolutionDataFilter())

# Add the handler to the root logger to capture all solution data logs
logging.getLogger().addHandler(solution_file_handler)

# Regular file handler for app logs
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



# Initialize CORS properly
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize CSRF protection
csrf = CSRFProtect(app)
csrf.exempt(r"/api/*")
csrf.exempt(r"/recommendations")
csrf.exempt(r"/get_solutions/*")

# App version
APP_VERSION = '1.0.0'

# Configure cache with Redis if available, otherwise use SimpleCache
try:
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        cache = Cache(app, config={
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_URL': redis_url,
            'CACHE_DEFAULT_TIMEOUT': 300
        })
        logger.info("Using Redis for caching")
    else:
        cache = Cache(app, config={
            'CACHE_TYPE': 'SimpleCache',
            'CACHE_DEFAULT_TIMEOUT': 300
        })
        logger.info("Using SimpleCache for caching")
except Exception as e:
    logger.warning(f"Failed to initialize Redis cache, falling back to SimpleCache: {e}")
    cache = Cache(app, config={
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300
    })
    logger.info("Using SimpleCache for caching")

# Initialize Flask extensions with Redis storage if available
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=os.getenv('REDIS_URL', 'memory://'),
    default_limits=["200 per day", "50 per hour"]
)

def initialize_all_solutions_with_debug():
    """Initialize all solutions from MongoDB and register them with the solutions manager."""
    logger.info("Loading and caching all wall and ceiling solutions with debug info...")
    debug_results = []
    
    # Get solutions manager and cache manager
    solutions_manager = get_solutions_manager()
    cache_manager = get_cache_manager()
    
    if not solutions_manager or not cache_manager:
        logger.error("Failed to get solutions manager or cache manager")
        return debug_results
    
    # Define solution loaders with their MongoDB document IDs
    solution_loaders = {
        'walls': [
            (load_genieclipwall_solutions, 'GenieClipWall'),
            (load_m20wall_solutions, 'M20Wall'),
            (load_independentwall_solutions, 'IndependentWall'),
            (load_resilientbarwall_solutions, 'ResilientBarWall'),
        ],
        'ceilings': [
            (load_genieclipceiling_solutions, 'GenieClipCeiling'),
            (load_lb3genieclipceiling_solutions, 'LB3GenieClipCeiling'),
            (load_independentceiling_solutions, 'IndependentCeiling'),
            (load_resilientbarceiling_solutions, 'ResilientBarCeiling'),
        ]
    }
    
    # Load solutions by surface type
    for surface_type, loaders in solution_loaders.items():
        surface_solutions = []
        
        for loader, name in loaders:
            try:
                std, pro = loader()
                std_loaded = std is not None and getattr(std, '_solution_data', None) is not None
                pro_loaded = pro is not None and getattr(pro, '_solution_data', None) is not None
                
                logger.info(f"Loaded {name} Standard: {std_loaded}")
                logger.info(f"Loaded {name} SP15: {pro_loaded}")
                
                debug_results.append({f'{name}_Standard': std_loaded})
                debug_results.append({f'{name}_SP15': pro_loaded})
                
                # Register solutions with solutions manager if they have data
                if std_loaded and std:
                    solution_id = f"{name.lower()}_standard"
                    solutions_manager.register_solution_with_characteristics(solution_id, std)
                    surface_solutions.append(std)
                    logger.info(f"Registered {solution_id} with solutions manager")
                
                if pro_loaded and pro:
                    solution_id = f"{name.lower()}_sp15"
                    solutions_manager.register_solution_with_characteristics(solution_id, pro)
                    surface_solutions.append(pro)
                    logger.info(f"Registered {solution_id} with solutions manager")
                
            except Exception as e:
                logger.error(f"Error loading {name} solutions: {e}")
                debug_results.append({f'{name}_error': str(e)})
        
        # Cache solutions by surface type
        if surface_solutions:
            # Convert solutions to serializable format for caching
            serializable_solutions = []
            logger.info(f"[DEBUG] Processing {len(surface_solutions)} {surface_type} solutions for serialization")
            for solution in surface_solutions:
                try:
                    if hasattr(solution, 'get_characteristics'):
                        characteristics = solution.get_characteristics()
                        logger.info(f"[DEBUG] Solution {getattr(solution, 'CODE_NAME', 'Unknown')} characteristics: {len(characteristics) if characteristics else 0} items")
                        if characteristics:
                            # Add solution identifier
                            characteristics['solution_id'] = getattr(solution, 'CODE_NAME', 'Unknown')
                            characteristics['surface_type'] = surface_type
                            characteristics['variant'] = 'SP15' if hasattr(solution, 'IS_SP15') and solution.IS_SP15 else 'Standard'
                            serializable_solutions.append(characteristics)
                            logger.info(f"[DEBUG] Added solution {getattr(solution, 'CODE_NAME', 'Unknown')} to serializable list")
                        else:
                            logger.warning(f"[DEBUG] Solution {getattr(solution, 'CODE_NAME', 'Unknown')} returned empty characteristics")
                    else:
                        logger.warning(f"[DEBUG] Solution {getattr(solution, 'CODE_NAME', 'Unknown')} has no get_characteristics method")
                except Exception as e:
                    logger.error(f"Error serializing solution {getattr(solution, 'CODE_NAME', 'Unknown')}: {e}")
            
            logger.info(f"[DEBUG] Created {len(serializable_solutions)} serializable solutions for {surface_type}")
            
            # Cache solutions by surface type
            cache_key = f"{surface_type.rstrip('s')}_solutions"  # Use singular form
            cache_manager.set(cache_key, serializable_solutions, 3600)
            logger.info(f"Cached {len(serializable_solutions)} {surface_type} solutions for recommendation engine")
            
            # Debug: Check what's actually in the cache
            cached_data = cache_manager.get(cache_key)
            logger.info(f"[DEBUG] Cache key '{cache_key}' contains {len(cached_data) if cached_data else 0} items")
            if cached_data:
                logger.info(f"[DEBUG] First cached solution: {cached_data[0] if len(cached_data) > 0 else 'None'}")
            
            # Also cache individual solutions for backward compatibility
            for solution in surface_solutions:
                try:
                    cache_key = f"{getattr(solution, 'CODE_NAME', 'Unknown').lower().replace(' ', '').replace('(', '').replace(')', '')}_{'sp15' if hasattr(solution, 'IS_SP15') and solution.IS_SP15 else 'standard'}"
                    cache_manager.set(cache_key, solution, 3600)
                except Exception as e:
                    logger.error(f"Error caching individual solution: {e}")
        else:
            logger.warning(f"[DEBUG] No {surface_type} solutions to cache")
    
    logger.info(f"Solution loading debug summary: {debug_results}")
    logger.info(f"Total solutions registered with manager: {len(solutions_manager.get_all_solutions())}")
    
    return debug_results

# Call this at startup
initialize_all_solutions_with_debug()

@app.route('/api/solutions', methods=['GET'])
def get_all_solutions():
    """Get all wall and ceiling solutions from the cache, with debug info."""
    try:
        cache_manager = get_cache_manager()
        wall_keys = [
            'genieclipwall_standard', 'genieclipwall_sp15',
            'm20wall_standard', 'm20wall_sp15',
            'independentwall_standard', 'independentwall_sp15',
            'resilientbarwall_standard', 'resilientbarwall_sp15',
        ]
        ceiling_keys = [
            'genieclipceiling_standard', 'genieclipceiling_sp15',
            'lb3genieclipceiling_standard', 'lb3genieclipceiling_sp15',
            'independentceiling_standard', 'independentceiling_sp15',
            'resilientbarceiling_standard', 'resilientbarceiling_sp15',
        ]
        all_solutions = []
        for key in wall_keys + ceiling_keys:
            sol = cache_manager.get(key)
            if sol and hasattr(sol, '_solution_data') and sol._solution_data:
                data = dict(sol._solution_data)
                data['cache_key'] = key
                data['variant'] = 'SP15' if 'sp15' in key else 'Standard'
                all_solutions.append(data)
            else:
                logger.warning(f"Solution not found or missing data for cache key: {key}")
        return jsonify(all_solutions)
    except Exception as e:
        logger.error(f"Error getting all solutions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/materials', methods=['GET'])
def get_all_materials():
    """Get all materials from the MongoDB database."""
    try:
        materials = get_all_materials_from_db()
        logger.info(f"[MATERIALS] Found {len(materials)} materials in MongoDB.")
        if materials:
            logger.info(f"[MATERIALS] Sample material: {materials[0]}")
        # Convert materials to frontend format
        materials_list = []
        for mat in materials:
            material = {
                '_id': str(mat.get('_id', '')),
                'name': mat.get('name', ''),
                'category': mat.get('category', 'unknown'),
                'thickness': mat.get('thickness', 0),
                'density': mat.get('density', 0),
                'stc_rating': mat.get('stc_rating', 0),
                'cost_per_sqm': mat.get('cost', 0)
            }
            materials_list.append(material)
        return jsonify(materials_list)
    except Exception as e:
        logger.error(f"Error getting all materials: {e}")
        return jsonify([]), 200

@app.route('/api/solutions/<surface_type>', methods=['GET'])
def get_solutions_api(surface_type):
    """Get solutions for a specific surface type from the cache manager (standard and SP15)."""
    try:
        cache_manager = get_cache_manager()
        surface_type = surface_type.lower()
        key_map = {
            'wall': [
                'genieclipwall_standard', 'genieclipwall_sp15',
                'm20wall_standard', 'm20wall_sp15',
                'independentwall_standard', 'independentwall_sp15',
                'resilientbarwall_standard', 'resilientbarwall_sp15',
            ],
            'ceiling': [
                'genieclipceiling_standard', 'genieclipceiling_sp15',
                'lb3genieclipceiling_standard', 'lb3genieclipceiling_sp15',
                'independentceiling_standard', 'independentceiling_sp15',
                'resilientbarceiling_standard', 'resilientbarceiling_sp15',
            ],
        }
        keys = key_map.get(surface_type, [])
        solutions = []
        for key in keys:
            sol = cache_manager.get(key)
            if sol and hasattr(sol, '_solution_data') and sol._solution_data:
                data = dict(sol._solution_data)
                data['cache_key'] = key
                data['variant'] = 'SP15' if 'sp15' in key else 'Standard'
                solutions.append(data)
            else:
                logger.warning(f"Solution not found or missing data for cache key: {key}")
        return jsonify(solutions)
    except Exception as e:
        logger.error(f"Error getting solutions for {surface_type}: {e}")
        return jsonify({'error': str(e)}), 500



@app.route('/api/calculate-costs', methods=['POST'])
def calculate_costs_api():
    """Calculate costs for soundproofing solutions."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input data
        if not data.get('recommendations') or not data.get('dimensions'):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Check for detailed breakdown flag
        detailed = data.get('detailed', False)
            
        # Get solutions manager
        solutions_manager = get_solutions_manager()
        if not solutions_manager:
            return jsonify({'error': 'Failed to get solutions manager'}), 500
        
        # Extract data
        recommendations = data['recommendations']
        dimensions = data['dimensions']
        selected_directions = data.get('selectedDirections', [])
        blockages = data.get('blockages', {})
        region = data.get('region', 'UK')
        
        # Calculate costs for each surface type
        costs = {
            'wall': 0,
            'ceiling': 0,
            'floor': 0,
            'total': 0
        }
        detailed_breakdown = {'wall': [], 'ceiling': [], 'floor': []} if detailed else None
        
        # Calculate wall costs
        if recommendations.get('primary', {}).get('walls'):
            for wall in recommendations['primary']['walls']:
                if wall.get('solution') and (not selected_directions or wall.get('direction') in selected_directions):
                    wall_cost = calculate_material_cost(wall['solution'], dimensions)
                    costs['wall'] += wall_cost
                    if detailed:
                        # Fetch solution and material breakdown
                        breakdown = get_solution_material_breakdown(wall['solution'], dimensions)
                        detailed_breakdown['wall'].append(breakdown)
        
        # Calculate ceiling cost
        if recommendations.get('primary', {}).get('ceiling'):
            ceiling = recommendations['primary']['ceiling']
            if ceiling.get('solution'):
                costs['ceiling'] = calculate_material_cost(ceiling['solution'], dimensions)
                if detailed:
                    breakdown = get_solution_material_breakdown(ceiling['solution'], dimensions)
                    detailed_breakdown['ceiling'].append(breakdown)
        
        # Calculate floor cost
        if recommendations.get('primary', {}).get('floor'):
            floor = recommendations['primary']['floor']
            if floor.get('solution'):
                costs['floor'] = calculate_material_cost(floor['solution'], dimensions)
                if detailed:
                    breakdown = get_solution_material_breakdown(floor['solution'], dimensions)
                    detailed_breakdown['floor'].append(breakdown)
        
        # Apply regional price factor
        price_factor = get_regional_price_factor(region)
        for key in costs:
            if key != 'total':
                costs[key] *= price_factor
        
        # Calculate total
        costs['total'] = costs['wall'] + costs['ceiling'] + costs['floor']
        
        response = costs
        if detailed:
            response = {'costs': costs, 'detailed_breakdown': detailed_breakdown}
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error calculating costs: {e}")
        return jsonify({'error': str(e)}), 500

def get_regional_price_factor(region):
    """Get price factor for a region."""
    price_factors = {
        'UK': 1.0,
        'US': 0.9,
        'Canada': 0.95,
        'Australia': 1.1,
        'Europe': 1.05
    }
    return price_factors.get(region, 1.0)

@app.route('/api/calculate-acoustic-properties', methods=['POST'])
def calculate_acoustic_properties():
    """Calculate acoustic properties for a solution."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Validate input data
        if not data.get('solution_id') or not data.get('dimensions'):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Get acoustic calculator
        calculator = get_acoustic_calculator()
        if not calculator:
            return jsonify({'error': 'Failed to get acoustic calculator'}), 500
            
        # Calculate properties
        properties = calculator.calculate_properties(
            solution_id=data['solution_id'],
            dimensions=data['dimensions']
        )
        
        return jsonify(properties)
        
    except Exception as e:
        logger.error(f"Error calculating acoustic properties: {e}")
        return jsonify({'error': str(e)}), 500

@csrf.exempt
@app.route('/api/recommendations', methods=['POST'])
def get_recommendations_flask():
    """Generate recommendations for soundproofing based on input data."""
    try:
        payload = request.get_json()
        logger.info(f"[DEBUG] Incoming /api/recommendations payload: {payload}")
        if not isinstance(payload, dict):
            logger.warning("Invalid payload format: not a dict")
            return jsonify({'error': 'Invalid payload format.'}), 400
        # Extract and validate required fields
        required_fields = [
            "room_type", "noise_type", "noise_level", "room_dimensions",
            "surface_areas", "existing_construction", "noise_profile"
        ]
        missing_fields = [f for f in required_fields if f not in payload]
        if missing_fields:
            logger.warning(f"Missing required fields: {missing_fields}")
            return jsonify({'error': f"Missing required fields: {missing_fields}"}), 400
        if not isinstance(payload["noise_profile"], dict):
            logger.warning("Malformed noise_profile field")
            return jsonify({'error': 'Malformed noise_profile field.'}), 400
        # Validate types of other fields
        if not isinstance(payload["room_dimensions"], dict):
            logger.warning("Malformed room_dimensions field")
            return jsonify({'error': 'Malformed room_dimensions field.'}), 400
        if not isinstance(payload["surface_areas"], dict):
            logger.warning("Malformed surface_areas field")
            return jsonify({'error': 'Malformed surface_areas field.'}), 400
        if not isinstance(payload["existing_construction"], dict):
            logger.warning("Malformed existing_construction field")
            return jsonify({'error': 'Malformed existing_construction field.'}), 400
        try:
            room_inputs = RoomInputs(
                room_type=payload["room_type"],
                noise_type=payload["noise_type"],
                noise_level=payload["noise_level"],
                room_dimensions=payload["room_dimensions"],
                surface_areas=payload["surface_areas"],
                existing_construction=payload["existing_construction"],
                budget_constraints=payload.get("budget_constraints"),
                priority_surfaces=payload.get("priority_surfaces"),
                special_requirements=payload.get("special_requirements")
            )
            noise_profile = NoiseProfile(
                type=payload["noise_profile"].get("type"),
                intensity=payload["noise_profile"].get("intensity"),
                direction=payload["noise_profile"].get("direction", []),
                time=payload["noise_profile"].get("time"),
                frequency=payload["noise_profile"].get("frequency"),
                is_impact=payload["noise_profile"].get("is_impact", False)
            )
        except Exception as e:
            logger.error(f"Invalid input data: {e}")
            return jsonify({'error': f"Invalid input data: {e}"}), 400
        try:
            solutions_manager = get_solutions_manager()
            if not solutions_manager:
                logger.error("Failed to initialize solutions manager.")
                return jsonify({'error': 'Failed to initialize solutions manager.'}), 500
            # Gather all possible solutions (for all surface types)
            all_solutions = []
            solution_types = getattr(solutions_manager, "SOLUTION_TYPES", None)
            if not solution_types:
                solution_types = ['wall', 'ceiling', 'floor']
            for surface_type in solution_types:
                surface_solutions = solutions_manager.get_solutions_by_type(surface_type)
                logger.info(f"[DEBUG] {surface_type} solutions found: {len(surface_solutions) if surface_solutions else 0}")
                if surface_solutions:
                    # Convert solution instances to dictionaries for rank_solutions
                    for solution in surface_solutions:
                        if isinstance(solution, dict):
                            # Solution is already in dictionary format
                            all_solutions.append(solution)
                        elif hasattr(solution, 'get_characteristics'):
                            # Convert solution instance to dictionary
                            characteristics = solution.get_characteristics()
                            if characteristics:
                                # Add solution identifier
                                characteristics['solution_id'] = getattr(solution, 'CODE_NAME', 'Unknown')
                                characteristics['surface_type'] = surface_type
                                characteristics['variant'] = 'SP15' if hasattr(solution, 'IS_SP15') and solution.IS_SP15 else 'Standard'
                                all_solutions.append(characteristics)
                        else:
                            logger.warning(f"Solution {solution} has no get_characteristics method")
            logger.info(f"[DEBUG] Total solutions passed to rank_solutions: {len(all_solutions)}")
            logger.debug(f"[DEBUG] all_solutions sample: {all_solutions[:2] if all_solutions else '[]'}")
            logger.debug(f"[DEBUG] room_inputs: {room_inputs}")
            logger.debug(f"[DEBUG] noise_profile: {noise_profile}")
            recommendations = rank_solutions(all_solutions, room_inputs, noise_profile)
            logger.info(f"Generated {len(recommendations) if recommendations else 0} recommendations.")
        except Exception as e:
            logger.error(f"Recommendation engine error: {e}")
            return jsonify({'error': f"Recommendation engine error: {e}"}), 500
        # Check for detailed breakdown flag
        detailed = payload.get('detailed', False)
        if detailed:
            # Attach detailed material breakdown for each recommended solution
            for surface in ['walls', 'ceiling', 'floor']:
                if recommendations and recommendations.get('primary', {}).get(surface):
                    if isinstance(recommendations['primary'][surface], list):
                        for rec in recommendations['primary'][surface]:
                            rec['material_breakdown'] = get_solution_material_breakdown(rec.get('solution'), payload.get('room_dimensions', {}))
                    elif isinstance(recommendations['primary'][surface], dict):
                        rec = recommendations['primary'][surface]
                        rec['material_breakdown'] = get_solution_material_breakdown(rec.get('solution'), payload.get('room_dimensions', {}))
        return jsonify({"recommendations": recommendations or []})
    except Exception as e:
        logger.error(f"[FATAL] Unhandled exception in /api/recommendations: {e}")
        return jsonify({'error': f'Unhandled exception: {e}'}), 400

# Utility function for detailed material breakdown

def get_solution_material_breakdown(solution_id, dimensions):
    """Return a detailed breakdown of materials for a solution, including acoustic and cost properties using new loader."""
    from solutions.material_properties import get_material_properties
    from solutions.cost_calculator import calculate_material_cost
    from solutions.database import get_solution_by_id
    solution = get_solution_by_id(solution_id)
    if not solution or 'materials' not in solution:
        return {'solution_id': solution_id, 'materials': [], 'error': 'Solution or materials not found'}
    material_names = [m['name'] if isinstance(m, dict) else m for m in solution['materials']]
    material_props = get_material_properties(material_names)
    breakdown = []
    for m in solution['materials']:
        name = m['name'] if isinstance(m, dict) else m
        props = material_props.get(name, {})
        cost = props.get('cost', 0)
        coverage = props.get('coverage', m.get('coverage', None))
        stc = props.get('stc_rating', None)
        freq = props.get('acoustic_properties', {}).get('frequency_response', None)
        breakdown.append({
            'name': name,
            'cost': cost,
            'coverage': coverage,
            'stc_rating': stc,
            'frequency_response': freq
        })
    total_cost = calculate_material_cost(solution_id, dimensions)
    return {'solution_id': solution_id, 'materials': breakdown, 'total_cost': total_cost}

@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')

if __name__ == '__main__':
    # Initialize all required components
    if not ensure_solutions_manager():
        logger.error("Failed to initialize solutions manager. Application may not work correctly.")
    
    # Run the Flask application
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting server at http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)