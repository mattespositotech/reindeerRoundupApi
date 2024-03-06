import datetime
import os
import certifi

from pprint import pprint
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

# uses certifi certs instead of local which may be locked by os
client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())

# for db_info in client.list_database_names():
#     print(db_info)

db = client['reindeer']

collections = db.list_collection_names()
for collection in collections:
    print(collection)

roundups = db['roundup']

pprint(roundups.find_one())