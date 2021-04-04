"""
This file contain the test for channel_join_v2 HTTP implementation 
"""
from src.config import url
from src.helper import generate_token
import src.channel as channel
import src.channels as channels
import src.auth as auth
import pytest
import json
import requests

def test_channel_join_valid():
    """
    This function checks if the user is successfully
    added to the channel and store in the data structure.
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
    
    token2 = payload["token"]

    channels_response = requests.post(f"{url}/channels/create/v2", json = {
        "token": token1, 
        "name": "Channel1", 
        "is_public": True
    })

    payload = channels_response.json()
    
    channel_id = payload["channel_id"]
    join_response = requests.post(f"{url}/channel/join/v2", json = {
            "token": token2,
            "channel_id": channel_id
    })

    # Check if the HTML request is successful
    assert join_response.status_code == 200

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

def test_channel_join_except_channel():
    """
    This function tests if channel ID is
    a valid channel.
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
    
    token2 = payload["token"]
    invalid_channel = 55
    
    requests.post(f"{url}/channels/create/v2", json = {
        "token": token1, 
        "name": "Channel1", 
        "is_public": True
    })

    join_response = requests.post(f"{url}/channel/join/v2", json = {
        "token": token2,
        "channel_id": invalid_channel
    })

    # Test invalid channel by checking if 400 status code is raised
    assert join_response.status_code == 400

def test_channel_join_except_invalid_auth():
    """
    This function tests if token is valid
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

    requests.post(f"{url}/auth/register/v2", json = user2_data)
    
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
    join_response = requests.post(f"{url}/channel/join/v2", json = {
            "token": invalid_token,
            "channel_id": channel_id
    })

    # Check if the user token is valid
    # If not valid raise status code 403 AccessError 
    assert join_response.status_code == 403

def test_channel_join_except_private():
    """
    This function tests if the channel status
    is private and user is not global owner.
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
    

    token2 = payload["token"]

    channels_response = requests.post(f"{url}/channels/create/v2", json = {
        "token": token1, 
        "name": "Channel1", 
        "is_public": False
    })

    payload = channels_response.json()
    
    channel_id = payload["channel_id"]
    join_response = requests.post(f"{url}/channel/join/v2", json = {
            "token": token2,
            "channel_id": channel_id
    })

    # Raise 403 code if the user join a private channel without
    # being a global owner
    assert join_response.status_code == 403

def test_channel_join_private_global():
    """
    This function tests if the channel status
    is private and user is global DREAM owner.
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
    
    token2 = payload["token"]

    channels_response = requests.post(f"{url}/channels/create/v2", json = {
        "token": token2, 
        "name": "Channel1", 
        "is_public": False
    })

    payload = channels_response.json()
    
    channel_id = payload["channel_id"]
    join_response = requests.post(f"{url}/channel/join/v2", json = {
            "token": token1,
            "channel_id": channel_id
    })

    # Check if HTTP request is successful
    assert join_response.status_code == 200
    res = requests.get(f"{url}/channels/list/v2", params= {'token': token1})
    payload = res.json()
    
    assert payload == {
        'channels': [
        	{
        		'channel_id': 1, # channel id start at 1 or 0 is worth checking ?
        		'name': 'Channel1',
        	}
        ] 
    }

def test_channel_join_except_repetitive():
    """
    This function tests if the user is already
    a member in that channel.
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

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    token2 = payload["token"]

    channels_response = requests.post(f"{url}/channels/create/v2", json = {
        "token": token2, 
        "name": "Channel1", 
        "is_public": True
    })

    payload = channels_response.json()
    
    channel_id = payload["channel_id"]   
    join_response = requests.post(f"{url}/channel/join/v2", json = {
            "token": token2,
            "channel_id": channel_id,
    })

    # Check for repetitive join. If user already in channel,
    # raises status code 403 AccessError 
    assert join_response.status_code == 403


