import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
from flask import Flask, render_template, request, jsonify
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
from solutions.database import get_db
import re

# Add debug logging for imports
print("Starting imports...")
try:
    from solutions.room import Room
    from solutions.walls.M20Wall import M20WallStandard, M20WallSP15
    from solutions.walls.GenieClipWall import GenieClipWallStandard, GenieClipWallSP15
    from solutions.walls.resilientbarwall import ResilientBarWallStandard, ResilientBarWallSP15
    from solutions.walls.Independentwall import IndependentWallStandard, IndependentWallSP15
    from solutions.ceilings.resilientbarceiling import (
        ResilientBarCeilingStandard,
        ResilientBarCeilingSP15
    )
    print("All imports successful")
except Exception as e:
    print(f"Import failed: {str(e)}")
    sys.exit(1)

# Initialize logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

# Load environment variables
load_dotenv()

def setup_mongodb():
    try:
        # Load the MongoDB URI from the environment
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            logger.error("MONGODB_URI environment variable not set")
            return setup_fallback_data()

        # Configure MongoDB client with enhanced settings
        client_settings = {
            'tlsCAFile': certifi.where(),
            'serverSelectionTimeoutMS': 10000,
            'connectTimeoutMS': 10000,
            'socketTimeoutMS': 20000,
            'retryWrites': True,
            'retryReads': True,
            'maxPoolSize': 50,
            'minPoolSize': 10,
            'maxIdleTimeMS': 45000,
            'waitQueueTimeoutMS': 10000,
            'heartbeatFrequencyMS': 10000
        }

        # Initialize client with retry logic
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                client = MongoClient(mongodb_uri, **client_settings)
                # Test connection
                client.admin.command('ping')
                logger.info("Successfully connected to MongoDB")
                
                # Initialize database and collections
                db = client.guyrazor
                wallsolutions = db.wallsolutions
                ceilingsolutions = db.ceilingsolutions
                
                # Verify collections exist and are accessible
                if wallsolutions.count_documents({}) >= 0 and ceilingsolutions.count_documents({}) >= 0:
                    logger.info("Successfully verified collections access")
                    return client, db, wallsolutions, ceilingsolutions
                else:
                    raise Exception("Could not verify collections")
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"MongoDB connection attempt {attempt + 1} failed: {str(e)}")
                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    logger.error(f"All MongoDB connection attempts failed: {str(e)}")
                    return setup_fallback_data()

    except Exception as e:
        logger.error(f"Critical error in MongoDB setup: {str(e)}")
        return setup_fallback_data()


def setup_fallback_data():
    """Provide fallback data when MongoDB is unavailable"""
    logger.info("Using fallback data")
    
    class FallbackDB:
        def __init__(self):
            self.wallsolutions = FallbackCollection([
                {"name": "Basic Wall", "type": "wall", "nrc": 0.05},
                {"name": "Standard Drywall", "type": "wall", "nrc": 0.1}
            ])
            self.ceilingsolutions = FallbackCollection([
                {"name": "Basic Ceiling", "type": "ceiling", "nrc": 0.05},
                {"name": "Standard Ceiling", "type": "ceiling", "nrc": 0.1}
            ])

    class FallbackCollection:
        def __init__(self, data):
            self.data = data

        def find(self, query=None):
            return self.data

        def find_one(self, query=None):
            return self.data[0] if self.data else None

        def count_documents(self, query=None):
            return len(self.data)

    db = FallbackDB()
    return None, db, db.wallsolutions, db.ceilingsolutions

# Initialize MongoDB and Flask
try:
    client, db, wallsolutions, ceilingsolutions = setup_mongodb()
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
    csrf = CSRFProtect()
    csrf.init_app(app)
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"]
    )
    CORS(app)
except Exception as e:
    logger.error(f"Failed to initialize MongoDB: {e}")
    sys.exit(1)

