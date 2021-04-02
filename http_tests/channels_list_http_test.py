'''
This file contains HTTP server tests for the functions of channels_listall in 
src.channels, testing that the correct output is received for multiple channels 
created by the same user and different, and that the AccessError works
'''
import src.auth as auth
import src.channels as channels
from src.config import url
from src.helper import generate_token

import json
import pytest
import requests

# Test that an authorised user can add multiple channels to the list
def test_channels_list_multiple_channels():
    # Collate the data (email, password, name) to pass into auth_register_v
    requests.delete(f"{url}/clear/v1") 
    auth_data = {
        'email': 'comp1531@hotmail.com', 
        'password': 'hogwarts', 
        'name_first': 'harry', 
        'name_last': 'potter',
    }
    authorised_info = requests.post(f"{url}/auth/register/v2", json = auth_data)
    
    # Extracts the token provided by the registration to create new channels
    payload = authorised_info.json()
    authorised_token = payload['token']
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token, 
        'name': 'channel_1', 
        'is_public': False,
    })     
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token, 
        'name': 'channel_2', 
        'is_public': True,
    })    
   
    # Pass in the token as a parameter and insert the urll for channels_list
    request = requests.get(f"{url}/channels/list/v2", 
        params= {'token': authorised_token})
    # Check that the HTML request has succeeded through a 200 status code   
    assert request.status_code == 200 
    
    # Confirm the channels list contains the correct channel id and names
    payload = request.json() 
    assert payload['channels'] == [{'channel_id': 1, 'name': 'channel_1'},
                                  {'channel_id': 2, 'name': 'channel_2'}]

# Test to ensure that only the channels added by the user that created the 
# token are listed
def test_channels_list_verifying_user():
    # Clear data
    requests.delete(f"{url}/clear/v1") 
    # Register the first user
    auth_data = {
        'email': 'autumn2021@hotmail.com', 
        'password': 'winter06', 
        'name_first': 'autumn', 
        'name_last': 'winters',
    }
    authorised_info1 = requests.post(f"{url}/auth/register/v2", json = auth_data)    
    payload = authorised_info1.json()
    # Use this first user's token to create a channel
    authorised_token1 = payload['token']
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token1, 
        'name': 'channel/3', 
        'is_public': False,
    })     
    
    # Create a second user registration and pass in the necessary data
    auth_data = {
        'email': 'summer2021@hotmail.com', 
        'password': 'spring09', 
        'name_first': 'summer', 
        'name_last': 'springs',
    }
    authorised_info2 = requests.post(f"{url}/auth/register/v2", json = auth_data)    
    payload = authorised_info2.json()
    # Use the token generated from the registration to create a new channel 
    authorised_token2 = payload['token']
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token2, 
        'name': 'channel/4', 
        'is_public': True,
    })    
    # Using the second user's account, request channels_list and verify that
    # only one channel has been listed with the correct channel_id and name
    request = requests.get(f"{url}/channels/list/v2", params = {
        'token': authorised_token2,
    })
    assert request.status_code == 200  # Confirm the request is successful
    payload = request.json() 
    assert payload['channels'] == [{'channel_id': 2, 'name': 'channel/4'}]
    
# Test to confirm that an Access Error is produced when an user who has not yet
# been registered requests channel_list                                     
def test_channels_list_invalid_user():
    # Clear data
    requests.delete(f"{url}/clear/v1") 
    # Register an user, extracting their user id
    auth_data = {
        'email': 'alastname@hotmail.com', 
        'password': 'snowy2021', 
        'name_first': 'anna', 
        'name_last': 'lastname',
    }
    authorised_info = requests.post(f"{url}/auth/register/v2", json = auth_data)    
    payload = authorised_info.json()
    
    # Create an unauthorised token by incrementing the previous user id and 
    # passing it into generate_token
    unauthorised_user_id = payload['auth_user_id'] + 1
    unauthorised_token = generate_token(unauthorised_user_id)
    # Pass this generated token into channels_list and verify an AccessError
    # has been aised
    request = requests.get(f"{url}/channels/list/v2", params = {
        'token': unauthorised_token
    })
    assert request.status_code == 403                         
    
                    
