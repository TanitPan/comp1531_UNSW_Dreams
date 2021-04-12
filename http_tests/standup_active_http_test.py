'''This file consists of HTTP server tests for standup_active_v1 in standup.py'''

from src.config import url
from src.helper import generate_token
from src.standup import standups
import json
import pytest
import requests

@pytest.fixture
# Clear all data and register a user, extracting its token
def register_authorised_user():
    requests.delete(f"{url}/clear/v1") 
    standups.clear() 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "hayden.smith@icloud.com",
        "password": "comp1531",
        "name_first": "hayden",
        "name_last": "smith",
    })
    payload = authorised_info.json()
    token = payload["token"]

@pytest.fixture
# Creates a channel, extracting its ID
def create_channel(register_authorised_user):
    token = register_authorised_user()
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Comp1531_channel', 
        'is_public': True
    })
    payload = channel.json()
    channel_id = payload["channel_id"]

# Test confirming that standup_active returns False and None respectively when  
# there is no active standup returns 
def test_standup_active_inactivestandup(register_authorised_user, create_channel):
    token = register_authorised_user()
    channel_id = create_channel()
    
    # Test the status code of the request will be successful 
    request = requests.get(f"{url}/standup/active/v1", params = {
        "token": token,
        "channel_id": channel_id,
    })
    assert request.status_code == 200 
    
    # Extract the is_active and time_finish values, checking them against the 
    # expected values of False and None respectively
    payload = request.json()
    is_active = payload["is_active"]
    assert is_active == False
    finish_time = payload["finish_time"]
    assert finish_time == None
    
# Test confirming that standup_active returns True and the UTC timezone when  
# an active standup is called 
def test_standup_active_activestandup(register_authorised_user, create_channel):
    token = register_authorised_user()
    channel_id = create_channel()
    # Start a standup for 100 secondds
    requests.post(f"{url}/standup/start/v1", json = {
        "token": token,
        "channel_id": invalid_channel_id,
        "length": 100,
    })
    
    # Test the status code of the request to check if the standup is active and 
    # the call is successful 
    request = requests.get(f"{url}/standup/active/v1", params = {
        "token": token,
        "channel_id": channel_id,
    })
    assert request.status_code == 200 
    
    # Extract the is_active and time_finish values, checking them against the 
    # expected values of True and the expected integer return 
    payload = request.json()
    is_active = payload["is_active"]
    assert is_active == True 
    finish_time = payload["finish_time"]
    assert isinstance(finish_time, int)    

# Test checking that an invalid channel id will raise an InputError
def test_standup_active_invalidchannel(register_authorised_user, create_channel):
    token = register_authorised_user()
    # Increment the fixture to generate an invalid_channel_id, passing it as
    # a parameter to the standup_active call 
    invalid_channel_id = int(create_channel()) + 1
    # Pass this invalid id into the standup/start POST request
    request = requests.get(f"{url}/standup/active/v1", params = {
        "token": token,
        "channel_id": invalid_channel_id,
    })
    # Confirm an input error is raised (400 error code)
    assert request.status_code == 400 

# Test that an invalid token being passed in as a parameter will cause an 
# AccessError
def test_standup_active_alreadyactive(create_channel):
    requests.delete(f"{url}/clear/v1") 
    standups.clear() 
    # Using a random user_id, generate a token
    token = generate_token(100)
    channel_id = create_channel() # Use the fixture to obtain a channel id
    
    # Pass the generated token into the GET request and ensure it returns a 
    # 403 Forbidden request
    request = requests.get(f"{url}/standup/active/v1", params = {
        "token": token,
        "channel_id": channel_id,
    })
    assert request.status_code == 403
