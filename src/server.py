import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from src.error import InputError
from src import config

from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.user import (user_profile_v2, user_profile_setname_v2, 
user_profile_setemail_v2, user_profile_sethandle_v1, user_stats_v1, 
user_profile_uploadphoto_v1)
from src.other import users_all_v1, users_stats_v1, clear_v1, search_v2
from src.channel import channel_invite_v2, channel_addowner_v1, channel_removeowner_v1, channel_leave_v1, channel_join_v2, channel_details_v2, channel_messages_v2
from src.dm import dm_create_v1, dm_list_v1, dm_details_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.message import message_send_v2, message_edit_v1, message_remove_v1, message_sendlater_v1, message_pin_v1, message_unpin_v1

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

APP = Flask(__name__, static_url_path='/src/static/')
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

@APP.route("/user/stats/v1", methods=['GET'])
def user_stats_server():
    token = request.args.get('token')
    return dumps(
        user_stats_v1(token)
    )

@APP.route("/user/profile/uploadphoto/v1", methods = ['POST'])
def user_profile_uploadphoto_server():
    payload = request.get_json()
    token = payload['token']
    img_url = payload['img_url']
    x_start = payload['x_start']
    y_start = payload['y_start']
    x_end = payload['x_end']
    y_end = payload['y_end']
    return dumps(
        user_profile_uploadphoto_v1(token, config.url, img_url, x_start, y_start, x_end, y_end)
    )

@APP.route("/static/<path:path>", methods=['GET'])
def send_js(path):
    return send_from_directory('', path)

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
    u_id = payload["u_id"]
    return dumps(
        channel_invite_v2(token, channel_id, u_id)
    )

@APP.route("/channel/addowner/v1", methods = ['POST'])
def channel_addowner_server():
    payload = request.get_json()
    token = payload["token"]
    channel_id = int(payload["channel_id"])
    u_id = payload["u_id"]
    return dumps(
        channel_addowner_v1(token, channel_id, u_id)
    )

@APP.route("/channel/removeowner/v1", methods = ['POST'])
def channel_removeowner_server():
    payload = request.get_json()
    token = payload["token"]
    channel_id = int(payload["channel_id"])
    u_id = payload["u_id"]
    return dumps(
        channel_removeowner_v1(token, channel_id, u_id)
    )

@APP.route("/channel/leave/v1", methods = ['POST'])
def channel_leave_server():
    payload = request.get_json()
    token = payload["token"]
    channel_id = int(payload["channel_id"])
    return dumps(
        channel_leave_v1(token, channel_id)
    )


@APP.route("/channel/join/v2", methods = ['POST'])
def channel_join_server():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    return dumps(
        channel_join_v2(token, channel_id)
    )

@APP.route("/channel/details/v2", methods = ['GET'])
def channel_details_server():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    return dumps(
        channel_details_v2(token,channel_id)
    )

@APP.route("/channel/messages/v2", methods = ['GET'])
def channel_messages_server():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    start = payload['start']
    return dumps(
        channel_messages_v2(token,channel_id,start)
    )

"""
MESSAGE ROUTES
"""
@APP.route("/message/send/v2", methods = ['POST'])
def message_send_server():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    return dumps(
        message_send_v2(token,channel_id,message)
    )

@APP.route("/message/remove/v1", methods = ['DELETE'])
def message_remove_server():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    return dumps(
        message_remove_v1(token,message_id)
    )

@APP.route("/message/edit/v2", methods = ['PUT'])
def message_edit_server():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    message = payload['message']
    return dumps(
        message_edit_v1(token,message_id,message)
    )

@APP.route("/message/sendlater/v1", methods = ['POST'])
def message_sendlater_server():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    time_sent = payload['time_sent']
    return dumps(
        message_sendlater_v1(token,channel_id,message,time_sent)
    )

@APP.route("/message/pin/v1", methods = ['POST'])
def message_pin_server():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    return dumps(
        message_pin_v1(token,message_id)
    )

@APP.route("/message/unpin/v1", methods = ['POST'])
def message_unpin_server():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    return dumps(
        message_unpin_v1(token,message_id)
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

@APP.route("/users/stats/v1", methods=['GET'])
def users_stats_server():
    token = request.args.get('token')
    return dumps(
        users_stats_v1(token)
    )

@APP.route("/clear/v1", methods=['DELETE'])
def clear_server():
    return dumps(
        clear_v1()
    )
    
@APP.route("/search/v2", methods=["GET"])
def search_server():
    token = request.args.get("token")
    query_str = request.args.get("query_str")
    return dumps(
        search_v2(token, query_str)
    )

"""
DM ROUTES
"""
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create_server():
    payload = request.get_json()
    token = payload["token"]
    u_ids = payload["u_ids"]
    return dumps(
        dm_create_v1(token, u_ids)
    )
@APP.route("/dm/list/v1", methods=['GET'])
def dm_list_server():
    token = request.args.get("token")
    return dumps(
        dm_list_v1(token)
    )

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details_server():
    token = request.args.get("token")
    dm_id = request.args.get("dm_id")
    return dumps(
        dm_details_v1(token,dm_id)
    )

"""
STANDUP ROUTES
"""
@APP.route("/standup/start/v1", methods = ['POST'])
def standup_start_server():
    payload = request.get_json()
    token = payload["token"]
    channel_id = payload["channel_id"]
    length = int(payload["length"])
    return dumps(
        standup_start_v1(token, channel_id, length)
    )

@APP.route("/standup/active/v1", methods = ['GET'])
def standup_active_server():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(
        standup_active_v1(token, channel_id)
    )

@APP.route("/standup/send/v1", methods = ['POST'])
def standup_send_server():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    return dumps(
        standup_send_v1(token, channel_id, message)
    )
 
if __name__ == "__main__":
    clear_v1()
    APP.run(port=config.port) # Do not edit this port
