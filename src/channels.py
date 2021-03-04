def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

""" 
channel_listall_v1
This function returns the total number of channels that have been created, 
regardless of whether the user has been added to the group or not. 

Arguments:
    auth_user_id (int)  - an input token that hints that an authorised and valid
                          user is requesting for this information 
                                              
Exceptions:
    AccessError - Occurs when the auth_user_id is invalid and it doesn't belong
                  to the group

Return Value:
    Returns a list consisting of dictionaries, with the information about a 
    channel (likely to be 'channel_id' and 'name'
"""

  
def channels_listall_v1(auth_user_id):
    # an AccessError needs to be thrown when the auth_user_id passed is invalid
    channel_list = []
    for channel in all_channels:  
        channel_list.append(channel)
    return(channel_list)

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
