from data import data
from src.error import AccessError

def check_valid_user(user_token):	
    """ Checks the validity of the auth_user_id, by checking if it was added to
    the data file as a part of the 'users' information."""

    # Flag to test if the user_id is valid
    valid_user_id = False 

    # Extracts the user_token from the dictionary 
    user_id = user_token['auth_user_id']
    
    # Loops through the data file to find the user_id, which would be appended 
    # to the list if auth_register_v1 was called. The flag changes to True once  
    # the user_token has been found. 
    for user in data['users']:
        if user['auth_user_id'] == user_id:
            valid_user_id = True 
            break
    
    # If the flag remains False, it is not in the authorised user list and an 
    # AccessError is printed. 
    if valid_user_id == False:
        raise AccessError("The auth_user_id input is not a valid id.")

