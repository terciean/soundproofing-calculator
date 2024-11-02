from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import logging
import sys
from pymongo import MongoClient
import certifi
from pymongo.server_api import ServerApi

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
WALL_SOLUTIONS = [
    "Independent Wall (Standard)",
    "Independent Wall (SP15 Soundboard Upgrade)",
    "Resilient bar wall (Standard)",
    "Resilient bar wall (SP15 Soundboard Upgrade)",
    "Genie Clip wall (Standard)",
    "Genie Clip wall (SP15 Soundboard Upgrade)",
    "M20 Solution (Standard)",
    "M20 Solution (SP15 Soundboard upgrade)"
]

CEILING_SOLUTIONS = [
    "Independent Ceiling",
    "Independent Ceiling (SP15 Soundboard Upgrade)",
    "Genie Clip ceiling",
    "Genie Clip ceiling (SP15 Soundboard Upgrade)",
    "LB3 Genie Clip",
    "LB3 Genie Clip (SP15 Soundboard Upgrade)",
    "Resilient bar Ceiling",
    "Resilient bar Ceiling (SP15 Soundboard Upgrade)"
]

# MongoDB setup
try:
    MONGODB_URI = os.getenv('MONGODB_URI')
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI environment variable not set")
    
    client = MongoClient(
        MONGODB_URI,
        server_api=ServerApi('1'),
        tls=True,
        tlsCAFile=certifi.where()
    )
    
    # Test connection
    client.admin.command('ping')
    
    # Define database and collections
    db = client["soundproofing"]
    wallsolutions = db["wallsolutions"]
    ceilingsolutions = db["ceilingsolutions"]
    
    logger.info("Successfully connected to MongoDB Atlas!")
    
except Exception as e:
    logger.error(f"MongoDB Connection Error: {e}")
    sys.exit(1)

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
calculator_path = os.path.join(current_dir, 'solutions')
sys.path.append(calculator_path)

# Import solutions
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

    logger.info("Successfully imported wall and ceiling solutions")
except ImportError as e:
    logger.error(f"Import Error: {e}")
    raise

# Calculator mapping
CALCULATORS = {
    'Independent Wall (Standard)': IndependentWallStandard,
    'Independent Wall (SP15 Soundboard Upgrade)': IndependentWallSP15,
    'Resilient bar wall (Standard)': ResilientBarWallStandard,
    'Resilient bar wall (SP15 Soundboard Upgrade)': ResilientBarWallSP15,
    'Genie Clip wall (Standard)': GenieClipWallStandard,
    'Genie Clip wall (SP15 Soundboard Upgrade)': GenieClipWallSP15,
    'M20 Solution (Standard)': M20WallStandard,
    'M20 Solution (SP15 Soundboard upgrade)': M20WallSP15,
    'Independent Ceiling': IndependentCeilingStandard,
    'Independent Ceiling (SP15 Soundboard Upgrade)': IndependentCeilingSP15,
    'Genie Clip ceiling': GenieClipCeilingStandard,
    'Genie Clip ceiling (SP15 Soundboard Upgrade)': GenieClipCeilingSP15,
    'LB3 Genie Clip': LB3GenieClipCeilingStandard,
    'LB3 Genie Clip (SP15 Soundboard Upgrade)': LB3GenieClipCeilingSP15,
    'Resilient bar Ceiling': ResilientBarCeilingStandard,
    'Resilient bar Ceiling (SP15 Soundboard Upgrade)': ResilientBarCeilingSP15
}

# Routes
@app.route('/get_solutions/<surface_type>')
def get_solutions(surface_type):
    try:
        logger.info(f"Getting solutions for surface type: {surface_type}")
        
        if surface_type == 'walls':
            solutions = WALL_SOLUTIONS
        elif surface_type == 'ceilings':
            solutions = CEILING_SOLUTIONS
        else:
            logger.error(f"Invalid surface type: {surface_type}")
            return jsonify([]), 400
            
        logger.info(f"Found {len(solutions)} solutions")
        logger.info(f"Solutions: {solutions}")
        
        return jsonify(solutions)
        
    except Exception as e:
        logger.error(f"Error in get_solutions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    try:
        client.admin.command('ping')
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.errorhandler(500)
def handle_500(e):
    logger.error(f"Server error: {str(e)}")
    return render_template('index.html', 
                         error="Server Error",
                         message="An internal server error occurred.",
                         solution_types=list(CALCULATORS.keys()))

@app.errorhandler(404)
def handle_404(e):
    return render_template('index.html',
                         error="Not Found",
                         message="The requested page was not found.",
                         solution_types=list(CALCULATORS.keys()))

@app.route('/', methods=['GET', 'POST'])
def index():
    solution_types = list(CALCULATORS.keys())

    if request.method == 'POST':
        try:
            # Get form data
            length = float(request.form.get('length'))
            height = float(request.form.get('height'))
            solution_type = request.form.get('solutionType')
            surface_type = request.form.get('surfaceType')
            fitting_days = int(request.form.get('fittingDays', 0))
            removal_required = request.form.get('removalRequired') == 'yes'

            # Add error checking for removal dimensions
            if removal_required:
                removal_length = float(request.form.get('removalLength', 0))
                removal_height = float(request.form.get('removalHeight', 0))
                if removal_length <= 0 or removal_height <= 0:
                    raise ValueError("Invalid removal dimensions")

            # Get solution from database
            if surface_type == 'walls':
                collection = wallsolutions
            else:
                collection = ceilingsolutions
            
            solution = collection.find_one({'solution': solution_type})
            if not solution:
                logger.error("Solution not found in database.")
                return render_template('index.html',
                                    error="Invalid solution",
                                    message="The selected solution was not found in the database.",
                                    solution_types=solution_types)

            # Get calculator class
            calculator_class = CALCULATORS.get(solution_type)
            if not calculator_class:
                logger.error("Calculator class not found.")
                return render_template('index.html',
                                    error="Invalid solution type",
                                    message="The selected solution type is not supported.",
                                    solution_types=solution_types)

            # Calculate results
            calculator = calculator_class(length, height)
            results = calculator.calculate(solution['materials'])

            if not results:
                logger.error("Calculation failed.")
                return render_template('index.html',
                                    error="Calculation failed",
                                    message="Failed to calculate materials. Please try again.",
                                    solution_types=solution_types)

            # Add fitting fee if requested
            if fitting_days > 0:
                fitting_cost = fitting_days * 685.00
                results.append({
                    'name': f'Installation Fee ({fitting_days} days)',
                    'quantity': fitting_days,
                    'unit_cost': 685.00,
                    'total_cost': fitting_cost,
                    'coverage': 'Per Day'
                })

            # Add removal fee if requested
            if removal_required:
                area = length * height
                removal_cost = area * 25.00
                results.append({
                    'name': 'Removal Fee',
                    'quantity': area,
                    'unit_cost': 25.00,
                    'total_cost': removal_cost,
                    'coverage': 'Per m²'
                })

            return render_template('index.html', 
                                results=results,
                                area=length * height,
                                solution_type=solution_type,
                                solution=solution,
                                solution_types=solution_types)

        except Exception as e:
            logger.error(f"Error during calculation: {str(e)}")
            return render_template('index.html',
                                error="Calculation Error",
                                message=f"An error occurred: {str(e)}",
                                solution_types=solution_types)

    # If GET request, render the form with all solution types
    return render_template('index.html', solution_types=solution_types)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)