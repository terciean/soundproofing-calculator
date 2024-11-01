from pymongo import MongoClient
import json

print("Starting data export process...")

try:
    # Connect to local MongoDB
    print("Connecting to local MongoDB...")
    local_client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    
    # Test connection
    local_client.server_info()
    print("Connected to local MongoDB successfully!")
    
    local_db = local_client["soundproofing"]
    
    # Exact collection names
    collections = ['ceilingsolutions', 'floorsolutions', 'wallsolutions']
    
    for collection_name in collections:
        print(f"\nExporting {collection_name}...")
        collection = local_db[collection_name]
        
        try:
            # Get all documents from collection
            solutions = list(collection.find({}, {'_id': 0}))
            print(f"Found {len(solutions)} solutions in {collection_name}")
            
            if solutions:
                filename = f"{collection_name}.json"
                with open(filename, 'w') as f:
                    json.dump(solutions, f, indent=2)
                print(f"Exported to {filename}")
                # Print first solution as sample
                print(f"Sample solution: {solutions[0]['solution'] if solutions else 'No solutions'}")
            else:
                print(f"No solutions found in {collection_name}")
                
        except Exception as e:
            print(f"Error exporting {collection_name}: {str(e)}")
    
    print("\nExport completed!")
    
    # Print summary
    print("\nExport Summary:")
    for collection_name in collections:
        try:
            with open(f"{collection_name}.json", 'r') as f:
                data = json.load(f)
                print(f"{collection_name}: {len(data)} solutions exported")
        except FileNotFoundError:
            print(f"{collection_name}: No file created")
        except json.JSONDecodeError:
            print(f"{collection_name}: File created but empty or invalid")

except Exception as e:
    print(f"\nError during export: {str(e)}")
    print("Please make sure your local MongoDB is running and accessible")
    print("\nDetailed error:")
    import traceback
    print(traceback.format_exc())