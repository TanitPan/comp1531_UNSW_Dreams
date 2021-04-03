'''
This file contains other functions relating to the implementation of 
the backend project. Currently contains the clear function
'''

from data import data

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
