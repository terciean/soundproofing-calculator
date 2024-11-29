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
# Add debug logging for imports
print("Starting Room import...")
try:
    from solutions.room import Room
    print("Room import successful")
except Exception as e:
    print(f"Room import failed: {str(e)}")
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
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            logger.warning("MONGODB_URI not set, using fallback data")
            return setup_fallback_data()
        
        # Increased timeouts and added retry options
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
            # Add connection pool settings
            maxIdleTimeMS=45000,
            heartbeatFrequencyMS=10000
        )
        
        # Test connection with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                db = client.guyrazor
                # Quick test query
                db.wallsolutions.find_one({})
                logger.info("Successfully connected to MongoDB!")
                return client, db, db.wallsolutions, db.ceilingsolutions
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed to connect after {max_retries} attempts: {str(e)}")
                    return setup_fallback_data()
                logger.warning(f"Connection attempt {attempt + 1} failed, retrying...")
                time.sleep(2)  # Wait before retry

    except Exception as e:
        logger.error(f"MongoDB Connection Error: {str(e)}")
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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)