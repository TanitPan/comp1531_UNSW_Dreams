'''
This file contains other functions relating to the implementation of 
the backend project. 
'''
import time
import math

from src.data import data
from src.error import InputError, AccessError
import src.helper as helper

def users_all_v1(token):
    """
    Given a valid token, returns a list of users.

    Arguments:
        token <string>    - the user's token
        
    Exceptions:
        AccessError - Occurs when the token given isn't valid

    Return Value:
        Returns {} , an empty dictionary on success
    """
    helper.valid_token(token) # Raises AccessError on invalid token
    users = []
    for user in data['users']:
        #users.append(user)
        # return custom user data
        myuser = {
            'auth_user_id': user['auth_user_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str']
        }
        users.append(myuser)
    
    return {
        'users': users
    }

def users_stats_v1(token):
    """
    Given a valid token, fetches the required statistics about the use of UNSW Dreams

    Arguments:
        token <string>    - the user's token
        
    Exceptions:
        AccessError - Occurs when the token given isn't valid

    Return Value:
        Returns {dreams_stats} on success
    """
    helper.valid_token(token) # Raises AccessError on invalid token

    num_users_who_have_joined_at_least_one_channel_or_dm = 0

    unique_ids = []
    for channel in data['channels']:
        for id in channel['all_members']:
            if id not in unique_ids:
                unique_ids.append(id)
    
                
    num_users_who_have_joined_at_least_one_channel_or_dm = len(unique_ids)

    total_num_users = len(data['users'])
    util_rate = num_users_who_have_joined_at_least_one_channel_or_dm / total_num_users

    #num_channels_exist = data['channels_exist'][-1]['num_channels_exist']
    #num_dms_exist = data['dms_exist'][-1]['num_dms_exist']
    #num_messages_exist = data['messages_exist'][-1]['num_messages_exist']
    return {
        'channels_exist': data['channels_exist'],
        'dms_exist': data['dms_exist'],
        'messages_exist': data['messages_exist'],
        'utilization_rate': util_rate
    }

def clear_v1():
    '''
    Clears all data from the dataframe
    '''
    data['users'].clear()
    data['channels'].clear()
    data['channels_exist'].clear()
    data['messages_exist'].clear()
    data['dms_exist'].clear()
    # new dreams instance requires initialisation of dreams analytics timestamps
    timestamp = math.floor(time.time())
    data['channels_exist'].append({'num_channels_exist': 0, 'timestamp': timestamp})
    data['messages_exist'].append({'num_messages_exist': 0, 'timestamp': timestamp})
    data['dms_exist'].append({'num_dms_exist': 0, 'timestamp': timestamp})
    # Save the data persistently
    helper.save_data(data)
    
def search_v2(token, query_str):
    '''
    Returns a collection of messages that contain the substring, query_str, in 
    its exact forms. These will only contain the DM_ids that have been sent to 
    a channel as implied by channels/DM in 6.2. 
    
    Arguments:
        token (string) - an input token that signals an authorised and valid 
                         user has signed in or registered
        query_str (string) - substring containing the message that needs to be
        
    Exceptions:
        InputError  - Occurs when the query string contains more than 1000 
                      characters
        AccessError - Occurs when the token is invalid and it doesn't 
                      belong to the group
    Return Value:
        Returns a list of dictionaries, with information about a message
         ('message_id', 'u_id', 'message', 'time_created')
    '''         
    # Confirms that the token is valid and that the query string is less than 
    # 1000 characters. Otherwise, an error is raised.    
    auth_user_id = helper.valid_token(token)
    if len(query_str) > 1000:
        raise InputError("Query string is too long")
        
    # Created empty list, looping through the channels. If the user is a member 
    # of the channel and they have sent a DM, it will append this message to 
    # the list as a dictionary and return this list 
    messages_list = []
    for channel in data["channels"]:
        for member in channel['all_members']:
            if auth_user_id == member['auth_user_id'] and channel["dm_id"] == -1: 
                for message in channel["messages"]:
                    if query_str in  message["message"]:
                        mess_dict = {
                            "message_id": message["message_id"] ,
                            "u_id": message["auth_user_id"] , 
                            "message": message["message"], 
                            "time_created": message["timestamp"],
                        }
                        messages_list.append(mess_dict)
    return {
        'messages': messages_list
    }
