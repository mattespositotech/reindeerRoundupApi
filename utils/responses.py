import json
from bson import json_util
from flask import Response

def standard_response(data):
    return response_wrapper(data, 500)

def text_ok_response(text="There is a conflict"):
    return response_wrapper(text, 200)

def bad_request(text="Bad Request"):
    return response_wrapper(text, 400)

def unauthorized_request(text="Unauthorized to make take action"):
    return response_wrapper(text, 401)

def forbidden_request(text="You don't have the right permissions for that"):
    return response_wrapper(text, 403)

def not_found_request(text="That item is not found"):
    return response_wrapper(text, 404)

def internal_server_request(text="Internal Server Error"):
    return response_wrapper(text, 500)

def response_wrapper(data, status=200):
    return Response(
            json.dumps(data, default=json_util.default),
            mimetype='application/json',
            status=status
        )