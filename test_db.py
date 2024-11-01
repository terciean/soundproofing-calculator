print("Starting test...")

try:
    from pymongo.mongo_client import MongoClient
    print("1. MongoDB import successful")
except Exception as e:
    print(f"Error importing MongoDB: {e}")
    exit()

try:
    from dotenv import load_dotenv
    import os
    print("2. dotenv import successful")
except Exception as e:
    print(f"Error importing dotenv: {e}")
    exit()

try:
    load_dotenv()
    print("3. .env file loaded")
except Exception as e:
    print(f"Error loading .env: {e}")
    exit()

try:
    uri = os.getenv('MONGODB_URI')
    print(f"4. MongoDB URI found: {uri[:20]}...")  # Only show start of URI for security
except Exception as e:
    print(f"Error getting URI: {e}")
    exit()

try:
    print("5. Attempting connection...")
    client = MongoClient(uri)
    client.admin.command('ping')
    print("6. Connection successful!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()