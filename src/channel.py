from src.error import InputError, AccessError
from data import data

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    """
    This function adds a auth_user_id to a
    channel_id provided.
    """
    # Flags to check for invalid input or invalid access
    valid_auth = False
    valid_channel = False
    new_user_info = {}

    # Loop to check if auth_user_id is valid and store user info
    for user in data["users"]:
        if user["auth_user_id"] == auth_user_id:
            valid_auth = True
            global_permission = user["permission_id"]
            new_user_info["auth_user_id"] = user["auth_user_id"]
            break

    # Loop to check if channel id is valid and store channel privacy
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel = True
            channel_privacy = channel["is_public"]

            # Loop to check if member is already in channel 
            for member in channel["all_members"]:
                if member["auth_user_id"] == auth_user_id:
                    raise AccessError("Repetitive join! You are already a member of channel !")
            break


    # Raise exception when detect invalid auth_user_id
    if not valid_auth:
        raise AccessError("authorised user ID is invalid")

    # Raise excpetion when detect invalid channel
    if not valid_channel:
        raise InputError("invalid channel ID")

    # if global_permission != 1 and not channel_privacy:
    # Check if the auth_user_id has permission to join channel
    if global_permission == 1 or channel_privacy:
        for channel in data["channels"]:
            if channel["channel_id"] == channel_id:
                channel["all_members"].append(new_user_info)
    else:
        raise AccessError("channel ID refer to a private channel")

    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }