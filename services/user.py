from dataAccess.MongoDataAccess import MongoDataAccess
from services.encryption import check_password, hash_password

def add_roundup_to_user(email, roundup_id):
    query = {
        "email": email
    }
    update = {
        "$push": {"roundups": roundup_id}
    }

    dataAccess = MongoDataAccess('user')
    updated_rows = dataAccess.update_one(query, update)

    return updated_rows

def update_password_by_email(email, newPassword):
    password = hash_password(newPassword)

    query = {
        "email": email
    }
    update = {
        "$set": {"password": password}
    }

    dataAccess = MongoDataAccess('user')
    updated_rows = dataAccess.update_one(query, update)

    return updated_rows


def delete_user_by_email(email):
    query = {
        "email": email
    }

    dataAccess = MongoDataAccess('user')
    deleted_rows = dataAccess.delete_one(query)

    return deleted_rows

def login_user(email, password):
    user = get_user_by_email(email)

    if (user == None):
        return -1

    if check_password(password, user['password']):
        return user
    else:
        return -1

def sign_up_user(email, password):
    existing_user = get_user_by_email(email)

    if (existing_user): 
        return -1

    password_hash = hash_password(password)

    new_user = {
        "email": email,
        "password": password_hash,
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