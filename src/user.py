"""
This file contains the user function implementations used by the HTTP routes
"""

from data import data
from src.error import InputError, AccessError
import re
import src.helper as helper


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
                    'name_first' : user['name_first'], 
	                'name_last' : user['name_last'], 
                    'handle_str' : user['handle_str'], 
	                'email': user['email'], 
	                'password': user['password'], 
                    'permission_id': user['permission_id'],
                },
            }
    


def user_profile_setname_v2(token, name_first, name_last):
    """
    Given an auth_user_id, valid first and last name, updates the user
    info

    Arguments:
        auth_user_id <int>    - the user's identification number, a positive integer
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
    return {
    }

def user_profile_setemail_v2(token, email):
    """
    Given an auth_user_id and valid email, updates the user info

    Arguments:
        auth_user_id <int>    - the user's identification number, a positive integer
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

    return {
    }