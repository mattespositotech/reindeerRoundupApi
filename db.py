import certifi
import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import json_util

class Connection:
    def __new__(cls, database):
        load_dotenv()
        MONGODB_URI = os.environ['MONGODB_URI']
        connection = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
        return connection[database]

# add try catch blocks to all functions
class MongoDataAccess:
    def __init__(self, collection):
        load_dotenv()
        MONGODB_URI = os.environ['MONGODB_URI']
        self.client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())

        database = 'reindeer'
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