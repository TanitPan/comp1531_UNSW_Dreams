from src.config import url
import pytest
import json
import requests

def test_message_edit():
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
    message_id2 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "World"
    })

    requests.put(f"{url}/message/edit/v2", json = { 
        'token': user1.json()['token'],
        'message_id': message_id2.json()['message_id'],
        'message': "COMP1531"
    })

    res = requests.get(f"{url}/channel/messages/v2", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert res.status_code == 200
    payload = res.json()

    assert payload['messages'][0]['message_id'] == message_id2.json()['message_id']
    assert payload['messages'][1]['message_id'] == message_id1.json()['message_id']

    assert payload['messages'][0]['u_id'] == user1.json()['auth_user_id']
    assert payload['messages'][1]['u_id'] == user1.json()['auth_user_id']
    
    assert payload['messages'][0]['message'] == "COMP1531"
    assert payload['messages'][1]['message'] == "Hello"
    
    assert payload['end'] == -1 


def test_message_edit_more():
    # Clear the data
    requests.delete(f"{url}/clear/v1")

    user2 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'janesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Jane',
        'name_last': 'Smith',
    })

    user3 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'banesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Bane',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user2.json()['token'], 
        'name': 'COMP1531', 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite/v2", json = {
        'token' : user2.json()['token'],
        'channel_id' : channel1.json()['channel_id'],
        'u_id' : user3.json()['auth_user_id'],
    })

    message_id1 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello, Welcome to COMP1531"
    })
    message_id2 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user3.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello, Thanks for adding me"
    })

    requests.put(f"{url}/message/edit/v2", json = { 
        'token': user3.json()['token'],
        'message_id': message_id2.json()['message_id'],
        'message': "Hello, Thank you for the invitation"
    })

    message_id3 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user2.json()['token'],
        'channel_id':channel1.json()['channel_id'],
        'message': "No prob"
    })

    requests.put(f"{url}/message/edit/v2", json = { 
        'token': user2.json()['token'],
        'message_id': message_id3.json()['message_id'],
        'message': "No worries"
    })

    res = requests.get(f"{url}/channel/messages/v2", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert res.status_code == 200
    payload = res.json()

    assert payload['messages'][0]['message_id'] == message_id3.json()['message_id']
    assert payload['messages'][1]['message_id'] == message_id2.json()['message_id']
    assert payload['messages'][2]['message_id'] == message_id1.json()['message_id']

    assert payload['messages'][0]['u_id'] == user2.json()['auth_user_id']
    assert payload['messages'][1]['u_id'] == user3.json()['auth_user_id']
    assert payload['messages'][2]['u_id'] == user2.json()['auth_user_id']

    assert payload['messages'][0]['message'] == "No worries"
    assert payload['messages'][1]['message'] == "Hello, Thank you for the invitation"
    assert payload['messages'][2]['message'] == "Hello, Welcome to COMP1531"
    
    assert payload['end'] == -1 


def test_message_edit_unauthorized():
    requests.delete(f"{url}/clear/v1")

    user4 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'Kanesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Kane',
        'name_last': 'Smith',
    })

    user5 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'lanesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Lane',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user4.json()['token'], 
        'name': 'COMP1531', 
        'is_public': True
    })

    requests.post(f"{url}/channel/invite/v2", json = {
        'token' : user4.json()['token'],
        'channel_id' : channel1.json()['channel_id'],
        'u_id' : user5.json()['auth_user_id'],
    })

    message_id1 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user4.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello, Welcome to COMP1531"
    })

    msg_id1_edit = requests.put(f"{url}/message/edit/v2", json = { 
        'token': user5.json()['token'],
        'message_id': message_id1.json()['message_id'],
        'message': "hElLo, wElCoMe To CoMP!$3!"
    })

    assert msg_id1_edit.status_code == 403


def test_message_send_too_long():
    requests.delete(f"{url}/clear/v1")

    user6 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'ranesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Rane',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user6.json()['token'], 
        'name': 'Channel1', 
        'is_public': True
    })

    message_id1 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user6.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello, Welcome to COMP1531"
    })

    msg_id1_edit = requests.put(f"{url}/message/edit/v2", json = { 
        'token': user6.json()['token'],
        'message_id': message_id1.json()['message_id'],
        'message': "A"*1001
    })

    assert(msg_id1_edit.status_code == 400)

def test_message_edit_not_exist():
    requests.delete(f"{url}/clear/v1")

    user7 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'Qanesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Qane',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user7.json()['token'], 
        'name': 'Channel1', 
        'is_public': True
    })

    message_id1 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user7.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello, Welcome to COMP1531"
    })

    msg_id1_edit = requests.put(f"{url}/message/edit/v2", json = { 
        'token': user7.json()['token'],
        'message_id': 100,
        'message': "A"*1001
    })

    assert(msg_id1_edit.status_code == 400)

def test_message_edit_empty():
    requests.delete(f"{url}/clear/v1")

    user8 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'Yohnsmith@gmail.com',
        'password': 'password123',
        'name_first': 'Yohn',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user8.json()['token'], 
        'name': 'Channel1', 
        'is_public': True
    })

    message_id1 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user8.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello"
    })

    requests.put(f"{url}/message/edit/v2", json = { 
        'token': user8.json()['token'],
        'message_id': message_id1.json()['message_id'],
        'message': ""
    })

    res = requests.get(f"{url}/channel/messages/v2", params = {
        'token': user8.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert res.status_code == 200
    payload = res.json()

    assert payload['end'] == -1