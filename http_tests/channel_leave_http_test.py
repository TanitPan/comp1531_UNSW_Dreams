'''
This file contains HTTP server tests for channel_leave in src.channel, testing
an user can successfully leave a channel with the correct errors raised
'''

from src.config import url
from src.helper import generate_token
import json
import pytest
import requests

# Test that a member of the channel can vvalidly leave it even if they are the
# last member/owner
def test_channel_leave_valid():
    # Clears any persistent data and register an user
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "j.smith@gmail.com",
        "password": "pass1234",
        "name_first": "john",
        "name_last": "smith",
    })
    payload = authorised_info.json()
    authorised_token = payload['token']
   
    # Creates a new channel using this user's token 
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token, 
        'name': 'Channel_1', 
        'is_public': False,
    })
    payload = channel.json()
    channel_id = payload["channel_id"]
    
    # Make sure that the user can leave the channel successfully
    request = requests.post(f"{url}/channel/leave/v1", json = {
        'token': authorised_token, 
        'channel_id': channel_id, 
    })
    assert request.status_code == 200 # Should return an success code (200)
    
    # Ensure that the channel list returns an empty dictionary as the user has
    # left
    request = requests.get(f"{url}/channels/list/v2", params = {
        'token': authorised_token,
    })
    payload = request.json() 
    assert payload['channels'] == [{}]
    
# Test that an invalid channel ID argument will raise an InputError
def test_channel_leave_invalid_channelid():
    # Clear data and register an user
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "j.smith@outlook.com",
        "password": "pass1234",
        "name_first": "jane",
        "name_last": "smithers",
    })
    payload = authorised_info.json()
    token = payload["token"]
     
    # Create an invalid channel id of a negative number as ids are positive. 
    invalid_channel_id = -1 
    request = requests.post(f"{url}/channel/leave/v1", json = {
        'token': token, 
        'channel_id': invalid_channel_id,
    })
    # This should return an InputError (400 status code)
    assert request.status_code == 400

# Test that confirms the token belongs to a member or else raise an AccessError
def test_channel_leave_notamember():
    # Clear data and register an user member
    requests.delete(f"{url}/clear/v1") 
    authorised_info1 = requests.post(f"{url}/auth/register/v2", json = {
        "email": "jada.smith@gmail.com",
        "password": "123456",
        "name_first": "jada",
        "name_last": "smith",
    })
    payload = authorised_info1.json()
    token1 = payload["token"]

    # Create a new channel, making this current user an owner  
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token1, 
        'name': 'Channel_2', 
        'is_public': False,
    })
    payload = channel.json()
    channel_id = payload["channel_id"]
    
    # Create a new user but do not add them to the channel
    authorised_info2 = requests.post(f"{url}/auth/register/v2", json = {
        "email": "w.smith@gmail.com",
        "password": "smithwillow",
        "name_first": "willow",
        "name_last": "smith",
    })
    payload = authorised_info2.json()
    token2 = payload["token"]
    
    # Using this new user's token, an attempt to leave the channel should raise
    # a 403 status code
    request = requests.post(f"{url}/channel/leave/v1", json = {
        'token': token2, 
        'channel_id': channel_id,
    })
    assert request.status_code == 403

# Test that an argument with an invalid token will raise an AccessError
def test_channel_leave_invalid_token():   
    # Register an user after clearing data     
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "w.smith@gmail.com",
        "password": "william",
        "name_first": "will",
        "name_last": "smith",
    })
    payload = authorised_info.json()
    token = payload["token"]
    # Create an invalid user_id add by adding one to the existing user
    invalid_user_id = payload["auth_user_id"] + 1
    
    # Create an channel with the user's token and obtain their channel_id
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Channel_3', 
        'is_public': False,
    })
    payload = channel.json()
    channel_id = payload["channel_id"]

    # Pass the invalid user id into the generate_token helper function 
    token2 = generate_token(invalid_user_id)  
    
    # Trying to pass this token as an argument should raise a 403 AccessError
    request = requests.post(f"{url}/channel/leave/v1", json = {
        'token': token2, 
        'channel_id': channel_id,
    })
    assert request.status_code == 403
