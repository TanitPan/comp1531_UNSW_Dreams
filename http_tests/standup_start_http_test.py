'''This file consists of HTTP server tests for standup_start_v1 in standup.py'''

from src.config import url
from src.helper import generate_token
import json
import pytest
import requests

# Test for a successful use of standup_start, using valid token and channel_id
def test_standup_start_success():
    requests.delete(f"{url}/clear/v1")
    # Register a user, extracting its token
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "j.doe@yahoo.com",
        "password": "password123",
        "name_first": "jane",
        "name_last": "doe",
    })
    payload = authorised_info.json()   
    token = payload["token"]
    
    # Creates a channel, extracting its ID
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'channel_1', 
        'is_public': True
    })
    payload = channel.json()
    channel_id = payload["channel_id"]
    
    # Using the channel id and token, test the status code of the request will
    # return a success (200) 
    request = requests.post(f"{url}/standup/start/v1", json = {
        "token": token,
        "channel_id": channel_id,
        "length": 1,
    })
    assert request.status_code == 200 
    payload = request.json()
    time_finish = payload["time_finish"]
    
    # Confirm the return value is an integer
    assert isinstance(time_finish, int)

# Test checking that an error is raised when an invalid channel_id is passed in
def test_standup_start_invalidchannel():
    # Clear data and obtain a token
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "james.bond007@outlook.com",
        "password": "mi9mi9mi9",
        "name_first": "james",
        "name_last": "bond",
    })
    payload = authorised_info.json()   
    token = payload["token"]
    
    # Creates and passes an invalid_channel_id into the standup/start request
    request = requests.post(f"{url}/standup/start/v1", json = {
        "token": token,
        "channel_id": 1000,
        "length": 1,
    })
    # Confirm an input error is raised (400 error code)
    assert request.status_code == 400 

# Test that a 400 error is raised when an already active standup is asked to 
# start
def test_standup_start_alreadyactive():
    # Clear all data, obtain a token and channel id
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "j.bourne@email.com",
        "password": "bournelegacy",
        "name_first": "jason",
        "name_last": "bourne",
    })
    payload = authorised_info.json()   
    token = payload["token"]
    
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'channel_2', 
        'is_public': False
    })
    payload = channel.json()
    channel_id = payload["channel_id"]
    
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
def test_standup_start_invalidtoken():
    # Clear data
    requests.delete(f"{url}/clear/v1") 
    # Authorise an user and generate a channel_id
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "alec.leamas@circus.com",
        "password": "fromthecold",
        "name_first": "alec",
        "name_last": "leamas",
    })
    payload = authorised_info.json()   
    token1 = payload["token"]
    
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token1, 
        'name': 'channel_3', 
        'is_public': True
    })
    payload = channel.json()
    channel_id = payload["channel_id"]

    # Using a random user_id, generate a token
    token2 = generate_token(100)
    # Pass this token in and confirm an 403 AccessError is raised
    request = requests.post(f"{url}/standup/start/v1", json = {
        "token": token2,
        "channel_id": channel_id,
        "length": 1,
    })
    assert request.status_code == 403 

# Test confirming an user who is not a channel member will cause an AccessError
# to be raised
def test_standup_start_unauthorised_user():
    requests.delete(f"{url}/clear/v1") 
    # Clear data, register a user and create a channel 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "h.hart@kingsman.com",
        "password": "galahad",
        "name_first": "harry",
        "name_last": "hart",
    })
    payload = authorised_info.json()   
    token1 = payload["token"]
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token1, 
        'name': 'channel_4', 
        'is_public': True
    })
    payload = channel.json()
    channel_id = payload["channel_id"]
    
    # Register a second user and extract their token
    authorised_info2 = requests.post(f"{url}/auth/register/v2", json = {
        "email": "e.unwin@gmail.com",
        "password": "kingsman",
        "name_first": "eggsy",
        "name_last": "unwin",
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
