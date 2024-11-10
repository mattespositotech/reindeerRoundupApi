import os
import datetime
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
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)
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
    elif (new_user == None):
        return res.bad_request('Could not add user')
    
    access_token = create_access_token(identity=email)
    return res.standard_response({"email": email, "access_token": access_token})

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

@app.post('/roundup/participant/add')
@jwt_required()
def add_participant():
    data = request.get_json()
    roundup_id = data['id']
    participant = data['participant']
    tfm.prep_participant(participant)

    updated_rows = rnd.add_participant_to_roundup(roundup_id, participant)

    if (updated_rows > 0):
        rnd.set_status_to_in_progress(roundup_id)
        roundup = rnd.get_roundup_by_id(roundup_id)
        eml.send_invites(roundup, participant['email'])
        return res.standard_response('Added new participant')
    else:
        return res.bad_request('Could not add new participant')

@app.post('/roundup/participant/update')
@jwt_required()
def update_participant():
    data = request.get_json()
    roundup_id = data['id']
    participant_id = data['part_id']
    email = data['email']

    update_rows = rnd.update_participants_email(roundup_id, participant_id, email)

    if (update_rows > 0):
        roundup = rnd.get_roundup_by_id(roundup_id)
        eml.send_invites(roundup, email)
        return res.standard_response('Email updated')
    else:
        return res.bad_request('Could not update email')

@app.delete('/roundup/participant/delete')
@jwt_required()
def delete_participant():
    roundup_id = request.args.get('id')
    participant_id = request.args.get('uuid')

    updated_rows = rnd.delete_participant(roundup_id, participant_id)

    if (updated_rows > 0):
        return res.standard_response('Participant Removed')
    else:
        return res.bad_request('Could not remove participant')

@app.post('/roundup/participant/reinvite')
@jwt_required()
def resend_email():
    data = request.get_json()
    roundup_id = data['id']
    email = data['email']

    roundup = rnd.get_roundup_by_id(roundup_id)

    if (roundup):
        eml.send_invites(roundup, email)
        return res.standard_response('Email Sent')
    else:
        return res.bad_request("Could not find roundup")

@app.post('/roundup/blacklist/add')
@jwt_required()
def add_blacklist():
    data = request.get_json()
    roundup_id = data['id']
    blacklist = data['blacklist']

    cleaned_blacklist = tfm.create_blacklist_object(blacklist)

    updated_rows = rnd.add_blacklist(roundup_id, cleaned_blacklist)

    if (updated_rows > 0):
        return res.standard_response('Blacklist added')
    else:
        return res.bad_request('Could not add blacklist')

@app.post('/roundup/blacklist/update')
@jwt_required()
def update_blacklist():
    data = request.get_json()
    roundup_id = data['id']
    blacklist = data['blacklist']

    updated_rows = rnd.update_blacklist(roundup_id, blacklist)

    if (updated_rows > 0):
        return res.standard_response('Blacklist updated')
    else:
        return res.bad_request('Could not update blacklist')

@app.delete('/roundup/blacklist/delete')
@jwt_required()
def delete_blacklist():
    roundup_id = request.args.get('id')
    blacklist_id = request.args.get('uuid')

    updated_rows = rnd.delete_blacklist(roundup_id, blacklist_id)

    if (updated_rows > 0):
        return res.standard_response('Blacklist deleted')
    else:
        return res.bad_request('Could not delete blacklist')

@app.post('/roundup/launch')
@jwt_required()
def get_roundup_matches():
    data = request.get_json()

    update_rows, matches = roundup_launch(data['id'])

    if update_rows > 0:
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

    if updated_rows > 0:
        roundup = rnd.get_roundup_by_id(id)
        eml.send_recievers(roundup)

    return updated_rows, matches


if __name__ == '__main__':
    app.run(debug=True, port=10000)