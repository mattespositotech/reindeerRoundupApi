import json
from bson import json_util

from flask import Response

def standard_response(data):
    return Response(
        json.dumps(data, default=json_util.default),
        mimetype='application/json'
    )