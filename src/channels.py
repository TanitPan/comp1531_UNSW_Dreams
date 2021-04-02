''' This file implements channels_list, channels_listall and channels_create '''

from data import data
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.helper import valid_token

def channels_list_v2(token):
    '''
    Taking in the auth_user_id, this function returns all channels the 
    authorised user has access to 
    Arguments:
        token (string) - an input token that hints that an authorised and
                          valid user is requesting for this information 
                                                  
    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid and it doesn't 
                      belong to the group
    Return Value:
        Returns a list consisting of dictionaries, with information about a 
        channel ('channel_id' and 'name')
    ''' 
    
    # Check the user_id from the token to ensure that the user was valid 
    auth_user_id = valid_token(token)
   
    # Created an empty list to store the information of the channels the 
    # authorised user has access to.
    authorised_channels = []
    for channel in data['channels']:
        for member in channel['all_members']:
            # Checked for member, as owners will automatically be included as 
            # members of the channel. 
            if auth_user_id == member['auth_user_id']: 
                new_dict = {
                    'channel_id': channel['channel_id'], 
                    'name': channel['name'],}
                authorised_channels.append(new_dict)
                break 
    # Return a dictionary structure with its value a list of dictionaries
    return {
        'channels': authorised_channels
    }
       
def channels_listall_v2(token):
    ''' 
    This function returns the total number of channels that have been created, 
    regardless of whether the user has been added to the group or not. 

    Arguments:
        token (string)    -  an input token that hints that an authorised and 
                             valid user is requesting for this information 
                                                  
    Exceptions:
        AccessError - Occurs when the token is invalid and it wasn't generated 
                      by someone belonging to the user group

    Return Value:
        Returns a list consisting of dictionaries with information about a 
        channel ('channel_id' and 'name')
    '''

    # An AccessError is raised when the token passed is not authorised
    valid_token(token)
    
    # Create an empty list to store the channel_id and name of all channels. 
    # Loop through all of the channels and append each of these to the list. 
    channels_list = []
    for channel in data['channels']:
        all_channel_dict = {
            'channel_id': channel['channel_id'], 
            'name': channel['name'],
        }
        channels_list.append(all_channel_dict)
     
    # A dictionary with a value of a list of dictionaries is returned
    return {
        'channels': channels_list
    }

def channels_create_v2(token, name, is_public):
    ''' 
    This function creates a new channel for an authorised user, which is either 
    public or private (if the authorised user is not a global Dream user). 

    Arguments:
        token (string)      - input token that ensures a user that is given 
                              access has been validated. 
        name (string)       - name of the channel. 
        is_public (boolean) - checks whether a channel is public (assumed to be
                              the default setting) or private.
                              
    Exceptions:
        InputError  - Occurs when the name input is consists of more than 20 
                      characters as determined by the len function. 
        AccessError - Occurs when the token has not been authenicated
                      (appended to the data['users'] file)
        
    Return Value:
        Returns a dictionary consisting of the channel_id values provided the
        token is valid and the name is less than 20 characters in length. 
    '''

    # Calls the valid_token function to ensure the token is validated, returning
    # the user_id if it has been. An AccessError is else raised. 
    auth_user_id = valid_token(token)

    # Raises InputError if the length of the name is greater than 20 characters
    if len(name) > 20:
        raise InputError('The name input is more than 20 characters.')

    # Our assumptions began the channel_id at 1 and increase iteratively. To 
    # give a new channel_id, loop through the channels, record the highest id  
    # and set the new id as one greater than it. This allows for a unique id to 
    # be established without assuming the same iterative process was used. 
    maximum_id = 0
    for channel in data['channels']:
        if channel['channel_id'] > maximum_id:
            maximum_id = channel['channel_id']       
    new_id = maximum_id + 1
    
    # Iteratively add the messages id, ensuring it is one greater than the last
    # added messages _id
    current_messages_id = 0
    for channel in data['channels']:
        for messages in channel['messages']:
            if messages['message_id'] > current_messages_id:
                current_messages_id = messages['message_id']  
    new_messages_id = current_messages_id + 1

    # Only the channel creator has been added as user. 
    owner_list = [{'auth_user_id': auth_user_id}]
    all_member_list = [{'auth_user_id': auth_user_id}]

    # Added new channel data to the dataframe.
    new_channels = {
        'channel_id': new_id, 
        'name': name, 
        'owner_members': owner_list, 
        'all_members': all_member_list, 
        'is_public': is_public,
        'dm_id': -1, #assume default
        'messages': [
            {
                'message_id' : new_messages_id, #Assuming it is greater than 0
                'message' : '',
                'timestamp' : 0, # will replace this with the correct timestamp 
                'auth_user_id' : auth_user_id, 
            }
        ]
    }

    data['channels'].append(new_channels)
    return {
	    'channel_id': new_id,
    }


