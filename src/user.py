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
        raise InputError
    
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
                    'permission_id'  = user['permission_id'],
                }
            }


def user_profile_setname_v1(auth_user_id, name_first, name_last):
    """
    <Brief description of what the function does>

    Arguments:
        <name> (<data type>)    - <description>
        <name> (<data type>)    - <description>
        ...

    Exceptions:
        InputError  - Occurs when ...
        AccessError - Occurs when ...

    Return Value:
        Returns <return value> on <condition>
        Returns <return value> on <condition>
    """
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    """
    <Brief description of what the function does>

    Arguments:
        <name> (<data type>)    - <description>
        <name> (<data type>)    - <description>
        ...

    Exceptions:
        InputError  - Occurs when ...
        AccessError - Occurs when ...

    Return Value:
        Returns <return value> on <condition>
        Returns <return value> on <condition>
    """
    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    """
    <Brief description of what the function does>

    Arguments:
        <name> (<data type>)    - <description>
        <name> (<data type>)    - <description>
        ...

    Exceptions:
        InputError  - Occurs when ...
        AccessError - Occurs when ...

    Return Value:
        Returns <return value> on <condition>
        Returns <return value> on <condition>
    """
    return {
    }