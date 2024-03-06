import json
from bson import json_util
from bson.objectid import ObjectId
from flask import Flask, Response
from db import Connection, MongoDataAccess

app = Flask(__name__)
db = Connection('reindeer')

'''
Endpoints:
-Adding new roundup
-Deleteing roundup
-Deleting user
-Forgot password
-Accepting roundup invite (check if all particpants have accepted, trigger launch roundup function)
-Declining roundup invite
-Launching roundup early
'''

@app.get('/user')
def get_user(email="test@gmail.com"):
    user = get_user_by_email(email)

    return Response(
        json.dumps(user, default=json_util.default),
        mimetype='application/json'
    )

@app.post('/user/signup')
def post_signup(email='new@gmail.com', password='passwordHash'):
    new_user = sign_up_user(email, password)

    if (new_user == -1):
        return Response(
            "Email is already registered",
            mimetype='application/json',
            status=403
        )
    
    return Response(
        new_user,
        mimetype='application/json'
    )

@app.post('/user/login')
def post_login(email='new@gmail.com', password='passwordHash'):
    user = login_user(email, password)

    if (user):
        return Response(
            json.dumps(user, default=json_util.default),
            mimetype='application/json'
        )
    else:
        return Response(
            "Bad login",
            mimetype='application/json',
            status=403
        )

@app.delete('/user/delete')
def delete_user(email='new@gmail.com'):
    

@app.get('/roundup')
def get_roundups_by_user(email="test@gmail.com"):
    user = get_user_by_email(email)

    roundups = get_all_roundups_by_user(user)

    return Response(
        json.dumps(roundups, default=json_util.default),
        mimetype='application/json'
    )

def login_user(email, password):
    query = {
        "email": email,
        "password": password
    }

    dataAccess = MongoDataAccess('user')
    user = dataAccess.read_one(query)

    return user

def sign_up_user(email, password):
    existing_user = get_user_by_email(email)

    if (existing_user): 
        return -1

    new_user = {
        "email": email,
        "password": password,
        "roundups": []
    }

    dataAccess = MongoDataAccess('user')
    insert_result = dataAccess.insert_one(new_user)

    return insert_result

def get_user_by_email(email):
    query = {
        "email": email
    }

    dataAccess = MongoDataAccess('user')
    user = dataAccess.read_one(query)

    return user

def get_all_roundups_by_user(user):
    roundup_ids = user['roundups']

    obj_roundup_ids = [ObjectId(id) for id in roundup_ids]

    query = {
        '_id': {'$in': obj_roundup_ids}
    }

    dataAccess = MongoDataAccess('roundup')
    roundups = dataAccess.read_all(query)
    
    return roundups

if __name__ == '__main__':
    app.run(debug=True)