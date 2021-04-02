import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
<<<<<<< HEAD
from src.channels import channels_create_v2, channels_listall_v2
=======
from src.channels import channels_create_v2
from src.user import user_profile_v2
>>>>>>> master
from src.other import clear_v1

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

"""
AUTH ROUTES
"""

@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_server():
    payload = request.get_json()
    
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']

    return dumps(
        auth_register_v2(email, password, name_first, name_last)
    )

@APP.route("/auth/login/v2", methods=['POST'])
def auth_login_server():
    payload = request.get_json()
    
    email = payload['email']
    password = payload['password']

    return dumps(
        auth_login_v2(email, password)
    )

@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout_server():
    payload = request.get_json()
    
    token = payload['token']

    return dumps(
        auth_logout_v1(token)
    )

"""
CHANNEL ROUTES
"""
@APP.route("/channels/create/v2", methods = ['POST'])
def channels_create_server():
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']
    return dumps(
        channels_create_v2(token, name, is_public)
    )

@APP.route("/channels/listall/v2", methods = ['GET'])
def channels_listall_server():
    token = request.args.get('token') 
    return dumps(
        channels_listall_v2(token)
    )
    
"""
USER ROUTES
"""
@APP.route("/user/profile/v2", methods=['GET'])
def user_profile_server():
    token = request.args.get('token')
    id = int(request.args.get('u_id'))
    return dumps(
        user_profile_v2(token, id)
    )

"""
OTHER ROUTES
"""
@APP.route("/clear/v1", methods=['DELETE'])
def clear_server():
    return dumps(
        clear_v1()
    )

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
    
