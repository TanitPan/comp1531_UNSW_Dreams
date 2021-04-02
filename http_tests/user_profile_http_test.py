'''
This file contains the tests for the HTTP server of user/profile route
'''

import pytest
import requests
import json
from src.config import url

import urllib # for query string generation

def test_valid_input():
    global url
    requests.delete(f"{url}/clear/v1") # clear the data first
    user = requests.post(f"{url}/auth/register/v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "john",
        "name_last": "smith",
    })
    payload = user.json()
    id = payload['auth_user_id']
    token = payload['token']
    # Generate a query string for get request
    query = urllib.parse.urlencode({
        'token': token,
        'u_id': id
    })

    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload == {
        'user': {
            'auth_user_id': id,
            'name_first' : 'john', 
	        'name_last' : 'smith', 
            'handle_str' : 'johnsmith', 
	        'email': 'johnsmith@gmail.com', 
	        'password': '123456', 
            'permission_id': 1, #1 for owner, 2 for member 
        }
    }

def test_invalid_uid():
    global url
    requests.delete(f"{url}/clear/v1") # clear the data first
    user = requests.post(f"{url}/auth/register/v2", json={
        "email": "johnsmith@gmail.com", # valid email
        "password": "123456",
        "name_first": "john",
        "name_last": "smith",
    })
    payload = user.json()
    id = -5 # Invalid user id since auth_user_id >= 0 
    token = payload['token']
    # Generate a query string for get request
    query = urllib.parse.urlencode({
        'token': token,
        'u_id': id
    })
    res = requests.get(f"{url}/user/profile/v2?{query}")
    payload = res.json()
    assert payload['code'] == 400 # InputError
    
