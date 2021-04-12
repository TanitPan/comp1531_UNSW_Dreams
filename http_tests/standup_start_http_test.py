'''This file consists of HTTP server tests for standup_start_v1 in standup.py'''

from src.config import url
from src.helper import generate_token
from src.standup import standups
import json
import pytest
import requests

@pytest.fixture
# Register a user, extracting its token
def register_authorised_user():
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "j.doe@yahoo.com",
        "password": "password123",
        "name_first": "jane",
        "name_last": "doe",
    })
    payload = authorised_info.json()
    return payload["token"]

@pytest.fixture
# Creates a channel, extracting its ID
def create_channel(register_authorised_user):
    token = register_authorised_user
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'channel_1', 
        'is_public': False
    })
    payload = channel.json()
    return payload["channel_id"]

# Test for a successful use of standup_start, using valid token and channel_id
def test_standup_start_success(register_authorised_user):
    requests.delete(f"{url}/clear/v1") 
    standups.clear() 
    token = register_authorised_user
    channel_id = create_channel

    # Using the channel id and token, test the status code of the request will
    # return a success (200) 
    request = requests.post(f"{url}/standup/start/v1", json = {
        "token": token,
        "channel_id": channel_id,
        "length": 1,
    })
    print(request)
    assert request.status_code == 200 
    payload = request.json()
    time_finish = payload["time_finish"]
    # Confirm the return value is an integer
    assert isinstance(payload, int)

# Test checking that an error is raised when an invalid channel_id is passed in
def test_standup_start_invalidchannel(register_authorised_user, create_channel):
    requests.delete(f"{url}/clear/v1") 
    standups.clear()
    token = register_authorised_user
    # Creates an invalid_channel_id by adding one to the fixture
    invalid_channel_id = int(create_channel()) + 1
    # Pass this invalid id into the standup/start POST request
    request = requests.post(f"{url}/standup/start/v1", json = {
        "token": token,
        "channel_id": invalid_channel_id,
        "length": 1,
    })
    # Confirm an input error is raised (400 error code)
    assert request.status_code == 400 

# Test that a 400 error is raised when an already active standup is asked to 
# start
def test_standup_start_alreadyactive(register_authorised_user, create_channel):
    requests.delete(f"{url}/clear/v1") 
    standups.clear()
    token = register_authorised_user
    channel_id = create_channel
    # Begin a standup and while it is running, begin a new standup 
    requests.post(f"{url}/standup/start/v1", json = {
        "token": token,
        "channel_id": channel_id,
        "length": 100,
    })
    request = requests.post(f"{url}/standup/start/v1", json = {
        "token": token,
        "channel_id": channel_id,
        "length": 1,
    })
    # Confirm a 400 error code is created
    assert request.status_code == 400 

# Test that an invalid token cannot begin a standup
def test_standup_start_invalidtoken(create_channel):
    # Clear data
    requests.delete(f"{url}/clear/v1") 
    standups.clear() 
    # Using a random user_id, generate a token
    token = generate_token(100)
    channel_id = create_channel
    # Pass this token in and confirm an 403 AccessError is raised
    request = requests.post(f"{url}/standup/start/v1", json = {
        "token": token,
        "channel_id": channel_id,
        "length": 1,
    })
    assert request.status_code == 403 

# Test confirming an user who is not a channel member will cause an AccessError
# to be raised
def test_standup_start_unauthorised_user(register_authorised_user, create_channel):
    requests.delete(f"{url}/clear/v1") 
    standups.clear()
    # Clear data, register a user and create a channel 
    register_authorised_user
    channel_id = create_channel
    # Register a second user and extract their token
    authorised_info2 = requests.post(f"{url}/auth/register/v2", json = {
        "email": "hayden.smith@gmail.com",
        "password": "pass1234",
        "name_first": "hayden",
        "name_last": "smith",
    })
    payload = authorised_info2.json()
    token2 = payload["token"]
    # Pass this token in and confirm an 403 AccessError is raised
    request = requests.post(f"{url}/standup/start/v1", json = {
        "token": token2,
        "channel_id": channel_id,
        "length": 1,
    })
    assert request.status_code == 403
