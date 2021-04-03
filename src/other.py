'''
This file contains other functions relating to the implementation of 
the backend project. Currently contains the clear function.
'''

from data import data
from src.error import InputError, AccessError
import src.helper as helper

def users_all_v1(token):
    """
    Given a valid token, returns a list of users.

    Arguments:
        token <string>    - the user's token
        
    Exceptions:
        AccessError - Occurs when the token given isn't valid

    Return Value:
        Returns {} , an empty dictionary on success
    """
    helper.valid_token(token) # Raises AccessError on invalid token
    users = []
    for user in data['users']:
        users.append(user)
    
    return {
        'users': users
    }


def clear_v1():
    '''
    Clears all data from the dataframe
    '''
    data['users'].clear()
    data['channels'].clear()
    

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
