from data import data
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.extra_functions import check_valid_user

def channels_list_v1(auth_user_id):
    """ Taking in the auth_user_id, this function returns all channels the 
    authorised user has access to 
    Arguments:
        auth_user_id (int) - an input token that hints that an authorised and
                             valid user is requesting for this information 
                                                  
    Exceptions:
        AccessError - Occurs when the auth_user_id is invalid and it doesn't 
                      belong to the group

    Return Value:
        Returns a list consisting of dictionaries, with the information about a 
        channel (likely to be 'channel_id' and 'name'
    """    
    check_valid_user(auth_user_id)
    authorised_channels = []
    for channel in data['channels']:
        print(channel)
        members = channel['users']
        for member in members:
            if userID == member: #as owners are included as members of the channel 
                authorised_channels.append(channel)
                #assuming only one user can be member once
                break 
    return authorised_channels
       
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
    return {
        'channel_id': 1,
    }