# Import solution classes
try:
    # Wall solutions
    from solutions.walls.Independentwall import IndependentWallStandard, IndependentWallSP15
    from solutions.walls.resilientbarwall import ResilientBarWallStandard, ResilientBarWallSP15
    from solutions.walls.GenieClipWall import GenieClipWallStandard, GenieClipWallSP15
    from solutions.walls.M20Wall import M20WallStandard, M20WallSP15
    
    # Ceiling solutions
    from solutions.ceilings.independentceiling import IndependentCeilingStandard, IndependentCeilingSP15
    from solutions.ceilings.genieclipceiling import GenieClipCeilingStandard, GenieClipCeilingSP15
    from solutions.ceilings.lb3genieclipceiling import LB3GenieClipCeilingStandard, LB3GenieClipCeilingSP15
    from solutions.ceilings.resilientbarceiling import ResilientBarCeilingStandard, ResilientBarCeilingSP15
    
    logger.info("Successfully imported solution classes")
except ImportError as e:
    logger.error(f"Import Error: {e}")
    sys.exit(1)

# Dictionary mapping solution names to calculator classes
CALCULATORS = {
    "Independent Wall (Standard)": IndependentWallStandard,
    "Independent Wall (SP15 Soundboard Upgrade)": IndependentWallSP15,
    "Resilient bar wall (Standard)": ResilientBarWallStandard,
    "Resilient bar wall (SP15 Soundboard Upgrade)": ResilientBarWallSP15,
    "Genie Clip wall (Standard)": GenieClipWallStandard,
    "Genie Clip wall (SP15 Soundboard Upgrade)": GenieClipWallSP15,
    "M20 Solution (Standard)": M20WallStandard,
    "M20 Solution (SP15 Soundboard upgrade)": M20WallSP15,
    "Independent Ceiling": IndependentCeilingStandard,
    "Independent Ceiling (SP15 Soundboard Upgrade)": IndependentCeilingSP15,
    "Genie Clip ceiling": GenieClipCeilingStandard,
    "Genie Clip ceiling (SP15 Soundboard Upgrade)": GenieClipCeilingSP15,
    "LB3 Genie Clip": LB3GenieClipCeilingStandard,
    "LB3 Genie Clip (SP15 Soundboard Upgrade)": LB3GenieClipCeilingSP15,
    "Resilient bar Ceiling": ResilientBarCeilingStandard,
    "Resilient bar Ceiling (SP15 Soundboard Upgrade)": ResilientBarCeilingSP15
}

SOLUTION_TYPES = {
    'walls': [
        'Independent Wall Standard',
        'Independent Wall SP15',
        'Resilient Bar Wall Standard',
        'Resilient Bar Wall SP15',
        'Genie Clip Wall Standard',
        'Genie Clip Wall SP15',
        'M20 Wall Standard',
        'M20 Wall SP15'
    ],
    'ceilings': [
        'Resilient Bar Ceiling Standard',
        'Resilient Bar Ceiling SP15',
        'LB3 Genie Clip Ceiling Standard',
        'LB3 Genie Clip Ceiling SP15'
    ]
}

SURFACE_TYPES = ['walls', 'ceilings']

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                wall_features = data.get('wall_features', [])
                ceiling_features = data.get('ceiling_features', [])
                floor_features = data.get('floor_features', [])
                length = float(data.get('length', 0))
                width = float(data.get('width', 0))
                height = float(data.get('height', 0))
            else:
                # Existing form data handling
                wall_features = request.form.getlist('wall_features[]')
                ceiling_features = request.form.getlist('ceiling_features[]')
                floor_features = request.form.getlist('floor_features[]')
                length = float(request.form.get('length', 0))
                width = float(request.form.get('width', 0))
                height = float(request.form.get('height', 0))
            
            # Create room instance
            room = Room(
                name="Main Room",
                length=length,
                width=width,
                height=height
            )
            
            # Process blockages if present
            if 'blockages' in request.form:
                blockages_data = request.form.getlist('blockages[]')
                for blockage in blockages_data:
                    blockage_data = json.loads(blockage)
                    room.add_blockage(
                        surface_type=blockage_data['surface_type'],
                        length=float(blockage_data['length']),
                        width=float(blockage_data['width']),
                        position=blockage_data.get('position')
                    )
            
            # Calculate room summary
            room_summary = room.get_room_summary()
            
            return render_template('index.html',
                                solution_types=SOLUTION_TYPES,
                                surface_types=SURFACE_TYPES,
                                room_data=room_summary,
                                wall_features=wall_features,
                                ceiling_features=ceiling_features,
                                floor_features=floor_features)
        
        # GET request
        return render_template('index.html',
                            solution_types=SOLUTION_TYPES,
                            surface_types=SURFACE_TYPES)
                            
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return render_template('index.html',
                            error="Server Error",
                            message=str(e),
                            solution_types=SOLUTION_TYPES,
                            surface_types=SURFACE_TYPES)
