import certifi
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from utils.constants import DATABASE_NAME

# add try catch blocks to all functions
class MongoDataAccess:
    def __init__(self, collection):
        load_dotenv()
        MONGODB_URI = os.environ['MONGODB_URI']
        self.client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())

        database = DATABASE_NAME
        self.cursor = self.client[database]
        self.collection = self.cursor[collection]
    
    def change_collection(self, collection):
        self.collection = self.cursor[collection]
    
    def read_one(self, query):
        document = self.collection.find_one(query)
        if (document):
            document['_id'] = str(document['_id'])
            return document
        else:
            return None
    
    def read_all(self, query):
        documents = self.collection.find(query)
        return [{**doc, '_id': str(doc['_id'])} for doc in documents]
    
    def insert_one(self, record):
        inserted = self.collection.insert_one(record)
        return str(inserted.inserted_id)
    
    def update_one(self, query, update):
        updated = self.collection.update_one(query, update)
        return updated.modified_count
    
    def delete_one(self, query):
        deleted = self.collection.delete_one(query)
        return deleted.deleted_count
    
    def aggregate_as_list(self, pipeline):
        return list(self.collection.aggregate(pipeline))