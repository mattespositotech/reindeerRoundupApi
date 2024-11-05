from bson.objectid import ObjectId
from dataAccess.MongoDataAccess import MongoDataAccess
from enums.roundup_enums import RoundupStatus
from enums.user_enums import UserStatus
from services.user import add_roundup_to_user

def get_all_roundups_by_user(user):
    roundup_ids = user['roundups']

    if len(roundup_ids) == 0:
        return None

    obj_roundup_ids = [ObjectId(id) for id in roundup_ids]

    query = {
        '_id': {'$in': obj_roundup_ids}
    }

    # 1 means to include the field
    projection = {
        'name': 1,
        'date': 1,
        'status': 1,
        '_id': 1
    }

    dataAccess = MongoDataAccess('roundup')
    roundups = dataAccess.read_all(query, projection=projection)
    
    return roundups

def create_roundup(email, data):
    dataAccess = MongoDataAccess('roundup')

    data['organizer'] = email
    roundup_id = dataAccess.insert_one(data)

    if (roundup_id):
        user_rows_updated = add_roundup_to_user(email, roundup_id)
        return user_rows_updated, roundup_id
    else:
        return -1, -1
    
def get_roundup_by_id(roundup_id):
    query = {
        '_id': ObjectId(roundup_id)
    }

    dataAccess = MongoDataAccess('roundup')
    roundup = dataAccess.read_one(query)

    return roundup

def delete_roundup_by_id(roundup_id):
    query = {
        '_id': ObjectId(roundup_id)
    }

    dataAccess = MongoDataAccess('roundup')
    deleted_rows = dataAccess.delete_one(query)

    return deleted_rows

def update_participant_to_accepted(roundup_id, uuid):
    return update_participants_status(roundup_id, uuid, UserStatus.Accepted)

def update_participant_to_declined(roundup_id, uuid):
    return update_participants_status(roundup_id, uuid, UserStatus.Declined)

def update_participants_status(roundup_id, uuid, status):
    query = {
        "_id": ObjectId(roundup_id),
        "participants.uuid": uuid
    }
    update = {
        "$set": {"participants.$.status": status.value}
    }

    dataAccess = MongoDataAccess('roundup')
    updated_rows = dataAccess.update_one(query, update)

    launchRoundup = check_roundup_for_launch(roundup_id)

    return updated_rows, launchRoundup

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

def set_all_participants_to_accepted(roundup_id):
    query = {
        "_id": ObjectId(roundup_id)
    }
    update = {
        "$set": {"participants.$[].status": UserStatus.Accepted.value}
    }

    dataAccess = MongoDataAccess('roundup')
    updated_rows = dataAccess.update_many(query, update)

    return updated_rows

def set_status_to_in_progress(roundup_id):
    query = {
        "_id": ObjectId(roundup_id)
    }
    update = {
        "$set": {
            "status": RoundupStatus.InProgress.value
        }
    }

    dataAccess = MongoDataAccess('roundup')
    updated_rows = dataAccess.update_one(query, update)

    return updated_rows

def set_status_to_bad_matches(roundup_id):
    query = {
        "_id": ObjectId(roundup_id)
    }
    update = {
        "$set": {
            "status": RoundupStatus.BadMatches.value
        }
    }

    dataAccess = MongoDataAccess('roundup')
    updated_rows = dataAccess.update_one(query, update)

    return updated_rows

def save_matches_to_roundup(roundup_id, matches):
    query = {
        "_id": ObjectId(roundup_id)
    }
    update = {
        "$set": {
            "matches": matches,
            "status": RoundupStatus.Complete.value
        }
    }

    dataAccess = MongoDataAccess('roundup')
    updated_rows = dataAccess.update_one(query, update)

    return updated_rows

def add_participant_to_roundup(roundup_id, participant):
    query = {
        "_id": ObjectId(roundup_id)
    }

    update = {
        "$push": {
            "participants": participant
        }
    }

    dataAccess = MongoDataAccess('roundup')
    updated_rows = dataAccess.update_one(query, update)

    return updated_rows

def update_participants_email(roundup_id, participant_id, email):
    query = {
        "_id": ObjectId(roundup_id),
        "participants.uuid": participant_id
    }

    update = {
        "$set": {
            "participants.$.email": email
        }
    }

    dataAccess = MongoDataAccess('roundup')
    updated_rows = dataAccess.update_one(query, update)

    return updated_rows

def delete_participant(roundup_id, participant_id):
    query = {
        "_id": ObjectId(roundup_id)
    }

    update = {
        "$pull": {
            "participants": {
                "uuid": participant_id
            }
        }
    }

    dataAccess = MongoDataAccess('roundup')
    updated_rows = dataAccess.update_one(query, update)

    return updated_rows