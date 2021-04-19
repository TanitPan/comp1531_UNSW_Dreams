from src.config import url
from src.helper import generate_token
import src.channel as channel
import src.channels as channels
import src.auth as auth
import src.message as message

import pytest
import json
import requests

def test_message_send():
    # Clear the data
    requests.delete(f"{url}/clear/v1")

    user1 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'johnsmith@gmail.com',
        'password': 'password123',
        'name_first': 'John',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user1.json()['token'], 
        'name': 'Channel1', 
        'is_public': True
    })

    message_id1 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })
    
    res = requests.get(f"{url}/channel/messages/v2", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })
    
    assert res.status_code == 200
    payload = res.json()

    assert payload['messages'][0]['message'] == "Hello"
    assert payload['end'] == -1 
    assert payload['messages'][0]['message_id'] == message_id1.json()['message_id']

def test_message_send_more():
    # Clear the data
    requests.delete(f"{url}/clear/v1")

    user2 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'janesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Jane',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user2.json()['token'], 
        'name': 'COMP1531', 
        'is_public': True
    })

    message_id1 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })
    message_id2 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Welcome to COMP1531"
    })
    message_id3 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user2.json()['token'],
        'channel_id':channel1.json()['channel_id'],
        'message': "21T1"
    })

    res = requests.get(f"{url}/channel/messages/v2", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert res.status_code == 200
    payload = res.json()
    print(payload)
    assert payload['messages'][0]['message_id'] == message_id3.json()['message_id']
    assert payload['messages'][1]['message_id'] == message_id2.json()['message_id']
    assert payload['messages'][2]['message_id'] == message_id1.json()['message_id']

    assert payload['messages'][0]['u_id'] == user2.json()['auth_user_id']
    assert payload['messages'][1]['u_id'] == user2.json()['auth_user_id']
    assert payload['messages'][2]['u_id'] == user2.json()['auth_user_id']

    assert payload['messages'][0]['message'] == "21T1"
    assert payload['messages'][1]['message'] == "Welcome to COMP1531"
    assert payload['messages'][2]['message'] == "Hello"
    
    assert payload['end'] == -1 

def test_message_send_unauthorized():
    requests.delete(f"{url}/clear/v1")

    user3 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'banesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Bane',
        'name_last': 'Smith',
    })
    user4 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'Kanesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Kane',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user3.json()['token'], 
        'name': 'COMP1531', 
        'is_public': True
    })

    res = requests.post(f"{url}/message/send/v2", json = { 
        'token': user4.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    assert(res.status_code == 403)
    
def test_message_send_too_long():
    requests.delete(f"{url}/clear/v1")

    user5 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'lanesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Lane',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user5.json()['token'], 
        'name': 'Channel1', 
        'is_public': True
    })

    res = requests.post(f"{url}/message/send/v2", json = { 
        'token': user5.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "A"*1001
    })

    assert(res.status_code == 400)
  