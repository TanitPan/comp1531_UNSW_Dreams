import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.user import user_profile_v2, user_profile_setname_v2, user_profile_setemail_v2, user_profile_sethandle_v1
from src.other import users_all_v1, clear_v1
from src.channel import channel_invite_v2, channel_addowner_v1, channel_removeowner_v1, channel_leave_v1

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
CHANNELS ROUTES
"""
@APP.route("/channels/list/v2", methods = ['GET'])
def channels_list_server():
    token = request.args.get('token') 
    return dumps(
        channels_list_v2(token)
    )
    
@APP.route("/channels/listall/v2", methods = ['GET'])
def channels_listall_server():
    token = request.args.get('token') 
    return dumps(
        channels_listall_v2(token)
    )
    
@APP.route("/channels/create/v2", methods = ['POST'])
def channels_create_server():
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']
    return dumps(
        channels_create_v2(token, name, is_public)
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

@APP.route("/user/profile/setname/v2", methods=['PUT'])
def user_profile_setname():
    payload = request.get_json()
    token = payload['token']
    name_first = payload['name_first']
    name_last = payload['name_last']
    return dumps(
        user_profile_setname_v2(token, name_first, name_last)
    )

@APP.route("/user/profile/setemail/v2", methods=['PUT'])
def user_profile_setemail():
    payload = request.get_json()
    token = payload['token']
    email = payload['email']

    return dumps(
        user_profile_setemail_v2(token, email)
    )

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_profile_sethandle():
    payload = request.get_json()
    token = payload['token']
    handle_str = payload['handle_str']

    return dumps(
        user_profile_sethandle_v1(token, handle_str)
    )

"""
ADMIN ROUTES
"""
@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove_server():
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    return dumps(
        admin_user_remove_v1(token, u_id)
    )
    
@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change_server():
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    return dumps(
        admin_userpermission_change_v1(token, u_id, permission_id)
    )

"""
CHANNEL ROUTES
"""
@APP.route("/channel/invite/v2", methods = ['POST'])
def channel_invite_server():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    # print(channel_id)
    u_id = payload["u_id"]
    return dumps(
        channel_invite_v2(token, channel_id, u_id)
    )

@APP.route("/channel/addowner/v1", methods = ['POST'])
def channel_addowner_server():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    u_id = payload["u_id"]
    return dumps(
        channel_addowner_v1(token, channel_id, u_id)
    )

@APP.route("/channel/removeowner/v1", methods = ['POST'])
def channel_removeowner_server():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    u_id = payload["u_id"]
    return dumps(
        channel_removeowner_v1(token, channel_id, u_id)
    )

@APP.route("/channel/leave/v1", methods = ['POST'])
def channel_leave_server():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    return dumps(
        channel_leave_v1(token, channel_id)
    )



"""
OTHER ROUTES
"""
@APP.route("/users/all/v1", methods=['GET'])
def users_all_server():
    token = request.args.get('token')
    return dumps(
        users_all_v1(token)
    )

@APP.route("/clear/v1", methods=['DELETE'])
def clear_server():
    return dumps(
        clear_v1()
    )

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
    