@app.route('/get_solutions/<surface_type>', methods=['GET'])
def get_solutions(surface_type):
    valid_surface_types = ['walls', 'ceilings', 'floors']
    if surface_type not in valid_surface_types:
        return jsonify({'error': f'Invalid surface type: {surface_type}'}), 400
    
    try:
        if surface_type == 'walls':
            solutions = list(walls.find({}, {'_id': 0}))  # Fetch wall solutions
        elif surface_type == 'ceilings':
            solutions = list(ceilings.find({}, {'_id': 0}))  # Fetch ceiling solutions
        elif surface_type == 'floors':
            solutions = []  # Add floor logic here if necessary
        else:
            solutions = []
        
        if not solutions:
            return jsonify({'error': 'No solutions found'}), 404
        
        return jsonify(solutions), 200
    except Exception as e:
        logger.error(f"Error fetching solutions for {surface_type}: {str(e)}")
        return jsonify({'error': str(e), 'error_type': type(e).__name__}), 500
@app.route('/health')
def health_check():
    """Enhanced health check endpoint"""
    try:
        # Check MongoDB connection
        mongo_status = {'status': 'unknown', 'latency_ms': None}
        if client:
            start_time = time.time()
            client.admin.command('ping')
            latency = (time.time() - start_time) * 1000
            mongo_status = {
                'status': 'connected',
                'latency_ms': round(latency, 2)
            }
        else:
            mongo_status = {'status': 'disconnected'}

        # Check collections
        collections_status = {
            'walls': wallsolutions.count_documents({}) if wallsolutions else 0,
            'ceilings': ceilingsolutions.count_documents({}) if ceilingsolutions else 0
        }

        # Memory usage (if psutil is available)
        memory_status = {}
        try:
            import psutil
            process = psutil.Process()
            memory_status = {
                'memory_percent': round(process.memory_percent(), 2),
                'memory_mb': round(process.memory_info().rss / 1024 / 1024, 2)
            }
        except ImportError:
            memory_status = {'error': 'psutil not available'}

        return jsonify({
            'status': 'healthy' if mongo_status['status'] == 'connected' else 'degraded',
            'timestamp': time.time(),
            'mongo': mongo_status,
            'collections': collections_status,
            'memory': memory_status
        }), 200 if mongo_status['status'] == 'connected' else 503

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': time.time()
        }), 500

@app.route('/debug_solutions')
def debug_solutions():
    try:
        # Test direct MongoDB access
        wall_count = wallsolutions.count_documents({})
        ceiling_count = ceilingsolutions.count_documents({})
        logger.info(f"Wall solutions count: {wall_count}")
        logger.info(f"Ceiling solutions count: {ceiling_count}")

        # Get raw documents without any filtering
        wall_sols = list(wallsolutions.find({}, {'_id': 0}))
        ceiling_sols = list(ceilingsolutions.find({}, {'_id': 0}))
        
        logger.info(f"Raw wall solutions: {wall_sols}")
        logger.info(f"Raw ceiling solutions: {ceiling_sols}")

        return jsonify({
            'database_counts': {
                'walls': wall_count,
                'ceilings': ceiling_count
            },
            'raw_data': {
                'wall_solutions': wall_sols,
                'ceiling_solutions': ceiling_sols
            },
            'calculators': list(CALCULATORS.keys())
        })
    except Exception as e:
        logger.error(f"Debug route error: {str(e)}")
        return jsonify({'error': str(e), 'error_type': type(e).__name__}), 500

@app.errorhandler(500)
def handle_500(e):
    logger.error(f"Server error: {str(e)}")
    return render_template('index.html', 
                         error="Server Error",
                         message="An internal server error occurred.",
                         solution_types=SOLUTION_TYPES,
                         surface_types=SURFACE_TYPES)

