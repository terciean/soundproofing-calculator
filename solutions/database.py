import os
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv

def get_db():
    """Get a connected MongoDB database object using environment variables."""
    load_dotenv()
    mongo_uri = os.getenv('MONGODB_URI')
    if not mongo_uri:
        raise ValueError("MONGODB_URI not found in environment variables")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    db_name = os.getenv('MONGODB_DB', 'guyrazor')
    return client.get_database(db_name)

def get_solution_by_id(collection_name: str, object_id: str):
    """Fetch a solution document by ObjectId or string from the specified collection. Auto-detects type."""
    db = get_db()
    collection = db.get_collection(collection_name)
    # Print collection name and sample IDs for debugging
    sample_ids = [str(doc['_id']) for doc in collection.find({}, {'_id': 1}).limit(5)]
    print(f"[DEBUG] Querying collection '{collection_name}'. Sample IDs: {sample_ids}")
    # Try ObjectId first, then string
    doc = None
    try:
        doc = collection.find_one({'_id': ObjectId(object_id)})
    except Exception:
        pass
    if not doc:
        doc = collection.find_one({'_id': object_id})
    db.client.close()
    return doc

def get_all_materials_from_db():
    """Fetch all materials from the 'materials' collection in MongoDB."""
    db = get_db()
    collection = db.get_collection('materials')
    materials = list(collection.find({}))
    print(f"[MATERIALS] Found {len(materials)} materials in MongoDB.")
    if materials:
        print(f"[MATERIALS] Sample material: {materials[0]}")
    db.client.close()
    return materials

def diagnose_missing_document(collection_name: str, object_id: str, max_sample: int = 5):
    """Prints a summary diagnostic if a document is missing in the given collection."""
    try:
        db = get_db()
        collection = db.get_collection(collection_name)
        count = collection.count_documents({})
        print(f"[DIAGNOSTIC] Collection '{collection_name}' has {count} documents.")
        if count > 0:
            sample_ids = [str(doc['_id']) for doc in collection.find({}, {'_id': 1}).limit(max_sample)]
            print(f"[DIAGNOSTIC] Sample IDs in '{collection_name}': {sample_ids}")
        else:
            print(f"[DIAGNOSTIC] Collection '{collection_name}' is empty.")
        print(f"[DIAGNOSTIC] Attempted to find document with _id: {object_id}")
        db.client.close()
    except Exception as e:
        print(f"[DIAGNOSTIC] Error during diagnostic for collection '{collection_name}': {e}") 