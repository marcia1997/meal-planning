from pymongo import MongoClient

# MongoDB Connection URL
MONGO_URI = "mongodb://localhost:27017"

# Create a MongoDB client
client = MongoClient(MONGO_URI)

# Select the database
db = client["meal-planning"] 

#  Collections
users_collection = db["users"]
recipes_collection = db["recipes"] 
