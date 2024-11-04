import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import services.user as usr
import services.roundup as rnd
import services.secret_santa as ss
import services.transformer as tfm
import services.email as eml
from utils.exceptions import NoValidCombinationError
import utils.responses as res
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
load_dotenv()
app.config['JWT_SECRET_KEY'] = os.environ['JWT_KEY']
jwt = JWTManager(app)
CORS(app, origins=["http://localhost:3000", "https://wonderful-tree-00f3c6710.5.azurestaticapps.net", "reindeer-roundup.com"])

@app.get('/test')
def test():
    return res.text_ok_response('test')

@app.get('/user')
def get_user():
    email = request.args.get('email')
    user = usr.get_user_by_email(email)

    if user:
        return res.standard_response(user)
    else:
        return res.not_found_request('No user found with that email')

@app.post('/user/signup')
def post_signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    new_user = usr.sign_up_user(email, password)

    if (new_user == -1):
        return res.bad_request("Email is already registered")
    
    access_token = create_access_token(identity=email)
    return res.standard_response({"email": new_user['email'], "access_token": access_token})

@app.post('/user/login')
def post_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = usr.login_user(email, password)

    if user == -1:
        return res.bad_request('Bad login')
    
    access_token = create_access_token(identity=email)
    return res.standard_response({"email": user['email'], "access_token": access_token})

@app.delete('/user/delete')
def delete_user():
    email = request.args.get('email')
    deleted_rows = usr.delete_user_by_email(email)

    if (deleted_rows > 0):
        return res.standard_response("Deleted user with email of " + email)
    else:
        return res.bad_request("Could not delete user")

@app.post('/user/resetpassword')
def post_reset_password():
    email = request.args.get('email')

    user = usr.get_user_by_email(email)

    if (user == None):
        return res.bad_request('No user with that email')

    eml.reset_password(user)
    return res.standard_response('Email sent')
    
@app.post('/user/updatepassword')
def post_password():
    data = request.get_json()
    id = data.get('id')
    password = data.get('password')

    updated_rows = usr.update_password_by_email(id, password)

    if (updated_rows > 0):
        return res.standard_response("Updated password for user")
    else:
        return res.bad_request("Could not update user password")

@app.get('/user/roundups')
@jwt_required()
def get_roundups_by_user():
    email = request.args.get('email')
    user = usr.get_user_by_email(email)

    if not user:
        return res.not_found_request('No user found with that email')
    
    roundups = rnd.get_all_roundups_by_user(user)

    if roundups:
        return res.standard_response(roundups)
    else:
        return res.standard_response([])

@app.get('/roundup')
@jwt_required()
def get_roundup_by_id():
    id = request.args.get('id')

    roundup = rnd.get_roundup_by_id(id)

    if roundup:
        return res.standard_response(roundup)
    else:
        return res.not_found_request("Invalid roundup id")

@app.post('/roundup/add')
@jwt_required()
def post_add_roundup():
    email = request.args.get('email')
    data = request.get_json()

    roundup = tfm.prep_roundup_for_mongo(data)

    updated_rows, roundup_id = rnd.create_roundup(email, roundup)

    if updated_rows > 0:
        roundup = rnd.get_roundup_by_id(roundup_id)
        eml.send_invites(roundup)
        return res.standard_response("Created a new roundup for user " + email)
    else:
        return res.bad_request("Could not add new roundup")

@app.delete('/roundup/delete')
@jwt_required()
def delete_roundup():
    id = request.args.get('id')
    deleted_rows = rnd.delete_roundup_by_id(id)

    if (deleted_rows > 0):
        return res.standard_response("Deleted roundup with id of " + id)
    else:
        return res.bad_request("Could not delete roundup")
    
@app.post('/roundup/participants/sendinvites')
@jwt_required()
def send_email_invites():
    id = request.args.get('id')

    roundup = rnd.get_roundup_by_id(id)

    if not roundup:
        return res.not_found_request("Invalid roundup id")

    eml.send_invites(roundup)
    return res.standard_response("Invites sent")

@app.post('/roundup/participants/allToAccepted')
@jwt_required()
def set_all_to_accepted():
    data = request.get_json()

    updated_rows = rnd.set_all_participants_to_accepted(data['id'])

    if (updated_rows > 0):
        return res.standard_response('Updated all participants')
    else:
        return res.bad_request('Could not update participants')


@app.post('/roundup/participant/accept')
def accept_invite():
    data = request.get_json()

    updated_rows, launchRoundup = rnd.update_participant_to_accepted(data['id'], data['uuid'])

    if launchRoundup:
        roundup_launch(data['id'])

    if (updated_rows > 0):
        roundup = rnd.get_roundup_by_id(data['id'])
        return res.standard_response(roundup['name'])
    else:
        return res.bad_request('Could not update participant')
    
@app.post('/roundup/participant/decline')
def decline_invite():
    data = request.get_json()

    updated_rows, launchRoundup = rnd.update_participant_to_declined(data['id'], data['uuid'])

    if launchRoundup:
        roundup_launch(data['id'])

    if (updated_rows > 0):
        roundup = rnd.get_roundup_by_id(data['id'])
        return res.standard_response(roundup['name'])
    else:
        return res.bad_request('Could not update participant')

@app.post('/roundup/launch')
@jwt_required()
def get_roundup_matches():
    data = request.get_json()

    update_rows, matches = roundup_launch(data['id'])

    if update_rows > 0:
        roundup = rnd.get_roundup_by_id(data['id'])
        eml.send_recievers(roundup)
        return res.standard_response(matches)
    elif update_rows == -1:
        return res.bad_request('No valid matches found') 
    else:
        return res.bad_request('Something went wrong with matches')

def roundup_launch(id):
    roundup = rnd.get_roundup_by_id(id)

    try: 
        matches = ss.get_matches(roundup)
    except NoValidCombinationError:
        rnd.set_status_to_bad_matches(id)
        eml.no_matches(roundup)
        return -1, {}
    
    updated_rows = rnd.save_matches_to_roundup(id, matches)

    return updated_rows, matches


if __name__ == '__main__':
    app.run(debug=True, port=10000)