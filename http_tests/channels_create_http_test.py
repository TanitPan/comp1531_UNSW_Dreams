'''
This file contains HTTP server tests for the functions of channels_create in 
src.channels, testing for multiple valid channels being created
'''
import src.auth as auth
import src.channels as channels
from src.config import url
from src.helper import generate_token
import json
import pytest
import requests

# Test to ensure multiple channels are validly created and channel ids update
def test_channels_create_multiple():
    # Clears the data  
    requests.delete(f"{url}/clear/v1") 
    # Collate all the values for each key required in the auth_register/v2
    auth_data = {
        'email': 'john.smith@gmail.com', 
        'password': 'pass1234', 
        'name_first': 'john', 
        'name_last': 'smith'
    }
    authorised_info = requests.post(f"{url}/auth/register/v2", json = auth_data)
    
    # Extract the token to use in channels/create/v2
    payload = authorised_info.json()
    authorised_token = payload['token']
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token, 
        'name': 'Channel1', 
        'is_public': True
    })     
    # Test the channel_id to make sure it begins at 1 as per the assumptions
    payload = request.json()
    assert payload['channel_id'] == 1
    
    # Recall the request and verify a new, iterative channel_id has been created
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token, 
        'name': 'Channel2', 
        'is_public': False
    })     
    payload = request.json()
    assert payload['channel_id'] == 2

# Test to check if a status code of 400 (Input Error) is raised for a channel
# name that is over 20 characters
def test_channels_create_invalid_length():
    # Clear data
    requests.delete(f"{url}/clear/v1") 
    # Register the user using auth/register and ensure they are a part of users
    auth_data = {
        'email': 'robfrost@outlook.com', 
        'password': 'robertfrost1', 
        'name_first': 'robert', 
        'name_last': 'frost'
    }
    authorised_info = requests.post(f"{url}/auth/register/v2", json = auth_data)
    
    # Extract the token to use in channels/create/v2 and create a request with
    # a channel name that is greater than 20 characters in length 
    payload = authorised_info.json()
    authorised_token = payload['token']
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token, 
        'name': 'this_is_a_very_long_channel_name', 
        'is_public': True
    }) 
        
    # Test the code to ensure a 400 error code has been raised
    payload = request.json()
    assert payload['code'] == 400

# Test to confirm a 403 status code is given for an authorised token that is 
# passed in [i.e. it is not of a valid user_id]
def test_channels_create_invalid_user():
    # Clear the data before registering a valid user
    requests.delete(f"{url}/clear/v1") 
    auth_data = {
        'email': 'edgar_poe@yahoo.com', 
        'password': 'theraven', 
        'name_first': 'edgar', 
        'name_last': 'poe'
    }
    authorised_info = requests.post(f"{url}/auth/register/v2", json = auth_data)

    # Extract their user_id and create a new user id that is one greater than it
    # Using this unauthorised_user_id, generate an invalid token using the 
    # helper function
    payload = authorised_info.json()
    authorised_user_id = payload['auth_user_id']
    unauthorised_user_id = authorised_user_id + 1
    unauthorised_token = generate_token(unauthorised_user_id)

    # Attempted to create a new channel
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': unauthorised_token, 
        'name': 'Channel2', 
        'is_public': True
    })     
    
    # Test the code to ensure a 403 error code has been raised
    payload = request.json()
    assert payload['code'] == 403



