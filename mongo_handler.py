
import os
import json
import logging
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def connect_mongo_db():
    """Connects to the MongoDB database and returns the messages collection."""
    mongo_url = os.getenv("MONGO_DB_URI")
    if not mongo_url:
        raise Exception("MongoDB URI is not set in the environment variables")
    
    client = MongoClient(mongo_url, server_api=ServerApi('1'))
    
    try:
        client.admin.command('ping')  # Validate connection
        db = client["book"]
        collection = db["messages"]
        return collection
    except Exception as e:
        raise Exception(f"Failed to connect to MongoDB: {e}")


async def save_message(data):
    """Saves incoming messages to MongoDB."""
    collection = connect_mongo_db()
    try:
        logging.info(f"Received message: {data}")
          
        collection.insert_one(data)  # Save to MongDB
        logging.info(f"Message saved to DB: {data}")
        return json.dumps({"status": "success", "message": "Message saved"})

    except Exception as e:
        logging.error(f"Error saving message to DB: {e}")
        return json.dumps({"status": "error", "message": str(e)})