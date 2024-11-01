from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

# Get the connection string from .env
MONGODB_URI = os.getenv('MONGODB_URI')
print("Attempting to connect to MongoDB...")

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI)

try:
    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    
    # Test database access
    db = client["soundproofing"]
    
    # Count documents in collections
    wall_count = db.wallsolutions.count_documents({})
    ceiling_count = db.ceilingsolutions.count_documents({})
    
    print(f"Found {wall_count} wall solutions")
    print(f"Found {ceiling_count} ceiling solutions")
    
except Exception as e:
    print(f"An error occurred: {e}")