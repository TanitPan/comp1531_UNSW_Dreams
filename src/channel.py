from src.error import InputError, AccessError
from data import data
from src.helper import check_valid_user, valid_token, valid_channel, check_existing_owner, check_dreams_owner

def channel_invite_v2(token, channel_id, u_id):
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
    # Check token validity
    auth_user_id = valid_token(token)

    # Flags to check for invalid input or invalid access
    valid_channel = False
    valid_uid = False
    ismember = False

    new_member = {}
    # Loop to check if user id is valid and store that user info
    for user in data["users"]:
        if user["auth_user_id"] == u_id:
            valid_uid = True
            new_member["auth_user_id"] = user["auth_user_id"]
            break

    # Raise exception for invalid u_id
    if valid_uid == False:
        raise InputError(description = "u_id is not valid user")

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
                    raise AccessError(description = "Repetitive invite! This u_id already in channel")

            break

    # Raise exception when detect invalid access/input
    if valid_channel == False:
        raise InputError(description = "channel_id is not a valid channel")
    if ismember == False:
        raise AccessError(description = "authorised user not a member of channel")

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
    """
    This function adds a auth_user_id to a
    channel_id provided.

    Arguments:
        auth_user_id (int) - the user ID of the person joining a channel
        channel_id (int) - the ID of the channel the user want to join

    Exceptions:
        InputError - Occurs when channel_id is invalid.
        AccessError - Occurs when the authorised user is not a valid ID or 
                      the authorised user is joining a private channel without
                      being a global DREAM owner or the authorised user is joining
                      a channel he is already in
    Return Value:
        Returns an empty dictionary on completeion
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

    # Check if the auth_user_id has permission to join channel
    if global_permission == 1 or channel_privacy:
        for channel in data["channels"]:
            if channel["channel_id"] == channel_id:
                channel["all_members"].append(new_user_info)
    else:
        raise AccessError("channel ID refer to a private channel")

    return {
    }

def channel_addowner_v1(token, channel_id, u_id):
    auth_user = valid_token(token)
    valid_channel(channel_id)
    if check_existing_owner(u_id, channel_id):
        raise InputError("The user is already an owner of the channel.")
    if check_existing_owner(auth_user, channel_id) == False:
         check_dreams_owner(auth_user)
	
    new_owner = {"auth_user_id": u_id}    
    for channel in data['channels']:	
        for owner in channel['owner_members']:
            channel['owner_members'].append(new_owner)
            break
		
    member_valid = False
    for member in channel['all_members']:
        if u_id == member['auth_user_id']: 
            member_valid = True	
            break 	
	
    if member_valid == False:
        channel['all_members'].append(new_owner)
    
    return {
    }


def channel_removeowner_v1(token, channel_id, u_id):
    auth_user = valid_token(token)
    valid_channel(channel_id)
    if check_existing_owner(u_id, channel_id) == False:
        raise InputError("The user is not an owner of the channel.")
    if check_existing_owner(auth_user, channel_id) == False:
         check_dreams_owner(auth_user)
    
    for channel in data["channels"]:
        if channel_id == channel["channel_id"]:
            for owner in channel["owner_members"]:
                if owner["auth_user_id"] == u_id and len(channel["owner_members"]) == 1:
                    raise InputError("The owner is the only channel owner")
   
    removed_owner = {"auth_user_id": u_id}    
    for channel in data['channels']:	
        for owner in channel['owner_members']:
            if removed_owner == owner:
                channel['owner_members'].remove(removed_owner)
                break
    return {
    }


  
    
