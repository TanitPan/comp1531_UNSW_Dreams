"""
This file contain the test for channel_invite_v2 HTTP implementation 
"""
from src.config import url
from src.helper import generate_token
import src.channel as channel
import src.channels as channels
import src.auth as auth
import pytest
import json
import requests


def test_channel_invite_valid():
    """
    This function checks if the new user 
    detail added to the channel is correct.
    """

    # Clear the data
    requests.delete(f"{url}/clear/v1")

    # Users information to be pass in as json
    user1_data = {
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first": "john",
        "name_last": "smith",
    }
    
    user2_data = {
        "email": "michaelbush@gmail.com",
        "password": "123456",
        "name_first": "michael",
        "name_last": "bush",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    
    auth_id2 = payload["auth_user_id"]
    token2 = payload["token"]

    channels_response = requests.post(f"{url}/channels/create/v2", json = {
        "token": token1, 
        "name": "Channel1", 
        "is_public": True
    })

    payload = channels_response.json()
    
    channel_id = payload["channel_id"]   
    invite_response = requests.post(f"{url}/channel/invite/v2", json = {
            "token": token1,
            "channel_id": channel_id,
            "u_id": auth_id2
    })

    # Check if the HTML request is successful
    assert invite_response.status_code == 200

    res = requests.get(f"{url}/channels/list/v2", params= {'token': token2})
    payload = res.json()
    
    assert payload == {
        'channels': [
        	{
        		'channel_id': 1, # channel id start at 1 or 0 is worth checking ?
        		'name': 'Channel1',
        	}
        ] 
    }

    
def test_channel_invite_except_channel():
    """
    This function tests error for invalid channel
    being used as an input.
    """
    # Clear the data
    requests.delete(f"{url}/clear/v1")

    # Users information to be pass in as json
    user1_data = {
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first": "john",
        "name_last": "smith",
    }
    
    user2_data = {
        "email": "michaelbush@gmail.com",
        "password": "123456",
        "name_first": "michael",
        "name_last": "bush",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    
    auth_id2 = payload["auth_user_id"]
    invalid_channel = 55
    

    requests.post(f"{url}/channels/create/v2", json = {
        "token": token1, 
        "name": "Channel1", 
        "is_public": True
    })

    invite_response = requests.post(f"{url}/channel/invite/v2", json = {
            "token": token1,
            "channel_id": invalid_channel,
            "u_id": auth_id2
    })

    # Test invalid channel by checking if 400 status code is raised
    assert invite_response.status_code == 400

def test_channel_invite_except_user():
    """
    This function tests error for invalid u_id
    being invited to the channel.
    """

    # Clear the data
    requests.delete(f"{url}/clear/v1")

    # Users information to be pass in as json
    user1_data = {
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first": "john",
        "name_last": "smith",
    }
    
    user2_data = {
        "email": "michaelbush@gmail.com",
        "password": "123456",
        "name_first": "michael",
        "name_last": "bush",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    
    invalid_u_id = 2222

    channels_response = requests.post(f"{url}/channels/create/v2", json = {
        "token": token1, 
        "name": "Channel1", 
        "is_public": True
    })

    payload = channels_response.json()
    
    channel_id = payload["channel_id"]   
    invite_response = requests.post(f"{url}/channel/invite/v2", json = {
            "token": token1,
            "channel_id": channel_id,
            "u_id": invalid_u_id
    })

    # Test invalid u_id by checking if 400 status code is raised
    assert invite_response.status_code == 400



def test_channel_invite_except_noaccess():
    """
    This function tests if the auth_user_id
    is a member of the channel.
    """
     # Clear the data
    requests.delete(f"{url}/clear/v1")

    # Users information to be pass in as json
    user1_data = {
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first": "john",
        "name_last": "smith",
    }
    
    user2_data = {
        "email": "michaelbush@gmail.com",
        "password": "123456",
        "name_first": "michael",
        "name_last": "bush",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    
    auth_id2 = payload["auth_user_id"]
    token2 = payload["token"]

    channels_response = requests.post(f"{url}/channels/create/v2", json = {
        "token": token1, 
        "name": "Channel1", 
        "is_public": True
    })

    payload = channels_response.json()
    
    channel_id = payload["channel_id"]   
    invite_response = requests.post(f"{url}/channel/invite/v2", json = {
            "token": token2,
            "channel_id": channel_id,
            "u_id": auth_id2
    })

    # Check if auth_user_id not a member of channel.
    # If not a member raises status code 403 AccessError 
    assert invite_response.status_code == 403

def test_channel_invite_except_invalid_auth():
    """
    This function tests if the token is valid.
    """
    # Clear the data
    requests.delete(f"{url}/clear/v1")

    # Users information to be pass in as json
    user1_data = {
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first": "john",
        "name_last": "smith",
    }
    
    user2_data = {
        "email": "michaelbush@gmail.com",
        "password": "123456",
        "name_first": "michael",
        "name_last": "bush",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    
    auth_id2 = payload["auth_user_id"]
   

    # Generate invlid user token
    invalid_user = 222
    invalid_token = generate_token(invalid_user)

    channels_response = requests.post(f"{url}/channels/create/v2", json = {
        "token": token1, 
        "name": "Channel1", 
        "is_public": True
    })

    payload = channels_response.json()
    
    channel_id = payload["channel_id"]   
    invite_response = requests.post(f"{url}/channel/invite/v2", json = {
            "token": invalid_token,
            "channel_id": channel_id,
            "u_id": auth_id2
    })

    # Check if the user token is valid
    # If not valid raise status code 403 AccessError 
    assert invite_response.status_code == 403

def test_channel_invite_except_repetitive():
    """
    This functions tests if the auth_user_id is 
    inviting a user already in the channel.
    """

    # Clear the data
    requests.delete(f"{url}/clear/v1")

    # Users information to be pass in as json
    user1_data = {
        "email": "johnsmith@gmail.com",
        "password": "password123",
        "name_first": "john",
        "name_last": "smith",
    }
    
    user2_data = {
        "email": "michaelbush@gmail.com",
        "password": "123456",
        "name_first": "michael",
        "name_last": "bush",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]
    auth_id1 = payload["auth_user_id"]

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()

    channels_response = requests.post(f"{url}/channels/create/v2", json = {
        "token": token1, 
        "name": "Channel1", 
        "is_public": True
    })

    payload = channels_response.json()
    
    channel_id = payload["channel_id"]   
    invite_response = requests.post(f"{url}/channel/invite/v2", json = {
            "token": token1,
            "channel_id": channel_id,
            "u_id": auth_id1
    })

    # Check for repetitive invite. If u_id already in channel,
    # raises status code 403 AccessError 
    assert invite_response.status_code == 403
