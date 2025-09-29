import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import os
from dotenv import load_dotenv

def test_mongodb_connection():
    """Test MongoDB connection and database structure"""
    client = None
    try:
        # Load environment variables
        load_dotenv()
        
        # Get MongoDB URI from environment
        mongo_uri = os.getenv('MONGODB_URI')
        if not mongo_uri:
            raise ValueError("MONGODB_URI not found in environment variables")
            
        print("Attempting to connect to MongoDB...")
        
        # Create client with server selection timeout
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("MongoDB connection successful")
        
        # List all databases
        database_names = client.list_database_names()
        print(f"Available databases: {database_names}")
        
        # Try each database to find our collections
        found_collections = {}
        for db_name in database_names:
            if db_name in ['admin', 'local', 'config']:
                continue  # Skip system databases
                
            db = client.get_database(db_name)
            collection_names = db.list_collection_names()
            print(f"Collections in '{db_name}': {collection_names}")
            
            # Check for our target collections
            targets = ['wallsolutions', 'ceilingsolutions', 'materials', 'wall_solutions', 'ceiling_solutions', 'floor_solutions']
            for target in targets:
                for coll_name in collection_names:
                    if target.lower() in coll_name.lower():
                        found_collections[target] = f"{db_name}.{coll_name}"
                        # Test count
                        count = db.get_collection(coll_name).count_documents({})
                        print(f"Collection '{db_name}.{coll_name}' has {count} documents")
        
        print(f"Found collections: {found_collections}")
        return True
        
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {str(e)}", file=sys.stderr)
        return False
    except OperationFailure as e:
        print(f"MongoDB operation failed: {str(e)}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error testing MongoDB connection: {str(e)}", file=sys.stderr)
        return False
    finally:
        if client:
            client.close()

def test_collection_data(db_name, collection_name):
    """Test retrieving data from a specific collection"""
    client = None
    try:
        # Load environment variables
        load_dotenv()
        
        # Get MongoDB URI
        mongo_uri = os.getenv('MONGODB_URI')
        if not mongo_uri:
            raise ValueError("MONGODB_URI not found in environment variables")
            
        # Create client with server selection timeout
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client.get_database(db_name)
        
        # Get and display sample data
        collection = db.get_collection(collection_name)
        count = collection.count_documents({})
        print(f"Collection '{db_name}.{collection_name}' has {count} documents")
        
        if count > 0:
            sample = list(collection.find({}).limit(1))[0]
            print(f"Sample document from '{db_name}.{collection_name}':")
            for key, value in sample.items():
                print(f"  {key}: {value}")
            
        return True
        
    except Exception as e:
        print(f"Error retrieving data from '{db_name}.{collection_name}': {str(e)}", file=sys.stderr)
        return False
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    print("Starting MongoDB connection tests...")
    
    # Test connection and database structure
    connection_success = test_mongodb_connection()
    if connection_success:
        print("MongoDB connection test passed")
    else:
        print("MongoDB connection test failed", file=sys.stderr)
        
    # Check collections based on user input
    test_collection_data('guyrazor', 'wallsolutions')
    test_collection_data('guyrazor', 'ceilingsolutions')
    test_collection_data('guyrazor', 'materials')