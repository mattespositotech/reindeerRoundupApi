import json
# change to as statement during clean up
from services.user import * 
from services.roundup import * 
from bson import json_util
import utils.responses as res
from flask import Flask, Response, request



app = Flask(__name__)

'''
Endpoints:
-Forgot password (trigger send email, then update password)
-Accepting roundup invite (check if all particpants have accepted, trigger launch roundup function)
-Launching roundup early
'''

@app.get('/test')
def test():
    print('test')
    get_all_ready_particitpants('65e74ff2bab3a3b8e4ea819c')
    return Response(
        json.dumps("Test", default=json_util.default),
        mimetype='application/json'
    )

@app.get('/user')
def get_user(email="test@gmail.com"):
    user = get_user_by_email(email)

    return res.standard_response(user)

@app.post('/user/signup')
def post_signup(email='new@gmail.com', password='passwordHash'):
    new_user = sign_up_user(email, password)

    if (new_user == -1):
        return res.conflict_response("Email is already registered")
    
    return res.standard_response(new_user)

@app.post('/user/login')
def post_login(email='new@gmail.com', password='passwordHash'):
    user = login_user(email, password)

    if (user):
        return res.standard_response(user)
    else:
        return res.bad_request('Bad login')

@app.delete('/user/delete')
def delete_user(email='new@gmail.com'):
    deleted_rows = delete_user_by_email(email)

    if (deleted_rows > 0):
        confirm_text = "Deleted user with email of " + email
        return res.standard_response(confirm_text)
    else:
        return res.bad_request("Could not delete user")
    
@app.post('/user/updatepassword')
def post_password(email='new@gmail.com', newPassword='passwordHash2'):
    updated_rows = update_password_by_email(email, newPassword)

    if (updated_rows > 0):
        confirm_text = "Updated password for user with email of " + email
        return res.standard_response(confirm_text)
    else:
        return res.bad_request("Could not update user password")

@app.get('/roundup')
def get_roundups_by_user(email="test@gmail.com"):
    user = get_user_by_email(email)

    roundups = get_all_roundups_by_user(user)

    return res.standard_response(roundups)

@app.post('/roundup/add')
def post_add_roundup(email="test@gmail.com"):
    data = request.get_json()

    updated_rows = create_roundup(email, data)

    if (updated_rows > 0):
        confirm_text = "Created a new roundup for user " + email
        return res.standard_response(confirm_text)
    else:
        return res.bad_request("Could not add new roundup")

@app.delete('/roundup/delete')
def delete_roundup(id='65e85fea1968931f6f6acea9'):
    deleted_rows = delete_roundup_by_id(id)

    if (deleted_rows > 0):
        confirm_text = "Deleted roundup with id of " + id
        return res.standard_response(confirm_text)
    else:
        return res.bad_request("Could not delete roundup")

@app.post('/roundup/participant/status')
def post_change_participant_status(id='65e74ff2bab3a3b8e4ea819c', par_email="email1@gmail.com", status=1):
    updated_rows = update_participants_status(id, par_email, status)

    if (updated_rows > 0):
        confirm_text = "Updated " + par_email + " in roundup " + id
        res.standard_response(confirm_text)
    else:
        return res.bad_request("Could not update roundup")

if __name__ == '__main__':
    app.run(debug=True)