from bson.objectid import ObjectId
from dataAccess.MongoDataAccess import MongoDataAccess
from services.user import add_roundup_to_user

def get_all_roundups_by_user(user):
    roundup_ids = user['roundups']

    if len(roundup_ids) == 0:
        return None

    obj_roundup_ids = [ObjectId(id) for id in roundup_ids]

    query = {
        '_id': {'$in': obj_roundup_ids}
    }

    dataAccess = MongoDataAccess('roundup')
    roundups = dataAccess.read_all(query)
    
    return roundups

def create_roundup(email, data):
    dataAccess = MongoDataAccess('roundup')
    roundup_id = dataAccess.insert_one(data)

    if (roundup_id):
        user_rows_updated = add_roundup_to_user(email, roundup_id)
        return user_rows_updated
    else:
        return -1

def delete_roundup_by_id(roundup_id):
    query = {
        '_id': ObjectId(roundup_id)
    }

    dataAccess = MongoDataAccess('roundup')
    deleted_rows = dataAccess.delete_one(query)

    return deleted_rows

def update_participants_status(roundup_id, par_email, status):
    query = {
        "_id": ObjectId(roundup_id),
        "participants.email": par_email
    }
    update = {
        "$set": {"participants.$.status": status}
    }

    dataAccess = MongoDataAccess('roundup')
    updated_rows = dataAccess.update_one(query, update)

    # hook up to email service when implemented
    check_roundup_for_launch(roundup_id)

    return updated_rows

def check_roundup_for_launch(roundup_id):
    pipeline = [
        { "$match" : {
            "_id" : ObjectId(roundup_id),
            "participants.status": 0
            }
        },
        {"$limit": 1}
    ]

    dataAccess = MongoDataAccess('roundup')
    par_pending = dataAccess.aggregate_as_list(pipeline)

    return not par_pending

def get_all_ready_particitpants(roundup_id):
    pipeline = [
        {"$match": {"_id": ObjectId(roundup_id), "participants.status": 1}}, 
        {"$project": {"_id": 0, "participants": {"$filter": {
            "input": "$participants",
            "as": "participant",
            "cond": {"$eq": ["$$participant.status", 1]}
        }}}}
    ]

    dataAccess = MongoDataAccess('roundup')
    result = dataAccess.aggregate_as_list(pipeline)

    participants = [participant for doc in result for participant in doc.get("participants", [])]

    return participants