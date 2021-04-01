'''
This file contains the tests for the HTTP server of the functions channels_create
'''
import src.auth as auth
import src.channels as channels
from src.config import url
import json
import pytest
import requests

def test_one_valid_input():
    global url
    print(url)
    requests.delete(f"{url}/clear/v1") 
    auth_register_data = {
        'email': 'john.smith@gmail.com', 
        'password': 'pass1234', 
        'name_first': 'john', 
        'name_last': 'smith'
    }
    authorised_info = requests.post(f"{url}/auth/register/v2", 
        json = auth_register_data)
    #print(authorised_info)
    payload = authorised_info.json()
    authorised_token = payload['token']
    #print(authorised_token)

    channels_create_data = {
        'token': authorised_token, 
        'name': 'Channel0', 
        'is_public': True,
    }
    print(channels_create_data)
    res = requests.post(f"{url}/channels/create/v2", json = channels_create_data)
    print(res)

    #channels_create_data)
    payload = res.json()
    #print(payload)
    assert payload['name'] == 'Channel0'


