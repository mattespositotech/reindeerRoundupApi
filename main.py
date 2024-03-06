import json
# change to as statement during clean up
from services.user import * 
from services.roundup import * 
from bson import json_util
from utils.responses import standard_response
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

    return standard_response(user)

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
def post_password(email='new@gmail.com', newPassword='passwordHash2'):
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

@app.post('/roundup/add')
def post_add_roundup(email="test@gmail.com"):
    data = request.get_json()

    updated_rows = create_roundup(email, data)

    if (updated_rows > 0):
        confirm_text = "Created a new roundup for user " + email
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

@app.delete('/roundup/delete')
def delete_roundup(id='65e85fea1968931f6f6acea9'):
    deleted_rows = delete_roundup_by_id(id)

    if (deleted_rows > 0):
        confirm_text = "Deleted roundup with id of " + id
        return Response(
            json.dumps(confirm_text, default=json_util.default),
            mimetype='application/json'
        )
    else:
        return Response(
            "Could not delete roundup",
            mimetype='application/json',
            status=400
        )

@app.post('/roundup/participant/status')
def post_change_participant_status(id='65e74ff2bab3a3b8e4ea819c', par_email="email1@gmail.com", status=1):
    updated_rows = update_participants_status(id, par_email, status)

    if (updated_rows > 0):
        confirm_text = "Updated " + par_email + " in roundup " + id
        return Response(
            json.dumps(confirm_text, default=json_util.default),
            mimetype='application/json'
        )
    else:
        return Response(
            "Could not update roundup",
            mimetype='application/json',
            status=400
        )

if __name__ == '__main__':
    app.run(debug=True)