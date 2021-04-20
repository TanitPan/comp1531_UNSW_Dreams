''' This file implements channels_list, channels_listall and channels_create '''

from src.data import data
from src.error import InputError, AccessError
from src.helper import (valid_token, check_valid_user, check_only_dreams_owner, 
check_dreams_owner, save_data)

def admin_user_remove_v1(token, u_id):
    '''
    Taking in the token and a user_id, this function removes the account of an
    user with that user_id from the entire Dreams channel, removing them from 
    the list of channels, and replacing their messages id and name in the user
    list with 'Removed user'
    
    Arguments:
        token (string) - input token that allows the user to stay for a session
        u_id (integer) - user id of a valid user who is accessing Dreams
                                  
    Exceptions:
        InputError - Occurs when the user is the only owner of Dreams
                   - Also occurs when the u_id does not refer to an user who is
                     included as part of the data[users] section
       AccessError - Occurs when the authorised user (the one who is inputting
                     the token) is not an owner of Dreams
                   - Occurs when the token has not been authenicated validly
    Return Value:
        Returns an empty dictionary
    '''
    # Call helper functions to test that the token is valid and belongs to a 
    # Dreams owner and the u_id belongs to a valid user, who is not the only 
    # Dreams owner 
    auth_user_id = valid_token(token)
    check_dreams_owner(auth_user_id)
    check_valid_user(u_id)
    check_only_dreams_owner(u_id)
    
    # If it has passed all the error testing, change the name in users to read
    # 'removed users' when profile is called 
    for user in data['users']:
        if user['auth_user_id'] == u_id: 
            user['name_first'] = 'Removed'
            user['name_last'] = 'user'
  
    # Loop through channels and remove the user, whose auth_user_id matches the 
    # inputted u_id in both the members and owners section.
    for channel in data['channels']:	
        for member in channel['all_members']:     
            if member['auth_user_id'] == u_id: 
                channel['all_members'].remove(member)
        for owner in channel['owner_members']:     
            if owner['auth_user_id'] == u_id: 
                channel['owner_members'].remove(member)
        # Replace all of the contents of the messages with 'Removed user'
        for message in channel['messages']:
            if message['auth_user_id'] == u_id:
                message.clear()
                message = "Removed user"
    
    # Writes data to file for persistence
    save_data(data)
    # Return an empty dictionary			
    return {
    }

def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Taking in a token, u_id and permission_id, this function alters the global
    Dreams permission of the user with the user id to either 1 (owner) or 2
    (member)
    Arguments:
        token (string) - input token that allows the user to stay for a session
        u_id (integer) - user id of a valid user who is accessing Dreams
        permission_id (integer) - id informing whether someone is an owner or
                                   member of dreams              
    Exceptions:
        InputError - Occurs if the u_id does not refer to an user who is
                     included as part of the data[users] section
                   - Also is raised when the permission_id is not an integer, 
                    and thus cannot refer to a value permission          
       AccessError - Occurs when the authorised user (the one who is inputting
                     the token) is not an owner of Dreams
                   - Again, occurs when the token has not been authenicated
                      (appended to the data['users'] file)
    Return Value:
        Returns an empty dictionary
    '''
	# Calls the valid_token and check_valid_user function to ensure the token, 
	# user_id and authorised_user have have been validated. An AccessError is 
	# otherwise raised. 
    auth_user_id = valid_token(token)
    check_valid_user(u_id)
    check_dreams_owner(auth_user_id)
    # Raise an InputError if the permission_id is not an integer value 
    if permission_id != 1 and permission_id != 2:
        raise InputError("Permission ID does not refer to a valid value")
	
	# If it passes all the tests, loop through the user data until the id 
	# matches the inputted data. Edit the permission_id for that user to the
	# permitted permission_id.  
    for user in data['users']:
        if user["auth_user_id"] == u_id:
            user['permission_id'] = permission_id
            break
    
    # Writes data to file for persistence
    save_data(data)
    
    # Return an empty dictionary			
    return {
    }
    

