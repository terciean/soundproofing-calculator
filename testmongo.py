from pymongo import MongoClient
import logging
import json
from pprint import pprint
import math

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mongodb_connection():
    try:
        # Connect to MongoDB Atlas
        client = MongoClient("mongodb+srv://thatguyrazor:bell12@cluster0.rxg93.mongodb.net/Cluster0?retryWrites=true&w=majority")
        db = client.guyrazor
        
        # Test collections
        collections = {
            'wallsolutions': db.wallsolutions,
            'ceilingsolutions': db.ceilingsolutions,
            'materials': db.materials
        }
        
        # Test each collection
        for name, collection in collections.items():
            logger.info(f"\nTesting {name} collection:")
            
            # Count documents
            count = collection.count_documents({})
            logger.info(f"Found {count} documents in {name}")
            
            # Sample documents
            documents = list(collection.find({}).limit(2))
            for doc in documents:
                logger.info(f"\nSample {name} document:")
                pprint(doc)
                
                # If this is a solution, test its material references
                if 'materials' in doc:
                    logger.info("\nTesting material references:")
                    for material in doc['materials']:
                        material_doc = db.materials.find_one({'name': material['name']})
                        if material_doc:
                            logger.info(f"Found material: {material['name']}")
                        else:
                            logger.warning(f"Missing material: {material['name']}")

        return True

    except Exception as e:
        logger.error(f"Connection Error: {str(e)}")
        return False

def test_solution_structure(solution_name):
    try:
        client = MongoClient("mongodb+srv://thatguyrazor:bell12@cluster0.rxg93.mongodb.net/Cluster0?retryWrites=true&w=majority")
        db = client.guyrazor
        
        # Find the solution
        solution = db.wallsolutions.find_one({'solution': solution_name})
        if not solution:
            solution = db.ceilingsolutions.find_one({'solution': solution_name})
        
        if solution:
            logger.info(f"\nTesting solution structure for: {solution_name}")
            logger.info("\nRequired fields:")
            required_fields = [
                'solution', 'display_name', 'materials', 
                'sound_reduction', 'stc_rating', 'frequency_range'
            ]
            
            for field in required_fields:
                logger.info(f"{field}: {'Present' if field in solution else 'Missing'}")
            
            logger.info("\nMaterial details:")
            for material in solution.get('materials', []):
                logger.info(f"\nMaterial: {material.get('name')}")
                logger.info(f"Coverage: {material.get('coverage')}m²")
                logger.info(f"Cost: £{material.get('cost')}")
            return True
        else:
            logger.error(f"Solution '{solution_name}' is missing or malformed in the database.")
            return False
    except Exception as e:
        logger.error(f"Error testing solution structure: {str(e)}")
        return False

def test_material_calculations(solution_name, dimensions):
    """Test material calculations for a solution"""
    try:
        client = MongoClient("mongodb+srv://thatguyrazor:bell12@cluster0.rxg93.mongodb.net/Cluster0?retryWrites=true&w=majority")
        db = client.guyrazor
        
        # Get solution data
        solution = None
        for collection in [db.wallsolutions, db.ceilingsolutions]:
            solution = collection.find_one({'solution': solution_name})
            if solution:
                break
        
        if not solution:
            logger.error(f"Solution {solution_name} not found")
            return
            
        area = dimensions['length'] * dimensions['height']
        logger.info(f"\nCalculating materials for {solution_name}")
        logger.info(f"Area: {area}m²")
        
        # Calculate material quantities
        total_cost = 0
        for material in solution['materials']:
            quantity = math.ceil(area / float(material['coverage'].strip().split()[0]))
            cost = quantity * float(material['cost'])
            total_cost += cost
            
            logger.info(f"\nMaterial: {material['name']}")
            logger.info(f"Quantity needed: {quantity}")
            logger.info(f"Cost: £{cost:.2f}")
            
        logger.info(f"\nTotal cost: £{total_cost:.2f}")
        
    except Exception as e:
        logger.error(f"Error in material calculations: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting MongoDB connection test...")
    if test_mongodb_connection():
        logger.info("\nConnection test successful!")
        
        # Test specific solutions
        test_solutions = [
            'M20WallStandard',
            'GenieClipWallSP15',
            'ResilientBarCeilingStandard'
        ]
        
        for solution in test_solutions:
            test_solution_structure(solution)
        
        # Test material calculations for a sample solution
        test_dimensions = {'length': 4, 'height': 2.4}
        test_material_calculations('M20 Solution (Standard)', test_dimensions)
    else:
        logger.error("Connection test failed!")