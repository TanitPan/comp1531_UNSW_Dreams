from src.config import url
import pytest
import json
import requests

def test_channel_details_initial():
    """
    This function checks if the user is successfully
    added to the channel and store in the data structure.
    """
    # Clear the data
    requests.delete(f"{url}/clear/v1")

    # Call other routes to create the data and store in data structure
    user1 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'johnsmith@gmail.com',
        'password': 'password123',
        'name_first': 'John',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user1.json()['token'], 
        'name': 'Channel1', 
        'is_public': True
    })

    res = requests.get(f"{url}/channel/details/v2", params = {
        'token': user1.json()['token'], 
        'channel_id': channel1.json()['channel_id']
    }) 

    # Check if the HTML request is successful
    assert res.status_code == 200

    payload = res.json()
    assert payload == {
        'name': 'Channel1',
        'is_public': True, 
        'owner_members': [
            {'auth_user_id': 1, 'name_first': "John", 'name_last': "Smith",}
        ],
        'all_members': [
            {'auth_user_id': 1, 'name_first': "John", 'name_last': "Smith",}
        ]
    }
