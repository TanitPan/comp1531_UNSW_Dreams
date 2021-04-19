'''
This file contains the tests for the HTTP server of /user/profile/uploadphoto route
'''

import pytest
import requests
import json
from src.config import url

CUTE_CAT_URL = "https://thumbs.dreamstime.com/b/scottish-fold-cat-14577759.jpg"

@pytest.fixture
def register_user():
    global url
    requests.delete(f"{url}/clear/v1") # Clear the data
    user = requests.post(f"{url}/auth/register/v2", json={
        "email": "batman@gmail.com",
        "password": "123456",
        "name_first": "bat",
        "name_last": "man",
    })
    requests.post(f"{url}/auth/register/v2", json={
        "email": "johnsmith@gmail.com",
        "password": "123456",
        "name_first": "john",
        "name_last": "smith",
    })
    payload = user.json()
    return payload

def test_valid_input(register_user):
    global url

    user = register_user
    token = user['token']
    res = requests.post(f"{url}/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": CUTE_CAT_URL,
        "x_start": 0,
        "y_start": 0,
        "x_end": 200,
        "y_end": 200,
    })
    payload = res.json()
    assert payload == {}

def test_negative_dimensions(register_user):
    global url
    user = register_user
    token = user['token']

    res = requests.post(f"{url}/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": CUTE_CAT_URL,
        "x_start": -1,
        "y_start": 0,
        "x_end": 200,
        "y_end": 200,
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_switched_dimensions(register_user):
    global url
    user = register_user
    token = user['token']

    res = requests.post(f"{url}/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": CUTE_CAT_URL,
        "x_start": 50,
        "y_start": 50,
        "x_end": 0,
        "y_end": 0,
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

def test_large_dimensions(register_user):
    global url
    user = register_user
    token = user['token']

    res = requests.post(f"{url}/user/profile/uploadphoto/v1", json={
        "token": token,
        "img_url": CUTE_CAT_URL,
        "x_start": 0,
        "y_start": 0,
        "x_end": 100000,
        "y_end": 100000,
    })
    payload = res.json()
    assert payload['code'] == 400 # InputError

