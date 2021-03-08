from data import data
from src.error import InputError
from src.error import AccessError
from src.helper import *

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
    ''' 
    This function is to return the detail of a channel that includes
        channel name, the owners data and the all members data 
        
    Arguments:
        auth_user_id (int) - the user ID of the person inviting
        channel_id (int) - the ID of the channel to invite a user to

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
    
    # Assign the channel name into new dictionary channel_details
    channel_details['name'] = channel_data['name']
    
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

def channel_messages_v1(auth_user_id, channel_id, start):

    # Assign new variables to check
    valid_channel = False
    is_member = False

    # Assign new list msg
    msg = []
    
    # Assign new variables
    end = start + 50
    count = 0
    msg_counter = 0

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
    if start > message:
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
