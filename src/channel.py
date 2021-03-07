from src.error import InputError, AccessError
from data import data
from src.helper import check_valid_user


def channel_invite_v1(auth_user_id, channel_id, u_id):
    """
    This function invites the user to given channel. 
    On success, add the user data to the channel.

    Arguments:
        auth_user_id (int) - the user ID of the person inviting
        channel_id (int) - the ID of the channel to invite a user to
        u_id (int) - the ID of the user being invited to the channel

    Exceptions:
        InputError - Occurs when u_id or channel_id is invalid.
        AccessError - Occurs when the authorised user is not a member of the channel
                      or the authorised user is invalid or the authorised user is 
                      inviting someone already in the channel.
    Return Value:
        Returns an empty dictionary on completeion
    """

    # Flags to check for invalid input or invalid access
    valid_channel = False
    valid_uid = False
    ismember = False

    # Loop to check if auth_user_id is valid
    check_valid_user(auth_user_id)

    new_member = {}
    # Loop to check if user id is valid and store that user info
    for user in data["users"]:
        if user["auth_user_id"] == u_id:
            valid_uid = True
            new_member["auth_user_id"] = user["auth_user_id"]
            break

    # Raise exception for invalid u_id
    if valid_uid == False:
        raise InputError("u_id is not valid user")

    # Loop to check if channel id is valid
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel = True

            # Loop to check if auth_user_id is a member of channel
            for member in channel["all_members"]:
                if member["auth_user_id"] == auth_user_id:
                    ismember = True
                    break
            # Loop to check if u_id is already in channel
            for member in channel["all_members"]:
                if member["auth_user_id"] == u_id:
                    raise AccessError("Repetitive invite! This u_id already in channel")

            break

    # Raise exception when detect invalid access/input
    if valid_channel == False:
        raise InputError("channel_id is not a valid channel")
    if ismember == False:
        raise AccessError("authorised user not a member of channel")

    # Loop over the target channel and add u_id into channel
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
