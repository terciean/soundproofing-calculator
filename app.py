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
        print(f"Loaded MongoDB URI: {mongodb_uri}")  # Debug: Print the loaded URI
        
        if not mongodb_uri:
            logger.warning("MONGODB_URI not set, using fallback data")
            return setup_fallback_data()
        
        # Initialize the MongoDB client with connection settings
        client = MongoClient(
            mongodb_uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000,  # Increased to 10 seconds
            connectTimeoutMS=10000,
            socketTimeoutMS=20000,
            retryWrites=True,
            retryReads=True,
            maxPoolSize=50,
            waitQueueTimeoutMS=10000,
            connect=True,  # Force initial connection
            maxIdleTimeMS=45000,
            heartbeatFrequencyMS=10000
        )
        
        # Debug: Test the MongoDB connection
        print("Testing MongoDB connection...")  # Debug: Connection test start
        client.server_info()  # Ensures the connection is valid
        print("MongoDB connection successful!")  # Debug: Connection success
        
        # Retrieve the database and collections
        db = client.guyrazor
        logger.info("Successfully connected to MongoDB!")
        return client, db, db.wallsolutions, db.ceilingsolutions

    except Exception as e:
        # Log and print the error
        logger.error(f"MongoDB Connection Error: {str(e)}")
        print(f"MongoDB Connection Error: {e}")  # Debug: Print error message
        
        # Fall back to local data if connection fails
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
    try:
        client.admin.command('ping')
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

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

@app.route('/api/calculate-costs', methods=['POST'])
def calculate_costs():
    try:
        data = request.get_json()
        solution_type = data.get('solution')
        dimensions = data.get('dimensions')

        # Log the request
        logger.info(f"Calculating costs for solution: {solution_type}")
        logger.info(f"Dimensions: {dimensions}")

        # Validate input
        if not solution_type or not dimensions:
            return jsonify({'error': 'Missing solution type or dimensions'}), 400

        # Determine which collection to query based on solution type
        collection = db.ceilingsolutions if 'ceiling' in solution_type.lower() else db.wallsolutions
        logger.info(f"Querying collection: {collection.name}")

        # Query the MongoDB collection directly first
        direct_match = collection.find_one({'solution': solution_type})
        if direct_match:
            logger.info(f"Found direct match: {direct_match}")
            solution_data = direct_match
        else:
            # Try case-insensitive search with escaped regex pattern
            solution_type_normalized = solution_type.lower().strip()
            logger.info(f"No direct match found, trying case-insensitive search for: {solution_type_normalized}")
            # Escape regex special characters
            solution_type_escaped = re.escape(solution_type_normalized)
            solution_data = collection.find_one({
                'solution': {'$regex': f'^{solution_type_escaped}$', '$options': 'i'}
            })

        if not solution_data:
            # Try to find similar solutions for better error message
            # Use the first word of the solution type for fuzzy matching
            first_word = solution_type_normalized.split()[0]
            first_word_escaped = re.escape(first_word)
            similar_solutions = list(collection.find(
                {'solution': {'$regex': f'.*{first_word_escaped}.*', '$options': 'i'}},
                {'solution': 1, '_id': 0}
            ).limit(3))
            
            error_msg = f"Solution type '{solution_type}' not found"
            if similar_solutions:
                error_msg += ". Did you mean one of these: " + ", ".join([s['solution'] for s in similar_solutions])
            
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 400

        # Get materials from the solution data
        materials = solution_data.get('materials', [])
        if not materials:
            logger.error(f"No materials found for solution {solution_type}")
            return jsonify({'error': 'No materials found for solution'}), 400

        # Calculate area
        area = float(dimensions.get('length', 0)) * float(dimensions.get('width', 0))
        
        # Calculate costs for each material
        costs = []
        total = 0
        
        for material in materials:
            quantity = math.ceil(area / float(material.get('coverage', 1)))
            cost = quantity * material['cost']
            costs.append({
                'name': material['name'],
                'quantity': quantity,
                'rate': material['cost'],
                'total_cost': cost
            })
            total += cost

        # Add labor cost (1 unit per 10m²)
        labor_units = math.ceil(area / 10)
        labor_rate = 40  # Default labor rate
        labor_cost = labor_units * labor_rate
        costs.append({
            'name': 'Installation Labor',
            'quantity': labor_units,
            'rate': labor_rate,
            'total_cost': labor_cost
        })
        total += labor_cost

        return jsonify({
            'costs': costs,
            'total': total
        })

    except Exception as e:
        logger.error(f"Error calculating costs: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)