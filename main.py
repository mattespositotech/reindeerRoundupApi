import services.user as usr
import services.roundup as rnd
import services.secret_santa as ss
import services.transformer as tfm
import services.email as eml
import utils.responses as res
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

'''
Endpoints:
-Forgot password (trigger send email, then update password)
-Accepting roundup invite (check if all particpants have accepted, trigger launch roundup function)
-Launching roundup early
'''

@app.get('/test')
def test():
    #print('test')
    #rnd.get_all_ready_particitpants('65e8619212f7832259f1da50')
    #eml.test_email()
    return res.text_ok_response(hash)

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
    email = request.args.get('email')
    password = request.args.get('password')
    new_user = usr.sign_up_user(email, password)

    if (new_user == -1):
        return res.text_ok_response("Email is already registered")
    
    return res.standard_response(new_user)

@app.post('/user/login')
def post_login():
    email = request.args.get('email')
    password = request.args.get('password')
    user = usr.login_user(email, password)

    if (user):
        return res.standard_response(user)
    else:
        return res.bad_request('Bad login')

@app.delete('/user/delete')
def delete_user():
    email = request.args.get('email')
    deleted_rows = usr.delete_user_by_email(email)

    if (deleted_rows > 0):
        return res.standard_response("Deleted user with email of " + email)
    else:
        return res.bad_request("Could not delete user")
    
@app.post('/user/updatepassword')
def post_password():
    email = request.args.get('email')
    newPassword = request.args.get('password')
    updated_rows = usr.update_password_by_email(email, newPassword)

    if (updated_rows > 0):
        return res.standard_response("Updated password for user with email of " + email)
    else:
        return res.bad_request("Could not update user password")

@app.get('/user/roundups')
def get_roundups_by_user():
    email = request.args.get('email')
    user = usr.get_user_by_email(email)

    if not user:
        return res.not_found_request('No user found with that email')
    
    roundups = rnd.get_all_roundups_by_user(user)

    if roundups:
        return res.standard_response(roundups)
    else:
        return res.not_found_request("No roundups for this user")

@app.get('/roundup')
def get_roundup_by_id():
    id = request.args.get('id')

    roundup = rnd.get_roundup_by_id(id)

    if roundup:
        return res.standard_response(roundup)
    else:
        return res.not_found_request("Invalid roundup id")

@app.post('/roundup/add')
def post_add_roundup():
    email = request.args.get('email')
    data = request.get_json()

    roundup = tfm.prep_roundup_for_mongo(data)

    updated_rows = rnd.create_roundup(email, roundup)

    if (updated_rows > 0):
        return res.standard_response("Created a new roundup for user " + email)
    else:
        return res.bad_request("Could not add new roundup")

@app.delete('/roundup/delete')
def delete_roundup():
    id = request.args.get('id')
    deleted_rows = rnd.delete_roundup_by_id(id)

    if (deleted_rows > 0):
        return res.standard_response("Deleted roundup with id of " + id)
    else:
        return res.bad_request("Could not delete roundup")
    
@app.post('/roundup/participants/sendinvites')
def send_email_invites():
    id = request.args.get('id')

    roundup = rnd.get_roundup_by_id(id)

    if not roundup:
        return res.not_found_request("Invalid roundup id")

    eml.send_invites(roundup)
    return res.standard_response("Invites sent")

@app.post('/roundup/participant/status')
def post_change_participant_status():
    data = request.get_json()

    updated_rows = rnd.update_participants_status(data['id'], data['par_email'], data['status'])

    if (updated_rows > 0):
        return res.text_ok_response("Updated " + data['par_email'] + " in roundup " + data['id'])
    else:
        return res.bad_request("Could not update roundup")

@app.get('/roundup/santa')
def get_roundup_matches():
    id = request.args.get('id')
    matches = ss.launch_secret_santa(id)

    return res.standard_response(matches)

if __name__ == '__main__':
    app.run(debug=True, port=10000)