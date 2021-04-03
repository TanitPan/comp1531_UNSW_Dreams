"""
This file contain the test for channel_invite_v2 HTTP implementation 
"""
from src.config import url
import src.channel as channel
import src.channels as channels
import src.auth as auth
import pytest
import json
import requests

def test_channel_invite_valid():
    # Clear the data
    requests.delete(f"{url}/clear/v1")

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
    auth_user1_info = requests.post(f"{url}/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]

    auth_user2_info = requests.post(f"{url}/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    print(payload)
    auth_id2 = payload["auth_user_id"]
    token2 = payload["token"]

    channels_response = requests.post(f"{url}/channels/create/v2", json = {
        "token": token1, 
        "name": "Channel1", 
        "is_public": True
    })

    payload = channels_response.json()
    print(payload)
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

    # if __name__ == '__main__':
    #     test_channel_invite_valid()

