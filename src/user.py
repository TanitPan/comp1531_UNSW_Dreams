"""
This file contains the user function implementations used by the HTTP routes
"""

from data import data
from src.error import InputError, AccessError
import re
import src.helper as helper

import time

def user_profile_v2(token, u_id):
    """
    A function which, given a valid token, and a valid user_id, returns the
    'user' dictionary containing the user's information

    Arguments:
        token <string> - the user's hashed auth_user_id 
        u_id <int> - the user's user id, a positive integer
        ...

    Exceptions:
        InputError  - Occurs when user with u_id is not a valid

    Return Value:
        Returns {user} dictionary containing the user's information
        
    """
    try:
        helper.check_valid_user(u_id) # Raises AccessError when u_id is invalid
        helper.valid_token(token) # Raises AccessError when u_id is invalid
    except AccessError:
        raise InputError from AccessError

    
    # Find the user with the given data
    for user in data['users']:
        if u_id == user['auth_user_id']:
            return {
                'user': {
                    'auth_user_id': user['auth_user_id'],
                    'email': user['email'],
                    'name_first' : user['name_first'], 
	                'name_last' : user['name_last'], 
                    'handle_str' : user['handle_str'] 	                 
                },
            }
    


def user_profile_setname_v2(token, name_first, name_last):
    """
    Given an auth_user_id, valid first and last name, updates the user
    info

    Arguments:
        token <string> - the user's hashed auth_user_id 
        name_first <string>    - the new name the user wants to use
        name_last <string> - the new name the user wants to use

    Exceptions:
        InputError  - Occurs when name_first is not between 1 and 50 characters inclusively in length
        InputError  - Occurs when name_last is not between 1 and 50 characters inclusively in length
        AccessError - Occurs when the token given isn't valid

    Return Value:
        Returns {} , an empty dictionary on success
    """    
    # Validate the length of the name, return InputError if invalid
    helper.check_name_length(name_first)
    helper.check_name_length(name_last)

    id = helper.decrypt_token(token) # Also validates the token, raises AccessError when token is invalid
    # Change the name associated with the user
    for user in data['users']:
        if user['auth_user_id'] == id:
            user['name_first'] = name_first
            user['name_last'] = name_last
            break
    # Save the data persistently
    helper.save_data(data)
    return {
    }

def user_profile_setemail_v2(token, email):
    """
    Given an auth_user_id and valid email, updates the user info

    Arguments:
        token <string> - the user's hashed auth_user_id 
        email <string>        - the user's email

    Exceptions:
        InputError  - Email entered is not a valid email
        InputError  - Email address is already being used by another user
        AccessError - Occurs when the token given isn't valid

    Return Value:
        Returns {} , an empty dictionary on success
    """
    helper.check_email_valid(email) # Raises InputError if email is invalid
    if helper.search_email(email) is not None:
        raise InputError("Email is taken")
    
    id = helper.decrypt_token(token) # Also validates the token, raises AccessError when token is invalid
    # Change the name associated with the user
    for user in data['users']:
        if user['auth_user_id'] == id:
            user['email'] = email
            break
    # Save the data persistently
    helper.save_data(data)
    return {
    }

def user_profile_sethandle_v1(token, handle_str):
    """
    Given an auth_user_id and valid handle_str, updates the user's info

    Arguments:
        auth_user_id <int>    - the user's identification number, a positive integer
        handle_str <string>   - the user's handle

    Exceptions:
        InputError  - Handle entered is not a valid handle
        InputError  - handle_str is already being used by another user
        AccessError - Occurs when the token given isn't valid

    Return Value:
        Returns {} , an empty dictionary on success
    """
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Invalid handle_str")
    if helper.search_handle(handle_str) is not None:
        raise InputError("Handle_str is taken")
    
    for user in data['users']:
        if user['auth_user_id'] == id:
            user['handle_str'] = handle_str
            break
    # Save the data persistently
    helper.save_data(data)
    return {
    }

def user_stats_v1(token):
    """
    Given a valid token, Fetches the required statistics about this user's use of UNSW Dreams

    Arguments:
        token <string> - the user's hashed auth_user_id 

    Exceptions:
        AccessError - Occurs when the token given isn't valid

    Return Value:
        Returns {user_stats}
    """
    id = helper.valid_token(token) # Also validates the token, raises AccessError when token is invalid

    found = False
    for user in data['users']:
        if id == user['auth_user_id']:
            myUser = user        
            #if len(user['channels_joined']) > 0:
            print(user['channels_joined'])
            num_channels_joined = user['channels_joined'][-1]['num_channels_joined']
      
            #if len(user['dms_joined']) > 0:
            num_dms_joined = user['dms_joined'][-1]['num_dms_joined']

            #if len(user['messages_sent']) > 0:
            num_messages_sent = user['messages_sent'][-1]['num_messages_sent']
            
            found = True
            
    if found == False:
        raise(InputError)

    num_dreams_channels = 0
    for channel in data['channels']:
        if channel['dm_id'] == -1: # indicates a channel and not a DM
            num_dreams_channels += 1

    num_dreams_dms = 0
    for channel in data['channels']:
        if channel['dm_id'] == 1: # indicates a DM and not a channel
            num_dreams_dms += 1
    
    num_dreams_msgs = 0
    for channel in data['channels']:
        num_dreams_msgs += len(channel['messages'])

    numerator = num_channels_joined + num_dms_joined + num_messages_sent
    denominator = num_dreams_channels + num_dreams_dms + num_dreams_msgs
    if denominator == 0:
        involvement_rate = 0
    else:
        involvement_rate = numerator/denominator
    return {
        'channels_joined': myUser['channels_joined'],
        'dms_joined': myUser['dms_joined'],
        'messages_sent': myUser['messages_sent'],
        'involvement_rate': involvement_rate
    }
