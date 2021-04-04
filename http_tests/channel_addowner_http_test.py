'''
This file contains HTTP server tests for channel_addowner in src.channel, 
testing new owners are correctly added, and the correct input/access errors
'''

from src.config import url
from src.helper import generate_token
import json
import pytest
import requests

@pytest.fixture
def registered_user():
    # Registers an user
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "j.smith@gmail.com",
        "password": "pass1234",
        "name_first": "john",
        "name_last": "smith",
    })
    payload = authorised_info.json()
    return payload
    
# Test to ensure that a valid input passes through the various tests
def test_channels_create_multiple():
    # Clears data and register an user
    requests.delete(f"{url}/clear/v1") 
    payload = registered_user()
    token = payload["token"]
    # Using this user's details, create a channel and obtian the channel id
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Channel_1', 
        'is_public': True
    })
    payload = request.json()
    channel_id = payload["channel_id"]
    # Register a second user
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "jane.doe@gmail.com",
        "password": "jane1234",
        "name_first": "jane",
        "name_last": "doe",
    })
    payload = authorised_info.json()
    auth_user_id = payload["auth_user_id"]
    new_token = payload["token"]
    # Using this user's user_id and the first user's token, add the second user
    # as an  ownerr 
    request = requests.post(f"{url}/channel/addowner/v1", json = {
        'token': token, 
        'channel_id': channel_id, 
        'u_id': auth_user_id,
    })
    # Confirm the status code returns a success
    assert request.status_code == 200 
    
    # Pass in the second user's token and confirm channels_list is working 
    request = requests.get(f"{url}/channels/list/v2", 
        params= {'token': new_token})
    assert request.status_code == 200     
    # Confirm the channels list contains the correct channel id and name of the
    # channel the user has been added to 
    payload = request.json() 
    assert payload['channels'] == [{'channel_id': 1, 'name': 'channel_1'}]

# Test to confirm that an invalid channel returns an InputError
def test_channel_addowner_invalid_channel():   
    # Clears data and returns the information of the fixture's registered user
    requests.delete(f"{url}/clear/v1") 
    payload = registered_user()
    token = payload["token"]
    auth_user_id = payload["auth_user_id"]
    # Attempt to add them to a non-existing channel 
    request = requests.post(f"{url}/channel/addowner/v1", json = {
        'token': token, 
        'channel_id': -1 #channel ids are all positive
        'u_id': auth_user_id,
    })
    # Confirm an input error has been raised
    assert request.status_code == 400 

# Test to confirm an existing owner cannot be added again as an owner
def test_channel_addowner_already_owner():   
    # Clear data and register an user
    requests.delete(f"{url}/clear/v1") 
    payload = registered_user()
    token = payload["token"]
    auth_user_id = payload["auth_user_id"]
    
    # Create a channel using the user's token and extract its channel_id. 
    # Note the registered_user is, by default, already an owner
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Channel_2', 
        'is_public': False
    })
    payload = channel.json()
    channel_id = payload["channel_id"]
    # Attempt to add the registered user as an channel should generate an
    # Bad request
    request = requests.post(f"{url}/channel/addowner/v1", json = {
        'token': token, 
        'channel_id': channel_id
        'u_id': auth_user_id,
    })
    assert request.status_code == 400 

# Test to ensure an user who is neither a dreams owner or channel owner can 
# add a user as an owner
def test_channel_addowner_unauthorised_user():
    # Clear data and register an user, who is the dreams owner
    requests.delete(f"{url}/clear/v1") 
    payload = registered_user()
    token = payload["token"]
    # Create a channel from the token of first user (who is the channel's owner)
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Channel_3', 
        'is_public': True
    })
    payload = channel.json()
    channel_id = payload["channel_id"]
    
    # Create a second user and obtain their user id and token
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "jane.doe@gmail.com",
        "password": "jane1234",
        "name_first": "jane",
        "name_last": "doe",
    })
    payload = authorised_info.json()
    auth_user_id = payload["auth_user_id"]
    new_token = payload["token"]
    # Attempt to add the second user to the channel using their own token and
    # user id should generate in a Forbidden code 
    request = requests.post(f"{url}/channel/addowner/v1", json = {
        'token': new_token, 
        'channel_id': channel_id
        'u_id': auth_user_id,
    })
    assert request.status_code == 403 

# Test to confirm if an invalid_token is inputted, an Error will be created
def test_channel_addowner_invalid_token():
    # Clear data and register an user
    requests.delete(f"{url}/clear/v1") 
    payload = registered_user()
    # Using their valid token, create a channel with a channel_id
    token1 = payload["token"]
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token1, 
        'name': 'Channel_4', 
        'is_public': False
    })
    payload = channel.json()
    channel_id = payload["channel_id"]

    # Register a new user 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "jane.doe@gmail.com",
        "password": "jane1234",
        "name_first": "jane",
        "name_last": "doe",
    })
    payload = authorised_info.json()
    # Obtain their valid user id and increment it by one to create an invalid id
    auth_user_id = payload['auth_user_id']
    unauthorised_user_id = auth_user_id + 1
    # Generate an unauthorised token using this invalid user id 
    unauthorised_token = generate_token(unauthorised_user_id)
    # Attempt to add an owner should again create an Access Error (code 403)
    request = requests.post(f"{url}/channel/addowner/v1", json = {
        'token': unauthorised_token, 
        'channel_id': channel_id
        'u_id': auth_user_id,
    })
    assert request.status_code == 403 
  

