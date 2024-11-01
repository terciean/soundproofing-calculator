print("Starting test...")

from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv('MONGODB_URI')
print(f"Using connection string: {uri}")

try:
    print("\nConnecting to MongoDB...")
    client = MongoClient(uri)
    client.admin.command('ping')
    print("Connected successfully!")
    
    # Try to access and create a test collection
    db = client.soundproofing
    test = db.test.insert_one({"test": "test"})
    print("Database write test successful!")
    
    # Clean up test data
    db.test.delete_one({"test": "test"})
    
except Exception as e:
    print(f"Error: {e}")