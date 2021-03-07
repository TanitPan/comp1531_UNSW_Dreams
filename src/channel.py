from data import data
from src.error import InputError
from src.error import AccessError
from src.helper import *

'''
def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }
'''
##########################################################################################
'''

'''

def channel_details_v1(auth_user_id, channel_id):
    # Initialize variable
    valid_channel = False
    is_member = False

    details = {}
    
    # Checking channel_id is valid
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel = True

            # check if auth_user_id is member of channel_id
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
    
    # assign name
    for channel in data["channels"]:
         if channel["channel_id"] == channel_id:
            channel_data = channel
    details['name'] = channel_data['name']

    # assign owners data
    owners = []
    for id_owner in channel_data["owner_members"]:
        owner = search_user(id_owner)
        if owner['auth_user_id'] != -1:
            owners.append(owner)
    details['owner_members'] = owners

    # assign members data
    members = []
    for id_member in channel_data["all_members"]:
        member = search_user(id_member)
        if member['auth_user_id'] != -1:
            members.append(member)
    details['all_members'] = members
            
    # return the new dictionary
    return(details)

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

#########################################################################################
'''
def channel_messages_v1(auth_user_id, channel_id, start):
    msg = []
    
    # Initianlize variables
    valid_channel = False
    is_member = False
    
    # Checking if auth_user_id and channel_id is valid
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel = True
            for member in channel["all_members"]:
                if member["auth_user_id"] == auth_user_id:
                    is_member == True
                    break
            break
            
    #  Return Error if channel_id and auth_user_id is not Valid/ not part of the channel
    if valid_channel == False:
        raise InputError("Channel ID is not a valid channel")
    if is_member == False:
        raise AccessError("Authorised user is not a member of channel with")
    
    # Length of the message in the channel
    len_message = len(channel['messages'])
    
    # Return Error if start position is greater than messages in data
    if start > message:
        raise InputError("Input Error! start > messages")
    
    
    end = start + 50
    count = 0
    msg_counter = 0
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
    

########################################################################################

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
'''
