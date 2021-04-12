'''
This is a helper file containing useful functions used in other files
'''

from data import data
import re
import jwt
import json
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

def check_valid_user(u_id):	
    """ Checks the validity of the auth_user_id, by checking if it was added to
    the data file as a part of the 'users' information."""

    # Flag to test if the user_id is valid
    valid_user_id = False 
    
    # Loops through the data file to find the user_id, which would be appended 
    # to the list if auth_register_v1 was called. The flag changes to True once  
    # the user_token has been found. 
    for user in data['users']:
        if user['auth_user_id'] == u_id and user['name_first'] != 'Removed':
            valid_user_id = True 
            break
    
    # If the flag remains False, it is not in the authorised user list and an 
    # InputError is printed. 
    if valid_user_id == False:
        raise InputError("The auth_user_id input is not a valid id.")

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
    
def check_only_dreams_owner(u_id):
    """ A function which tests whether the given user is the only owner of the
    dreams channel, by checking their permission"""   
    dream_owners = []
    for user in data['users']:
        if user['permission_id'] == 1:
            owners_dict = {'auth_user_id': user['auth_user_id']}
            dream_owners.append(owners_dict)
    number_owners = len(owners_dict)
    for owner in dream_owners:
        if owner['auth_user_id'] == u_id and number_owners == 1:
            raise InputError("This user is the only owner of Dreams")

def check_dreams_owner(auth_user_id):
    """Confirm that the authorised user is an owner of Dreams by checking their
    permission ID in data['users']"""
    valid_dreams_owner = False
    for user in data['users']:
        if user['auth_user_id'] == auth_user_id and user['permission_id'] == 1: 
            valid_dreams_owner = True
            break       
    if valid_dreams_owner == False:
        raise AccessError("The authorised user is not an owner of Dreams")  

def valid_channel(channel_id):
    """
    This function checks if channel_id is valid. Return channel_id if valid and 
    raise an InputError exception otherwise.
    """
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            return channel_id

    raise InputError(description = "channel_id is not a valid channel")

def check_existing_owner(u_id, channel_id):
    """ This functions checks if the user id belongs to an existing owner. 
    Returns the result of the flag already_owner as True or False"""
    for channel in data['channels']:	
        already_owner = False 
        if channel["channel_id"] == channel_id:
            for owner in channel['owner_members']:
	            if u_id == owner["auth_user_id"]:
		            already_owner = True 
		            break
    return already_owner
    
def save_data(data):
    """ This function contains a possible way to keep data persistence by 
    dumping it into a file"""
    output = "data = " +json.dumps(data) 
    # Edits the boolean features so they capitalised 
    output = output.replace("true", "True")
    output = output.replace("false", "False")
    # Writes it to the file
    f = open("data.py", "w+")		
    f.write(output)
    f.close()

def valid_member(user_id, channel_id):
    """ This function checks if someone is a member of a channel, raising an 
    AccessError if they aren't"""
    valid_member = False
    for channel in data['channels']:	
        if channel_id == channel["channel_id"]:
            for member in channel['all_members']:     
                if member['auth_user_id'] == user_id:
                    valid_member = True
     
    if not valid_member:
        raise AccessError("The authorised user is not an member of the channel")  
