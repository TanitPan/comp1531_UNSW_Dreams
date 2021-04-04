'''This file consists of HTTP server tests for search_v2 in other.py'''

from src.config import url
from src.helper import generate_token
import json
import pytest
import requests

# Test for an empty search function when no messages have been sent 
def test_search_empty_messages():
    # Clear and register a user
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "a.andrews@gmail.com",
        "password": "password123",
        "name_first": "anne",
        "name_last": "andrews",
    })
    payload = authorised_info.json()
    token = payload["token"]
    
    # Create a channel and obtain the channel ID
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'channel1', 
        'is_public': True
    })
    payload = request.json()
    channel_id = payload["channel_id"]   
    # Confirm calling the status code will return a 200 status code 
    request = requests.get(f"{url}/search/v2", 
        params= {"token": token, "query_str": "Good morning"})
    assert request.status_code == 200 
    payload = request.json()
    # Confirm type of empty list
    messages = payload["messages"]
    assert (messages == [])

# Test that confirms a 400 error message is raised when the query string is over
# 1000 characters    
def test_search_overlimit_querystr():
    # Clear and register user
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "a.andrews@gmail.com",
        "password": "password123",
        "name_first": "anne",
        "name_last": "andrews",
    })
    payload = authorised_info.json()
    token = payload["token"]
    # Create a very large query string and attempt to use it as a parameter
    query_str = "12345" * 201
    request = requests.get(f"{url}/search/v2", 
        params= {"token": token, "query_str": query_str})
    # An error status code should be raised
    assert request.status_code == 400   

# Test that an invalid token will raise a 403 error code                                            
def test_search_invalidtoken():
    # Clear data and register an user 
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "a.andrews@gmail.com",
        "password": "password123",
        "name_first": "anne",
        "name_last": "andrews",
    })
    payload = authorised_info.json()
    
    # Create an invalid user_id add by adding one to the existing user, 
    # generating a token 
    invalid_user_id = payload["auth_user_id"] + 1
    token2 = generate_token(invalid_user_id)  
    # Call the search feature and make sure an access error is raised for the 
    # invalid user
    request = requests.get(f"{url}/search/v2", 
        params= {"token": token2, "query_str": "COMP1531"})
    assert request.status_code == 403   
    
