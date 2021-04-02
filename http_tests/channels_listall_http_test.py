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

# Test that multiple channels are successfully displayed if they are by the same
# user
def test_channels_listall_multiplechannel():
    # Clears data and collates the necessary information for auth_register/v2 
    requests.delete(f"{url}/clear/v1") 
    auth_data = {
        'email': 'z1111111@gmail.com', 
        'password': 'unswstudent', 
        'name_first': 'anne', 
        'name_last': 'student',
    }
    authorised_info = requests.post(f"{url}/auth/register/v2", json = auth_data)
    
    # Extracts the authorised token from the registration to create two channels
    payload = authorised_info.json()
    authorised_token = payload['token']
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token, 
        'name': 'Channel1', 
        'is_public': True,
    })     
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token, 
        'name': 'Channel_2', 
        'is_public': False,
    })    
    
    # Pass in the token as a parameter for listall
    request = requests.get(f"{url}/channels/listall/v2", 
        params= {'token': authorised_token})
    # Check that the HTML request has succeeded through a 200 status code   
    assert request.status_code == 200 
    
    # Confirm the channels list contains the correct channel id and names
    payload = request.json() 
    assert payload['channels'] == [{'channel_id': 1, 'name': 'Channel1'},
                                  {'channel_id': 2, 'name': 'Channel_2'}]

# Test that the function returns the list of channels for all authorised users 
# that have created a channel
def test_channels_listall_multipleusers():
    # Clear data
    requests.delete(f"{url}/clear/v1") 
    # Collate all the parameters and register the first user
    authorised_info1 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'z1111111@gmail.com', 
        'password': 'unswstudent', 
        'name_first': 'anne', 
        'name_last': 'student',
    })   
    # Obtain the token for the first authorised user
    payload = authorised_info1.json()
    authorised_token1 = payload['token']
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token1, 
        'name': 'Channel-3', 
        'is_public': True
    })     
    
    # Create and register a new user
    authorised_info2 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'z2222222@gmail.com', 
        'password': 'new_student1', 
        'name_first': 'henry', 
        'name_last': 'ford'
    })   
    # Extract the token created by the second user and create a channel
    payload = authorised_info2.json()
    authorised_token2 = payload['token']
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token2, 
        'name': 'Channel-4', 
        'is_public': True
    })  
    
    # Request for the listall function, passing a valid token in as a parameter 
    request = requests.get(f"{url}/channels/listall/v2", 
        params= {'token': authorised_token1})
    # Check that the HTML request has succeeded with a status code of 200   
    assert request.status_code == 200 
    
    # Confirm the request is of the correct format and content
    payload = request.json() 
    assert payload['channels'] == [{'channel_id': 1, 'name': 'Channel-3'},
                                  {'channel_id': 2, 'name': 'Channel-4'}]   

# Test for an invalid user requesting the channels_listall                                  
def test_channels_listall_invalid_user():
    requests.delete(f"{url}/clear/v1") 
    # Collate all the values for each key required in the auth_register/v2
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'wonderland2020@gmail.com', 
        'password': 'madhatter', 
        'name_first': 'alice', 
        'name_last': 'wonderland'
    })   
    # Extract the user_id and an unauthorised id, which is one greater than it. 
    # Generate a token with the unauthorised id, passing this unauthorised_token
    # into the params for the listall function 
    payload = authorised_info.json() 
    authorised_user_id = payload['auth_user_id']
    unauthorised_user_id = authorised_user_id + 1
    unauthorised_token = generate_token(unauthorised_user_id)  
    request = requests.get(f"{url}/channels/listall/v2", 
        params= {'token': unauthorised_token})
    
    # Check if an Access Error was raised through the 403 code                                  
    assert request.status_code == 403                         

    
