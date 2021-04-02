'''
This is a helper file containing useful functions used in other files
'''

from data import data
import re
import jwt
from src.error import InputError, AccessError

# Valid email input
RE = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
SECRET = 'COMP1531'

def check_email_valid(email):
    '''
    Check that email is valid, given an email and using a regex, returns an
    InputError otherwise
    '''
    if not re.search(RE, email):
        raise InputError("Invalid email")

def search_email(email):
    '''
    A function which searches the database for a user with a given email, returns
    their email if found, and None otherwise
    '''
    for user in data['users']:
        if user['email'] == email:
            return user
    return None

def check_password_valid(password):
    '''
    A function which checks if a password is valid, raises InputError if not
    '''
    if len(password) < 6:
        raise InputError("Invalid password")

def check_name_length(name):
    '''
    A function which checks whether a name is between 1 and 50 characters inclusively,
    raises InputError otherwise
    '''
    if len(name) not in range(1, 51):
        raise InputError("Invalid name length")

def generate_auth_user_id():
    '''
    A function which generates a new users auth_user_id and returns it,
    simply giving users an id equal to the number of users already registered
    '''
    return len(data['users'])

def search_handle(handle):
    '''
    A function which searches the user database for a user with a handle, 
    and returns that user if found, otherwise, return None
    '''
    for user in data['users']:
        if user['handle_str'] == handle:
            return user
    return None

def generate_handle(name_first, name_last):
    '''
    Generates a handle_str that is the
    concatenation of a lowercase-only first name and last name.If the concatenation is 
    longer than 20 characters, it is cutoff at 20 characters. The handle will not include 
    any whitespace or the '@' character. If the handle is already taken, append the 
    concatenated names with the smallest number(starting at 0) that forms a new handle 
    that isn't already taken. The addition of this final number may result in the handle 
    exceeding the 20 character limit. Description sourced from project specs
    '''
    handle = name_first + name_last
    handle = handle.lower()
    handle = handle[:20]
    # Check that no user already owns the handle
    if search_handle(handle) is not None: # If another user owns the handle
        i = 0
        handle = handle + str(i)
        while search_handle(handle) is not None:
            # If the number resulted in a non-unique handle, remove it and iteratively
            # add another one
            if i != 0: 
                handle = handle[-1]
            i += 1
            handle = handle + str(i)
    return handle

def check_password(user, password):
    '''
    This is a function which checks if a given password matches the user's
    password. Returns their auth_user_id value if correct and InputError
    otherwise
    '''
    if user['password'] == password:
        return user['auth_user_id']
    raise InputError

def check_valid_user(user_token):	
    """ Checks the validity of the auth_user_id, by checking if it was added to
    the data file as a part of the 'users' information."""

    # Flag to test if the user_id is valid
    valid_user_id = False 
    
    # Loops through the data file to find the user_id, which would be appended 
    # to the list if auth_register_v1 was called. The flag changes to True once  
    # the user_token has been found. 
    for user in data['users']:
        if user['auth_user_id'] == user_token:
            valid_user_id = True 
            break
    
    # If the flag remains False, it is not in the authorised user list and an 
    # AccessError is printed. 
    if valid_user_id == False:
        raise AccessError("The auth_user_id input is not a valid id.")

def generate_token(auth_user_id):
    """
    A function which given a auth_user_id, generates a token for that user and returns
    it
    """
    return jwt.encode({'auth_user_id': auth_user_id}, SECRET, algorithm='HS256')

def valid_token(token):
    """
    A function which, given a token, returns the auth_user_id if valid, or an
    Access Error if the token is invalid
    """
    decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
    id = decoded['auth_user_id']
    for user in data['users']:
        if (id == user['auth_user_id']):
            return id
    
    raise AccessError("Token is invalid")

def decrypt_token(token):
    """
    A function which returns a user's auth_user_id given a valid token
    """
    valid_token(token)
    return jwt.decode(token, SECRET, algorithms=['HS256'])