@app.errorhandler(404)
def handle_404(e):
    return render_template('index.html',
                         error="Not Found",
                         message="The requested page was not found.",
                         solution_types=SOLUTION_TYPES,
                         surface_types=SURFACE_TYPES)

@app.route('/room/<room_id>', methods=['GET', 'POST'])
def room_details(room_id):
    try:
        if request.method == 'POST':
            data = request.get_json()
            
            # Create or update room
            room = Room(
                name=data.get('name', f'Room {room_id}'),
                length=float(data.get('length', 0)),
                width=float(data.get('width', 0)),
                height=float(data.get('height', 0))
            )
            
            # Handle blockages if present
            if 'blockages' in data:
                for blockage in data['blockages']:
                    room.add_blockage(
                        surface_type=blockage['surface_type'],
                        length=float(blockage['length']),
                        width=float(blockage['width']),
                        position=blockage.get('position')
                    )
            
            # Calculate room summary
            summary = room.get_room_summary()
            return jsonify(summary)
            
        else:
            # GET request - return room template or data
            return jsonify({
                'status': 'success',
                'message': 'Room details endpoint ready'
            })
            
    except Exception as e:
        logger.error(f"Room details error: {str(e)}")
        return jsonify({
            'error': str(e),
            'error_type': type(e).__name__
        }), 500

