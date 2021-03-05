'''
This file contains the implementation of auth_login_v1 and auth_register_v1
'''

from data import data
from src.error import InputError
import re
import helper

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):
    '''
    This function registers a user to the dataframe, given a valid email, password, first
    name and last name. Returns their auth_user_id
    '''
    # Check that email is valid
    helper.check_email_valid(email)
    # Check that email isn't taken, return InputError if it is
    if helper.search_email(email) is not None:
        return InputError
    # Check that the password is valid
    helper.check_password_valid(password)
    # Check the name_first and name_last length
    helper.check_name_length(name_first)
    helper.check_name_length(name_last)
    
    # Generate an auth_user_id
    id = helper.generate_auth_user_id()
    # Generate a handle_str
    handle = helper.generate_handle(name_first, name_last)

    # If the user is the first user registering, give them global ownership
    # permissions
    if id == 0:
        permission_id = 1 # global owner
    else:
        permission_id = 2 # global member

    # Register data to the dataframe
    data['users'].append({
        'auth_user_id' : id, 
	    'name_first' : name_first, 
	    'name_last' : name_last, 
        'handle_str' : handle, 
	    'email': email, 
	    'password': password, 
        'permission_id'  = permission_id, #1 for owner, 2 for member 
    })
    
    return {
        'auth_user_id': id,
    }
