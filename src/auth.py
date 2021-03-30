'''
This file contains the implementation of auth_login_v1 and auth_register_v1
'''
import jwt

from data import data
from src.error import InputError
import re
import src.helper as helper

def auth_login_v2(email, password):
    '''
    This function returns the auth_user_id of a user given a valid
    and existing email and password

    Arguments:
        email (str) - a string of the user's email
        password (str) - a string of the user's password 

    Exceptions:
        InputError - Occurs when email doesn't match regex specs
        InputError - Occurs when email doesn't belong to a user
        InputError - Occurs when the password is incorrect

    Return value: 
        returns {auth_user_id : auth_user_id} on successful login
    '''
    # Check that the email is valid
    helper.check_email_valid(email)

    # Check that the email belongs to a user, raise InputError else
    user = helper.search_email(email)
    if user is None:
        raise InputError
    
    # Check that the password is valid
    id = helper.check_password(user, password)

    # Return their auth_user_id
    return {
        'auth_user_id': id,
    }

def auth_register_v2(email, password, name_first, name_last):
    '''
    This function registers a user to the dataframe, given a valid email, password, first
    name and last name. Returns their auth_user_id

    Arguments:
        email (str) - a string of the user's email
        password (str) - a string of the user's password
        name_first (str) - a string of the user's first name
        name_last (str) - a string of the user's last name

    Exceptions:
        InputError - Occurs when email doesn't match regex specs
        InputError - Occurs when email is taken by another user
        InputError - Occurs when password is less than 6 characters
        InputError - Occurs when name_first and name_last are not within
                     1 and 50 characters inclusively in length

    Return value:
        returns {
            'auth_user_id' : auth_user_id,
            'token' token
        } on successful registration
    '''
    # Check that email is valid
    helper.check_email_valid(email)
    # Check that email isn't taken, raise InputError if it is
    if helper.search_email(email) is not None:
        raise InputError
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
        'permission_id': permission_id, #1 for owner, 2 for member 
    })
    return {
        'auth_user_id': id,
        'token': helper.generate_token(id)
    }
