from pymongo import MongoClient

# Connect to the MongoDB
client = MongoClient("mongodb+srv://thatguyrazor:bell12@cluster0.rxg93.mongodb.net/guyrazor?retryWrites=true&w=majority")

# Access the 'guyrazor' database
db = client.guyrazor
wallsolutions = db.wallsolutions

# List all documents in the wallsolutions collection
# This will display the full document to understand its structure
for solution in wallsolutions.find():
    print(solution)
