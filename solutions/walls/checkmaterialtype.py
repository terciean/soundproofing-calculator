import pymongo

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Access the database
db = client["soundproofing"]  # Change this to your database name

# Access the collection
collection = db["wallsolutions"]  # Change this to your collection name

# Fetch the solution document for "Independent Wall (Standard)"
solution = collection.find_one({'solution': 'Independent Wall (Standard)', 'surface_type': 'walls'})

if solution and 'materials' in solution:
    # Iterate through all materials in the list
    for index, material in enumerate(solution['materials']):
        print(f"Material {index}:")
        print(f"  Name: {material.get('name', 'Unknown')}")
        print(f"  Cost: {material.get('cost', 'N/A')}")
        print(f"  Coverage: {material.get('coverage', 'N/A')} meters")
        print(f"  Object Type: {type(material)}")  # Check the object type
        print()  # Print a newline for better readability
else:
    print("Solution not found or no materials available.")