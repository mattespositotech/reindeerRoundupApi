import certifi
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from utils.constants import DATABASE_NAME

class MongoDataAccess:
    def __init__(self, collection):
        try:
            load_dotenv()
            MONGODB_URI = os.environ['MONGODB_URI']
            self.client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())

            database = DATABASE_NAME
            self.cursor = self.client[database]
            self.collection = self.cursor[collection]
        except Exception as e:
            print("An error occurred during initialization:", e)
    
    def change_collection(self, collection):
        try:
            self.collection = self.cursor[collection]
        except Exception as e:
            print("An error occurred while changing collection:", e)
    
    def read_one(self, query):
        try:
            document = self.collection.find_one(query)
            if document:
                document['_id'] = str(document['_id'])
                return document
            else:
                return None
        except Exception as e:
            print("An error occurred while reading one document:", e)
            return None
    
    def read_all(self, query, projection=None):
        try:
            if projection is None:
                documents = self.collection.find(query)
            else: 
                documents = self.collection.find(query, projection)
            return [{**doc, '_id': str(doc['_id'])} for doc in documents]
        except Exception as e:
            print("An error occurred while reading all documents:", e)
            return []
    
    def insert_one(self, record):
        try:
            inserted = self.collection.insert_one(record)
            return str(inserted.inserted_id)
        except Exception as e:
            print("An error occurred while inserting one document:", e)
            return None
    
    def update_one(self, query, update):
        try:
            updated = self.collection.update_one(query, update)
            return updated.modified_count
        except Exception as e:
            print("An error occurred while updating one document:", e)
            return 0
    
    def delete_one(self, query):
        try:
            deleted = self.collection.delete_one(query)
            return deleted.deleted_count
        except Exception as e:
            print("An error occurred while deleting one document:", e)
            return 0
    
    def aggregate_as_list(self, pipeline):
        try:
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            print("An error occurred while aggregating:", e)
            return []