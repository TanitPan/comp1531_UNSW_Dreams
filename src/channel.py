from src.error import InputError, AccessError
from storage.data import data


def channel_invite_v1(auth_user_id, channel_id, u_id):
    """
    This function invite the user to given channel. 
    On success, add the user data to the channel.

    """

    # Flags to check for invalid input or invalid access
    valid_channel = False
    valid_uid = False
    ismember = False
    auth_valid = False

    for user in data["users"]:
        if user["auth_user_id"] == auth_user_id:
            auth_valid = True
            break 

    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel = True
            for member in channel["all_members"]:
                if member["auth_user_id"] == auth_user_id:
                    ismember = True
                    break
            break
    # Raise exception when detect invalid access/input
    if auth_valid == False:
        raise AccessError("authorised user ID is invalid")
    if valid_channel == False:
        raise InputError("channel_id is not a valid channel")
    if ismember == False:
        raise AccessError("authorised user not a member of channel")

    for user in data["users"]:
        if user["auth_user_id"] == u_id:
            valid_uid = True
            break
    if valid_uid == False:
        raise InputError("u_id is not valid user")

    new_member = {}
  
    # Find the detail of that u_id user
    for user in data["users"]:
        if user["auth_user_id"] == u_id:
            new_member = user

    # Loop over the target channel and add the u_id into
    for channel in data["channels"]:
        if channel_id == channel["channel_id"]:
            channel["all_members"].append(new_member)
        


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
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

# channel_invite_v1(1, 1, 2)
print("HELLO")