@app.route('/update_room', methods=['POST'])
def update_room():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract and validate dimensions
        dimensions = data.get('dimensions', {})
        try:
            dimensions = {
                'length': float(dimensions.get('length', 0)),
                'width': float(dimensions.get('width', 0)),
                'height': float(dimensions.get('height', 0))
            }
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid dimension values'}), 400

        # Validate dimensions
        if any(d <= 0 for d in dimensions.values()):
            return jsonify({'error': 'All dimensions must be positive numbers'}), 400

        # Create room instance
        room = Room(name="Room", **dimensions)

        # Handle surfaces
        if 'surfaces' in data:
            surfaces = data['surfaces']
            
            # Process ceiling
            if 'ceiling' in surfaces:
                ceiling = surfaces['ceiling']
                for feature in ceiling.get('features', []):
                    room.add_ceiling_feature(feature)

            # Process floor
            if 'floor' in surfaces:
                floor = surfaces['floor']
                for feature in floor.get('features', []):
                    room.add_floor_feature(feature)

        return jsonify(room.get_room_summary())

    except Exception as e:
        logger.error(f"Room update error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def get_solutions_from_db(surface_type):
    if surface_type == 'walls':
        return list(walls.find({}, {'_id': 0}))  # Adjust according to your MongoDB collection
    elif surface_type == 'ceilings':
        return list(ceilings.find({}, {'_id': 0}))
    elif surface_type == 'floors':
        return list(floors.find({}, {'_id': 0}))
    return []

@app.route('/api/generate-quote', methods=['POST'])
def generate_quote():
    try:
        data = request.get_json()
        
        # Extract data
        dimensions = data.get('dimensions', {})
        noise_data = data.get('noiseData', {})
        blockages = data.get('blockages', {})
        room_type = data.get('roomType')

        # Validate required data
        if not all([dimensions.get(d) for d in ['length', 'width', 'height']]):
            return jsonify({'error': 'Missing room dimensions'}), 400
        if not all([noise_data.get(n) for n in ['type', 'intensity', 'direction']]):
            return jsonify({'error': 'Missing noise data'}), 400

        # Determine solution types based on noise data
        noise_priority = determine_noise_priority(noise_data)
        affected_surfaces = get_affected_surfaces(noise_data['direction'])
        
        # Generate recommendations
        recommendations = generate_recommendations(
            noise_priority=noise_priority,
            affected_surfaces=affected_surfaces,
            noise_type=noise_data['type']
        )

        # Calculate costs for each recommended solution
        costs = calculate_solution_costs(
            recommendations=recommendations,
            dimensions=dimensions,
            blockages=blockages
        )

        # Generate implementation details
        implementation = generate_implementation_details(
            recommendations=recommendations,
            dimensions=dimensions,
            noise_data=noise_data
        )

        return jsonify({
            'recommendations': recommendations,
            'costs': costs,
            'implementation': implementation
        })

    except Exception as e:
        app.logger.error(f"Error generating quote: {str(e)}")
        return jsonify({'error': 'Failed to generate quote'}), 500

def determine_noise_priority(noise_data):
    """Determine the priority level of noise treatment needed."""
    priority = 'medium'
    
    # High priority cases
    if (
        int(noise_data.get('intensity', 3)) >= 4 or  # High/Very High intensity
        'night' in noise_data.get('time', []) or     # Night-time noise
        noise_data.get('type') in ['music', 'machinery']  # Specific noise types
    ):
        priority = 'high'
    # Low priority cases
    elif (
        int(noise_data.get('intensity', 3)) <= 2 and  # Low/Very Low intensity
        'night' not in noise_data.get('time', [])     # Not night-time
    ):
        priority = 'low'
    
    return priority

def get_affected_surfaces(directions):
    """Determine which surfaces need treatment based on noise directions."""
    surfaces = {
        'walls': [],
        'floor': False,
        'ceiling': False
    }
    
    for direction in directions:
        if direction == 'above':
            surfaces['ceiling'] = True
        elif direction == 'below':
            surfaces['floor'] = True
        elif direction in ['north', 'east', 'south', 'west']:
            surfaces['walls'].append(direction)
    
    return surfaces

def generate_recommendations(noise_priority, affected_surfaces, noise_type):
    """Generate recommended solutions based on requirements."""
    solutions = {
        'wall': {
            'standard': ['M20WallStandard', 'GenieClipWallStandard', 'ResilientBarWallStandard', 'IndependentWallStandard'],
            'premium': ['M20WallSP15', 'GenieClipWallSP15', 'ResilientBarWallSP15', 'IndependentWallSP15']
        },
        'ceiling': {
            'standard': ['ResilientBarCeilingStandard'],
            'premium': ['ResilientBarCeilingSP15']
        }
    }

    recommendations = {
        'primary': {
            'walls': [],
            'ceiling': None,
            'floor': None,
            'reasoning': []
        },
        'alternatives': []
    }

    # Select solutions based on priority
    solution_tier = 'premium' if noise_priority == 'high' else 'standard'
    
    # Wall solutions
    if affected_surfaces['walls']:
        wall_solution = solutions['wall'][solution_tier][0]  # Primary solution
        recommendations['primary']['walls'] = [
            {'wall': wall, 'solution': wall_solution}
            for wall in affected_surfaces['walls']
        ]
        recommendations['primary']['reasoning'].append(
            f"Selected {wall_solution} for {', '.join(affected_surfaces['walls'])} walls based on {noise_priority} priority noise"
        )
        
        # Add alternative wall solutions
        for alt_solution in solutions['wall'][solution_tier][1:]:
            recommendations['alternatives'].append({
                'type': 'wall',
                'solution': alt_solution,
                'description': get_solution_description(alt_solution)
            })

    # Ceiling solution
    if affected_surfaces['ceiling']:
        ceiling_solution = solutions['ceiling'][solution_tier][0]
        recommendations['primary']['ceiling'] = ceiling_solution
        recommendations['primary']['reasoning'].append(
            f"Selected {ceiling_solution} for ceiling due to noise from above"
        )

    # Add noise-specific reasoning
    recommendations['primary']['reasoning'].append(
        get_noise_type_reasoning(noise_type)
    )

    return recommendations

def calculate_solution_costs(recommendations, dimensions, blockages):
    """Calculate costs for recommended solutions."""
    costs = {
        'wall': 0,
        'floor': 0,
        'ceiling': 0,
        'total': 0
    }

    # Calculate wall costs
    for wall_rec in recommendations['primary'].get('walls', []):
        solution_class = get_solution_class(wall_rec['solution'])
        if solution_class:
            calculator = solution_class(
                length=dimensions['length'],
                height=dimensions['height']
            )
            wall_costs = calculator.calculate(get_solution_materials(wall_rec['solution']))
            if wall_costs:
                costs['wall'] += sum(item['total_cost'] for item in wall_costs)

    # Calculate ceiling costs
    ceiling_solution = recommendations['primary'].get('ceiling')
    if ceiling_solution:
        solution_class = get_solution_class(ceiling_solution)
        if solution_class:
            calculator = solution_class(
                length=dimensions['length'],
                height=dimensions['width']  # For ceiling, height is room width
            )
            ceiling_costs = calculator.calculate(get_solution_materials(ceiling_solution))
            if ceiling_costs:
                costs['ceiling'] = sum(item['total_cost'] for item in ceiling_costs)

    # Calculate total
    costs['total'] = costs['wall'] + costs['floor'] + costs['ceiling']
    
    return costs

def generate_implementation_details(recommendations, dimensions, noise_data):
    """Generate implementation details for the recommended solutions."""
    skill_levels = {
        'M20WallStandard': 'Intermediate',
        'GenieClipWallStandard': 'Professional',
        'ResilientBarWallStandard': 'Professional',
        'IndependentWallStandard': 'Professional',
        'ResilientBarCeilingStandard': 'Professional'
    }

    # Get primary solution for skill level
    primary_solution = (
        recommendations['primary']['walls'][0]['solution'] 
        if recommendations['primary']['walls'] 
        else recommendations['primary'].get('ceiling')
    )

    # Calculate total area for time estimate
    wall_area = sum(
        dimensions['length'] * dimensions['height'] 
        for _ in recommendations['primary'].get('walls', [])
    )
    ceiling_area = (
        dimensions['length'] * dimensions['width'] 
        if recommendations['primary'].get('ceiling') 
        else 0
    )
    total_area = wall_area + ceiling_area

    # Estimate installation time (1 day per 20m² plus setup/cleanup)
    install_days = math.ceil(total_area / 20) + 1

    # Determine special requirements
    special_reqs = []
    if int(noise_data.get('intensity', 3)) >= 4:
        special_reqs.append('Enhanced ventilation during installation')
    if noise_data.get('type') in ['music', 'machinery']:
        special_reqs.append('Vibration testing recommended')

    return {
        'installTime': f"{install_days} days",
        'skillLevel': skill_levels.get(primary_solution, 'Professional'),
        'specialRequirements': special_reqs
    }

def get_solution_class(solution_name):
    """Get the calculator class for a solution."""
    solution_classes = {
        'M20WallStandard': M20WallStandard,
        'M20WallSP15': M20WallSP15,
        'GenieClipWallStandard': GenieClipWallStandard,
        'GenieClipWallSP15': GenieClipWallSP15,
        'ResilientBarWallStandard': ResilientBarWallStandard,
        'ResilientBarWallSP15': ResilientBarWallSP15,
        'IndependentWallStandard': IndependentWallStandard,
        'IndependentWallSP15': IndependentWallSP15,
        'ResilientBarCeilingStandard': ResilientBarCeilingStandard,
        'ResilientBarCeilingSP15': ResilientBarCeilingSP15
    }
    return solution_classes.get(solution_name)

def get_solution_materials(solution_name):
    """Get the list of materials for a solution."""
    # This would be replaced with actual material data from your database
    return []  # Placeholder

def get_solution_description(solution):
    """Get the description for a solution."""
    descriptions = {
        'M20WallStandard': 'Standard double-layer solution with excellent cost-effectiveness',
        'GenieClipWallStandard': 'Premium isolation using specialized clip system',
        'ResilientBarWallStandard': 'Effective decoupling using resilient bars',
        'IndependentWallStandard': 'Maximum isolation with independent wall construction',
        'M20WallSP15': 'Enhanced performance with SP15 sound board',
        'GenieClipWallSP15': 'Maximum performance clip system with SP15',
        'ResilientBarWallSP15': 'Enhanced bar system with SP15 upgrade',
        'IndependentWallSP15': 'Premium independent wall with SP15 enhancement',
        'ResilientBarCeilingStandard': 'Standard ceiling isolation system',
        'ResilientBarCeilingSP15': 'Enhanced ceiling system with SP15'
    }
    return descriptions.get(solution, 'Custom solution')

def get_noise_type_reasoning(noise_type):
    """Get the reasoning for a noise type."""
    reasonings = {
        'speech': 'Optimized for voice frequency ranges (100Hz-8kHz)',
        'music': 'Enhanced low frequency treatment for music and bass',
        'tv': 'Balanced treatment for mixed media frequencies',
        'traffic': 'Focus on low-mid frequency road noise reduction',
        'aircraft': 'Enhanced high frequency and impact noise treatment',
        'footsteps': 'Specialized impact noise reduction',
        'furniture': 'Impact noise and structural transmission reduction',
        'machinery': 'Vibration isolation and broadband noise treatment'
    }
    return reasonings.get(noise_type, 'General purpose noise reduction')

def get_solution_id_from_display_name(display_name):
    """Convert display name to solution ID."""
    name_to_id = {
        'M20 Solution (Standard)': 'M20WallStandard',
        'M20 Solution (SP15 Soundboard upgrade)': 'M20WallSP15',
        'Genie Clip wall (Standard)': 'GenieClipWallStandard',
        'Genie Clip wall (SP15 Soundboard Upgrade)': 'GenieClipWallSP15',
        'Independent Wall (Standard)': 'IndependentWallStandard',
        'Independent Wall (SP15 Soundboard Upgrade)': 'IndependentWallSP15',
        'Resilient bar wall (Standard)': 'ResilientBarWallStandard',
        'Resilient bar wall (SP15 Soundboard Upgrade)': 'ResilientBarWallSP15'
    }
    return name_to_id.get(display_name)

@app.route('/api/calculate-costs', methods=['POST'])
def calculate_costs():
    try:
        data = request.get_json()
        logger.info(f"Received calculate-costs request with data: {data}")
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['solution', 'dimensions', 'surfaceType']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        solution_name = data['solution']
        dimensions = data['dimensions']
        surface_type = data['surfaceType']
        wall = data.get('wall')  # Optional

        # Validate dimensions
        if not all(key in dimensions for key in ['length', 'width', 'height']):
            return jsonify({'error': 'Invalid dimensions provided'}), 400

        # Calculate area and perimeter
        area = 0
        perimeter = 0
        if surface_type == 'wall':
            if wall in ['north', 'south']:
                area = dimensions['width'] * dimensions['height']
                perimeter = 2 * (dimensions['width'] + dimensions['height'])
            elif wall in ['east', 'west']:
                area = dimensions['length'] * dimensions['height']
                perimeter = 2 * (dimensions['length'] + dimensions['height'])
        elif surface_type in ['ceiling', 'floor']:
            area = dimensions['length'] * dimensions['width']
            perimeter = 2 * (dimensions['length'] + dimensions['width'])

        if not area or area <= 0:
            return jsonify({'error': 'Invalid area calculation'}), 400

        # Get solution data from database
        solution = db.solutions.find_one({'name': solution_name})
        if not solution:
            logger.error(f"Could not find solution: {solution_name}")
            return jsonify({'error': 'Solution not found'}), 404

        # Calculate costs for each material
        total_cost = 0
        materials_costs = []

        for material in solution['materials']:
            coverage = float(material['coverage'])
            needs_wastage = material['name'] in [
                'Premium Acoustic Panel',
                'Dampening Material',
                '12.5mm Sound Plasterboard',
                'SP15 Soundboard',
                'Rockwool RWA45 50mm',
                'Rockwool RW3 100mm'
            ]
            is_perimeter_based = material['name'] in [
                'Acoustic Sealant',
                'Acoustic Mastic'
            ]

            if is_perimeter_based:
                amount = math.ceil(perimeter / coverage)
            else:
                calc_area = area * 1.1 if needs_wastage else area
                amount = math.ceil(calc_area / coverage)

            cost = amount * material['cost']
            total_cost += cost

            materials_costs.append({
                'name': material['name'],
                'amount': amount,
                'unit': material['unit'],
                'cost': cost
            })

        # Add labor cost
        labor_units = math.ceil(area / 10)  # 1 unit per 10m²
        labor_cost = labor_units * solution['labor_rate']
        total_cost += labor_cost

        materials_costs.append({
            'name': 'Installation Labor',
            'amount': labor_units,
            'unit': 'hours',
            'cost': labor_cost
        })

        return jsonify({
            'costs': materials_costs,
            'total': total_cost,
            'area': area,
            'perimeter': perimeter
        })

    except Exception as e:
        logger.error(f'Error calculating costs: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)