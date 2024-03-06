import json
from bson import json_util
from flask import Response

def standard_response(data):
    return Response(
        json.dumps(data, default=json_util.default),
        mimetype='application/json'
    )

def conflict_response(text="There is a conflict"):
    return Response(
            text,
            mimetype='application/json',
            status=200
        )

def bad_request(text="Bad Request"):
    return Response(
            text,
            mimetype='application/json',
            status=400
        )

def unauthorized_request(text="Unauthorized to make take action"):
    return Response(
            text,
            mimetype='application/json',
            status=401
        )

def forbidden_request(text="You don't have the right permissions for that"):
    return Response(
            text,
            mimetype='application/json',
            status=403
        )

def not_found_request(text="That item is not found"):
    return Response(
            text,
            mimetype='application/json',
            status=404
        )

def internal_server_request(text="Internal Server Error"):
    return Response(
            text,
            mimetype='application/json',
            status=500
        )