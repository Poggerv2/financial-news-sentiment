from pymongo import MongoClient

def get_mongo_collection(db_name="financial_news", collection_name="articles"):
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    return db[collection_name]