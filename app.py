from flask import Flask, render_template, request, jsonify
import sys
import os
import logging
from pymongo import MongoClient
from bson import json_util  # Use this instead of importing bson directly
from dotenv import load_dotenv

# Remove duplicate Flask initialization
app = Flask(__name__)
# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Setup logging
# MongoDB setup with error handling
# MongoDB setup with error handling
# MongoDB setup with error handling
try:
    MONGODB_URI = os.getenv('MONGODB_URI')
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI environment variable not set")
    
    # Updated connection with correct SSL/TLS options
    client = MongoClient(
        MONGODB_URI,
        tls=True,
        tlsAllowInvalidCertificates=True,
        retryWrites=True,
        serverSelectionTimeoutMS=10000,
        connect=True
    )
    
    # Test connection with longer timeout
    client.admin.command('ping', serverSelectionTimeoutMS=10000)
    logger.info("Successfully connected to MongoDB Atlas!")
except Exception as e:
    logger.error(f"MongoDB Connection Error: {e}")
    raise

# Database and collections
db = client["soundproofing"]
wallsolutions = db["wallsolutions"]
ceilingsolutions = db["ceilingsolutions"]

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
calculator_path = os.path.join(current_dir, 'solutions')
sys.path.append(calculator_path)

# Rest of your existing code...

# Initialize Flask
app = Flask(__name__)

# MongoDB setup


# Add MongoDB collection debug info
logger.debug("=== MONGODB COLLECTIONS ===")
logger.debug("Available collections:")
for collection_name in db.list_collection_names():
    logger.debug(f"- {collection_name}")
logger.debug("\nSolutions contents:")
for doc in wallsolutions.find():
    logger.debug(f"- Solution: {doc.get('solution')}, Surface: {doc.get('surface_type')}")
for doc in ceilingsolutions.find():
    logger.debug(f"- Solution: {doc.get('solution')}, Surface: {doc.get('surface_type')}")

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

    print("Successfully imported wall and ceiling solutions")
except ImportError as e:
    print(f"Import Error: {e}")
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
    'Resilient bar Ceiling': ResilientBarCeilingStandard,  # Changed to match MongoDB
    'Resilient bar Ceiling (SP15 Soundboard Upgrade)': ResilientBarCeilingSP15  # Changed to match MongoDB
}

@app.route('/get_solutions/<surface_type>')
def get_solutions(surface_type):
    if surface_type == 'walls':
        collection = wallsolutions
    elif surface_type == 'ceilings':
        collection = ceilingsolutions
    else:
        return jsonify([])
    
    solutions = list(collection.find({'surface_type': surface_type}, {'solution': 1, '_id': 0}))
    return jsonify([s['solution'] for s in solutions])

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

            # Add more detailed logging
            logger.debug(f"\nForm Data:")
            logger.debug(f"Length: {length}")
            logger.debug(f"Height: {height}")
            logger.debug(f"Solution Type: {solution_type}")
            logger.debug(f"Surface Type: {surface_type}")
            logger.debug(f"Fitting Days: {fitting_days}")
            logger.debug(f"Removal Required: {removal_required}")

            # Add error checking for removal dimensions
            if removal_required:
                removal_length = float(request.form.get('removalLength', 0))
                removal_height = float(request.form.get('removalHeight', 0))
                logger.debug(f"Removal Length: {removal_length}")
                logger.debug(f"Removal Height: {removal_height}")
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
                logger.debug(f"Added fitting fee: £{fitting_cost}")

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
                logger.debug(f"Added removal fee: £{removal_cost}")

            logger.debug("Calculation successful. Rendering results.")
            # Return results on the same page, along with solution types
            return render_template('index.html', 
                                results=results,
                                area=length * height,
                                solution_type=solution_type,
                                solution=solution,
                                solution_types=solution_types)

        except Exception as e:
            # More detailed error logging
            logger.error(f"Error during calculation:")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            return render_template('index.html',
                                error="Calculation Error",
                                message=f"An error occurred: {str(e)}",
                                solution_types=solution_types)

    # If GET request, render the form with all solution types
    return render_template('index.html', solution_types=solution_types)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)