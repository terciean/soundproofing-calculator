from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

# Get the connection string from .env
MONGODB_URI = os.getenv('MONGODB_URI')
print("Connection string loaded from .env")

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI)

try:
    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    
    # Try to access the database
    db = client.soundproofing
    print("Database accessed")
    
except Exception as e:
    print(f"Error: {e}")