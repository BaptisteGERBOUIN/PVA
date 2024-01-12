from pymongo import MongoClient

MONGODB_URI = 'mongodb://localhost'
DATABSE_NAME = 'pva_water_project'

def get_collection(collection_name: str):
    client = MongoClient(MONGODB_URI)
    db_water = client[DATABSE_NAME]
    return db_water[collection_name]