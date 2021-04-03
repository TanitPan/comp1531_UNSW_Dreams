"""
This file contains the tests for user/all route
"""

import pytest
import requests
import json
import urllib
from src.config import url

from src.helper import generate_token

@pytest.fixture
def register_user():
    global url
    requests.delete(f"{url}/clear/v1") # Clear the data
    requests.post(f"{url}/auth/register/v2", json={
        "email": "batman@gmail.com",
        "password": "123456",
        "name_first": "bat",
        "name_last": "man",
    })
    user = requests.post(f"{url}/auth/register/v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "john",
        "name_last": "smith",
    })
    payload = user.json()
    return payload

def test_valid_token(register_user):
    global url
    user = register_user
    token = user['token']
    query = urllib.parse.urlencode({
        'token': token
    })
    res = requests.get(f"{url}/users/all/v1?{query}")
    payload = res.json()
    assert payload == {
        'users': [
            {
                "auth_user_id": 0,
                "name_first": "bat",
                "name_last": "man",
                "handle_str": "batman",
                "email": "batman@gmail.com",
                "password": "123456",
                "permission_id": 1                              
            },
            {
                "auth_user_id": 1,
                "name_first": "john",
                "name_last": "smith",
                "handle_str": "johnsmith",
                "email": "johnsmith@gmail.com",
                "password": "123456",
                "permission_id": 2               
            }
        ]
    }

def test_invalid_token(register_user):
    global url
    # generate an invalid token
    token = generate_token(100)
    query = urllib.parse.urlencode({
        'token': token
    })
    res = requests.get(f"{url}/users/all/v1?{query}")
    payload = res.json()
    assert payload['code'] == 403 # AccessError
    