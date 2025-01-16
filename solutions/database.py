from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB Atlas connection string from environment variable
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority')

# Initialize MongoDB client
client = MongoClient(MONGODB_URI)
db = client.soundproofing

# Initialize materials collection if it doesn't exist
if 'materials' not in db.list_collection_names():
    materials = [
        {
            'name': 'Acoustic Panels',
            'solution': 'StandardWallSP10',
            'cost_per_unit': 45,
            'unit': 'm²'
        },
        {
            'name': 'Sound Barrier',
            'solution': 'StandardWallSP10',
            'cost_per_unit': 35,
            'unit': 'm²'
        },
        {
            'name': 'Installation Materials',
            'solution': 'StandardWallSP10',
            'cost_per_unit': 15,
            'unit': 'm²'
        },
        {
            'name': 'Premium Acoustic Panels',
            'solution': 'PremiumWallSP15',
            'cost_per_unit': 75,
            'unit': 'm²'
        },
        {
            'name': 'High-Mass Barrier',
            'solution': 'PremiumWallSP15',
            'cost_per_unit': 55,
            'unit': 'm²'
        },
        {
            'name': 'Professional Installation Kit',
            'solution': 'PremiumWallSP15',
            'cost_per_unit': 25,
            'unit': 'm²'
        }
    ]
    db.materials.insert_many(materials)

# Initialize wall solutions collection if it doesn't exist
if 'wallsolutions' not in db.list_collection_names():
    solutions = [
        {
            'name': 'StandardWallSP10',
            'description': 'Standard Wall Treatment SP10',
            'sound_reduction': 45,
            'materials': ['Acoustic Panels', 'Sound Barrier', 'Installation Materials'],
            'labor_rate': 40
        },
        {
            'name': 'PremiumWallSP15',
            'description': 'Premium Wall Treatment SP15',
            'sound_reduction': 55,
            'materials': ['Premium Acoustic Panels', 'High-Mass Barrier', 'Professional Installation Kit'],
            'labor_rate': 60
        }
    ]
    db.wallsolutions.insert_many(solutions)

def get_db():
    return db 