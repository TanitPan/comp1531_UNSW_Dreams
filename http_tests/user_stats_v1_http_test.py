'''
This file contains the tests for the HTTP server of the functions user_stats
'''
import pytest
import requests
import json
from src.config import url
import urllib

from src.user import user_stats_v1
from src.error import AccessError
from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_leave_v1
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.message import message_send_v2
from src.other import clear_v1
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

def test_valid_input(register_user):
    global url
    user = register_user
    token = user['token']
    query = urllib.parse.urlencode({
        'token': token
    })
    res = requests.get(f"{url}/user/stats/v1?{query}")
    assert res.status_code == 200 

def test_invalid_token():
    requests.delete(f"{url}/clear/v1") # Clear the data
    token = generate_token(42)
    query = urllib.parse.urlencode({
        'token': token
    })
    res = requests.get(f"{url}/user/stats/v1?{query}")
    payload = res.json() 
    assert payload['code'] == 403 # AccessError