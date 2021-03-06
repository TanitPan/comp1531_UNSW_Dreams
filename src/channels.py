from data import data
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.extra_functions import check_valid_user

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    """ 
    channel_create_v1
    This function creates a new channel for an authorised user, which is either 
    public or private (if the authorised user is not a global Dream user). 

    Arguments:
        auth_user_id (int)  - input token that ensures a user that is given 
                              access has been validated. 
        name (string)       - name of the channel. 
        is_public (boolean) - checks whether a channel is public (assumed to be
                              the default setting) or private.
                              
    Exceptions:
        InputError  - Occurs when the name input is consists of more than 20 
                      characters as determined by the len function. 
        AccessError - Occurs when the auth_user_id has not been authenicated
                      (appended to the data['users'] file)
        
    Return Value:
        Returns a dictionary consisting of the channel_id values provided the
        auth_user_id is valid and the name is less than 20 characters in length. 
    """

    # Calls the check_valid_user function to ensure the user_id is validated 
    # (has been added to the list of users). An AccessError is else raised. 
    check_valid_user(auth_user_id)

    if len(name) > 20:
        raise InputError("The name input is more than 20 characters.")

    # Our assumptions began the channel_id at 1 and increase iteratively. To 
    # give a new channel_id, loop through the channels, record the highest id  
    # and set the new id as one greater than it. This allows for a unique id to 
    # be established without assuming the same iterative process was used. 
    maximum_id = 0
    for channel in data['channels']:
        if channel['channel_id'] > maximum_id:
            maximum_id = channel['channel_id']       
    new_id = maximum_id + 1

    # Only the channel creator has been added as user. 
    owner_list = [auth_user_id]
    all_member_list = [auth_user_id]

    # Added new channel data to the dataframe.
    new_channels = {
			    'channel_id': new_id, 
			    'name': name, 
			    'owner_members': owner_list, 
			    'all_members': all_member_list, 
                'messages' : [],
			    'ispublic': is_public,
    }

    data['channels'].append(new_channels)
    return {
	    'channel_id': new_id,
    }
