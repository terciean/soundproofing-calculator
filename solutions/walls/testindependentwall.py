import pymongo
import math

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Access the database
db = client["soundproofing"]  # Change this to your database name

# Access the collection
collection = db["wallsolutions"]  # Change this to your collection name

# Fetch the solution document for "Independent Wall (Standard)"
solution = collection.find_one({'solution': 'Independent Wall (Standard)', 'surface_type': 'walls'})

if solution and 'materials' in solution:
    # Print details of each material
    for index, material in enumerate(solution['materials']):
        print(f"Material {index + 1}:")
        print(f"  Name: {material.get('name', 'Unknown')}")
        print(f"  Cost: {material.get('cost', 'N/A')}")
        print(f"  Coverage: {material.get('coverage', 'N/A')} square meters per unit")
        print(f"  Object Type: {type(material)}")  # Check the object type
        print()  # Print a newline for better readability

    # Now calculate the required quantities based on area
    area = 5  # Example area to be covered in square meters

    for index, material in enumerate(solution['materials']):
        try:
            # Get the coverage value
            coverage_value = material.get('coverage')
            print(f"Coverage for {material.get('name', 'Unknown')}: {coverage_value} square meters per unit")
            
            # Check if coverage is a valid number
            if coverage_value is None or not isinstance(coverage_value, (int, float, str)):
                raise ValueError(f"Invalid coverage value for {material.get('name', 'Unknown')}.")
            
            # Convert coverage to float (ensure it is a numeric value in square meters)
            coverage = float(coverage_value)  # Ensure this is a float
            if coverage <= 0:  # Check for non-positive coverage
                raise ValueError(f"Coverage must be greater than zero for {material.get('name', 'Unknown')}.")
            
            # Calculate the required quantity based on the area
            required_quantity = math.ceil(area / coverage)  # Area divided by coverage area per unit
            print(f"Material: {material.get('name', 'Unknown')}, Required Quantity: {required_quantity}")
        except ValueError as ve:
            print(f"Error for {material.get('name', 'Unknown')}: {ve}")
        except KeyError as ke:
            print(f"Key error for {material}: {ke}")
        except TypeError as te:
            print(f"Type error for {material.get('name', 'Unknown')}: {te}")
else:
    print("Solution not found or no materials available.")