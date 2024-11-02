import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys

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
            raise ValueError("MONGODB_URI environment variable is not set.")
        
        client = MongoClient(mongodb_uri)
        db = client.guyrazor  # Use the correct database name
        wallsolutions = db.wallsolutions
        ceilingsolutions = db.ceilingsolutions

        # Test connection
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB!")
        logger.info(f"Wall solutions count: {wallsolutions.count_documents({})}")
        logger.info(f"Ceiling solutions count: {ceilingsolutions.count_documents({})}")

        return client, db, wallsolutions, ceilingsolutions

    except Exception as e:
        logger.error(f"MongoDB Connection Error: {str(e)}")
        raise

# Initialize MongoDB and Flask
try:
    client, db, wallsolutions, ceilingsolutions = setup_mongodb()
    app = Flask(__name__)
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


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        # Get solutions from MongoDB
        wall_solutions = list(wallsolutions.find({}, {'solution': 1, '_id': 0}))
        ceiling_solutions = list(ceilingsolutions.find({}, {'solution': 1, '_id': 0}))
        
        # Extract solution names
        wall_solution_names = [s['solution'] for s in wall_solutions]
        ceiling_solution_names = [s['solution'] for s in ceiling_solutions]
        
        # Combine all solutions for the template
        solution_types = wall_solution_names + ceiling_solution_names

        if request.method == 'POST':
            length = float(request.form['length'])
            height = float(request.form['height'])
            solution_type = request.form['solutionType']
            fitting_days = int(request.form['fittingDays'])
            removal_required = request.form['removalRequired']
            
            # Calculate area
            area = length * height
            
            # Get the appropriate calculator class
            calculator_class = CALCULATORS.get(solution_type)
            if not calculator_class:
                raise ValueError(f"Invalid solution type: {solution_type}")
            
            # Initialize calculator
            calculator = calculator_class(length, height)
            
            # Get solution details from MongoDB
            collection = wallsolutions if "wall" in solution_type.lower() else ceilingsolutions
            solution = collection.find_one({"solution": solution_type})
            
            if not solution:
                raise ValueError(f"Solution not found in database: {solution_type}")
            
            # Calculate materials
            results = calculator.calculate(solution['materials'])
            
            # Add installation fee if selected
            if fitting_days > 0:
                results.append({
                    'name': f'Installation Fee ({fitting_days} days)',
                    'quantity': fitting_days,
                    'unit_cost': 685.0,
                    'total_cost': fitting_days * 685.0
                })
            
            # Add removal fee if selected
            if removal_required == 'yes':
                removal_length = float(request.form['removalLength'])
                removal_height = float(request.form['removalHeight'])
                removal_area = removal_length * removal_height
                removal_cost = removal_area * 25.0  # £25 per m²
                
                results.append({
                    'name': 'Removal Fee',
                    'quantity': removal_area,
                    'unit_cost': 25.0,
                    'total_cost': removal_cost
                })
            
            return render_template('index.html',
                                solution_types=solution_types,
                                surface_types=['walls', 'ceilings'],
                                results=results,
                                solution_type=solution_type,
                                solution=solution,
                                area=area)
            
        return render_template('index.html', 
                             solution_types=solution_types,
                             surface_types=['walls', 'ceilings'])
                             
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return render_template('index.html', 
                             error="Error processing request",
                             message=str(e),
                             solution_types=solution_types,
                             surface_types=['walls', 'ceilings'])
@app.route('/get_solutions/<surface_type>')
def get_solutions(surface_type):
    try:
        logger.info(f"Fetching solutions for surface_type: {surface_type}")
        
        # Select collection based on surface type
        collection = wallsolutions if surface_type == 'walls' else ceilingsolutions
        
        # Simple query - just get all solutions from the correct collection
        solutions = list(collection.find({}, {'solution': 1, '_id': 0}))
        
        # Extract solution names
        solution_names = [doc["solution"] for doc in solutions]
        logger.info(f"Solution names: {solution_names}")
        
        return jsonify(solution_names)
        
    except Exception as e:
        logger.error(f"Error fetching solutions: {str(e)}")
        return jsonify({'error': str(e)}), 500
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
                         solution_types=[],  # Changed this line
                         surface_types=['walls', 'ceilings'])

@app.errorhandler(404)
def handle_404(e):
    return render_template('index.html',
                         error="Not Found",
                         message="The requested page was not found.",
                         solution_types=[],  # Changed this line
                         surface_types=['walls', 'ceilings'])
if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)