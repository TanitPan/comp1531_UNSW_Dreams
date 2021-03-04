from src.error import InputError, AccessError
import data 
from src.auth import auth_register_v1
#from src.extra_functions import check_valid_user
def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

""" 
channel_create_v1
This function creates a new channel for an authorised user, which is either 
public or private (if the authorised user is not a global Dream user). 

Arguments:
    auth_user_id (int)  - input token that ensures a user that is given access 
                         has been validated. 
    name (string)       - name of the channel. 
    is_public (boolean) - checks whether a channel is public (assumed to be the
                          default setting) or private.
                          
Exceptions:
    InputError  - Occurs when the name input is consists of more than 20 
                  characters as determined by the len function. 
    AccessError - Occurs when ...

Return Value:
    Returns a dictionary consisting of the channel_id values provided that the 
    auth_user_id is valid and the name is less than 20 characters in length. 
"""
authorised_users = []

def channels_create_v1(auth_user_id, name, is_public):
    all_users = data.data['users']
    all_channels = data.data['channels']
    #global authorised_users
    #check_valid_user(auth_user_id, authorised_users)
    if len(name) > 20:
        raise InputError("The name input is more than 20 characters.")
    maximum_id = 0
    for channel in all_channels:
        if channel['channel_id'] > maximum_id:
            maximum_id = channel['channel_id']       
    new_id = maximum_id + 1
    owner_list = [auth_user_id]
    all_member_list = [auth_user_id]
    """new_channels = {'channel_id': new_id, 'name': name, 
                  'owner_members': owner_list, 
                  'all_members': all_member_list, 'ispublic': is_public,}
    all_channels.append(new_channels)"""
    return_value = {'channel_id': new_id}
    return (return_value)
    """return {
        'channel_id': 1,
    }"""
