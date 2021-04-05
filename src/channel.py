from src.error import InputError, AccessError
from data import data
from src.helper import check_valid_user, valid_token, search_user_data

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

def channel_details_v2(token, channel_id):

    ''' 
    This function is to return the detail of a channel that includes
        channel name, the owners data and the all members data 
        
    Arguments:
        token () - the user ID of the members
        channel_id (int) - the ID of the channel

    Exceptions:
        InputError - Occurs when u_id or channel_id is invalid.
        AccessError - Occurs when the authorised user is not a member of the channel
                      or the authorised user is invalid or the authorised user is 
                      inviting someone already in the channel.
    Return Value:
        Returns a dictionary dictionary that includes channel name, 
        the owners data and the members data
    '''

    # Assign new variables to check
    valid_channel = False
    is_member = False

    # Assign new lists
    owners_list = []
    members_list = []

    # Assign new dictionary details
    channel_details = {}
    
    # Find the auth_user_id from input token
    auth_user_id = valid_token(token)

    # Loops to check if channel is in data file by looking from the channel_id
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            valid_channel = True
            # Assign the channel with the right channel_id into channel_data
            channel_data = channel
            # Loops to check if member is in data file by looking from the auth_user_id
            for member in channel['all_members']:
                print(channel)
                if member['auth_user_id'] == auth_user_id:
                    is_member = True
                    break
            break
    
    # Raise error message if channel is not valid or if user is not a member
    if valid_channel == False:
        raise InputError("Channel ID is not a valid channel")
    if is_member == False:
        raise AccessError("Authorised user is not a member of channel")
    
    # Assign the channel name into new dictionary channel_details
    channel_details['name'] = channel_data['name']
    
    channel_details['is_public'] = channel_data['is_public']

    # Loops through the owner_members in channel data
    # Calling the search_user_data to return the user data and assign it into owner
    # Append the user data into the list owners_list
    # Add the list owners_list into new dictionary channel_details
    for id_owner in channel_data["owner_members"]:
        owner = search_user_data(id_owner)
        owners_list.append(owner)
    channel_details['owner_members'] = owners_list

    # Loops through the all_members in channel data
    # Calling the search_user_data to return the user data and assign it into member
    # Append the user data into the list memberss_list
    # Add the list members_list into new dictionary channel_details
    for id_member in channel_data["all_members"]:
        member = search_user_data(id_member)
        members_list.append(member)
    channel_details['all_members'] = members_list
            
    # return the new dictionary
    return(channel_details)
    '''
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
    '''

def channel_messages_v2(token, channel_id, start):

    ''' 
    This function is to return the upto 50 messages between start and end  
        
    Arguments:
        auth_user_id (int) - the user ID of the members
        channel_id (int) - the ID of the channel
        start (int) - the start of an index

    Exceptions:
        InputError - Occurs when u_id or channel_id is invalid.
        InputEror - Occurs when the start index is greater than the total number of messages
        AccessError - Occurs when the authorised user is not a member of the channel
                      or the authorised user is invalid or the authorised user is 
                      inviting someone already in the channel.

    Return Value:
        Returns a dictionary return_msg that includes the message details, index start and the index end
    '''

    # Assign new variables to check
    valid_channel = False
    is_member = False

    # Assign new list msg
    msg = []
    
    # Assign new variables
    end = start + 50
    count = 0
    msg_counter = 0

    # Find the auth_user_id from input token
    auth_user_id = valid_token(token)

    # Loops to check if channel is in data file by looking from the channel_id
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel = True
            # Assign the channel with the right channel_id into channel_data
            channel_data = channel
            # Loops to check if member is in data file by looking from the auth_user_id
            for member in channel["all_members"]:
                if member["auth_user_id"] == auth_user_id:
                    is_member = True
                    break
            break
            
    # Raise error message if channel is not valid or if user is not a member
    if valid_channel == False:
        raise InputError("Channel ID is not a valid channel")
    if is_member == False:
        raise AccessError("Authorised user is not a member of channel")

    # Return Error if start position is greater than messages in data
    if start > len(channel_data['messages']):
        raise InputError("Input Error! start > messages")

    # Length of the message in the channel
    len_message = len(channel['messages'])
    
    # Loops through the channel messages
    for message in channel['messages']:
        if count < end:
            msg.append(message)
            msg_counter += 1
        count += 1

    # Return -1 if the function returned the least recent message in the channel
    # to indicate there are no more messages to load after this return.
    if len(channel['messages']) == start + msg_counter:
        end = -1

    # Return the message, start, and end
    return_msg = {'messages':msg, 'start': start, 'end':end}
    
    return(return_msg)

    '''
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
    '''

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

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
