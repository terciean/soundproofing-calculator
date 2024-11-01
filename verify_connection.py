print("=== MongoDB Connection Test ===")

# 1. Check environment variable
import os
from dotenv import load_dotenv

print("Loading .env file...")
load_dotenv()

uri = os.getenv('MONGODB_URI')
if not uri:
    print("ERROR: MONGODB_URI not found in .env file")
    exit()

print(f"Found URI: {uri}")

# 2. Test connection
from pymongo.mongo_client import MongoClient

print("\nTesting connection...")
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")