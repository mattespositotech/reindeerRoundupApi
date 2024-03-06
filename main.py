import json
# change to as statement during clean up
from endpoints.user import * 
from bson import json_util
from bson.objectid import ObjectId
from flask import Flask, Response
from dataAccess.MongoDataAccess import MongoDataAccess


app = Flask(__name__)

'''
Endpoints:
-Adding new roundup
-Deleteing roundup
-Forgot password (trigger send email, then update password)
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
    deleted_rows = delete_user_by_email(email)

    if (deleted_rows > 0):
        confirm_text = "Deleted user with email of " + email
        return Response(
            json.dumps(confirm_text, default=json_util.default),
            mimetype='application/json'
        )
    else:
        return Response(
            "Could not delete user",
            mimetype='application/json',
            status=400
        )
    
@app.post('/user/updatepassword')
def update_password(email='new@gmail.com', newPassword='passwordHash2'):
    updated_rows = update_password_by_email(email, newPassword)

    if (updated_rows > 0):
        confirm_text = "Updated password for user with email of " + email
        return Response(
            json.dumps(confirm_text, default=json_util.default),
            mimetype='application/json'
        )
    else:
        return Response(
            "Could not update password",
            mimetype='application/json',
            status=400
        )

@app.get('/roundup')
def get_roundups_by_user(email="test@gmail.com"):
    user = get_user_by_email(email)

    roundups = get_all_roundups_by_user(user)

    return Response(
        json.dumps(roundups, default=json_util.default),
        mimetype='application/json'
    )

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