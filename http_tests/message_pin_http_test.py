from src.config import url
import pytest
import json
import requests

############################# MESSAGE PIN ####################################
def test_message_pin():
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
        'message': "Hello, Welcome to COMP1531"
    })

    requests.post(f"{url}/message/pin/v1", json = {
        'token': user1.json()['token'],
        'message_id': message_id1.json()['message_id']
    })

    res = requests.get(f"{url}/channel/messages/v2", params = {
        'token': user1.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert res.status_code == 200
    payload = res.json()

    assert payload['messages'][0]['message_id'] == message_id1.json()['message_id']

    assert payload['messages'][0]['u_id'] == user1.json()['auth_user_id']
    
    assert payload['messages'][0]['message'] == "Hello, Welcome to COMP1531"
    
    assert payload['messages'][0]['is_pinned'] == True

    assert payload['end'] == -1 


def test_message_pin_more():
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
        'message': "Hello, Welcome to COMP1531"
    })
    message_id2 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Please read the channel rules"
    })

    message_id3 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user2.json()['token'],
        'channel_id':channel1.json()['channel_id'],
        'message': "1. Do not be rude!"
    })
    message_id4 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user2.json()['token'],
        'channel_id':channel1.json()['channel_id'],
        'message': "2. Do not spam"
    })
    message_id5 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user2.json()['token'],
        'channel_id':channel1.json()['channel_id'],
        'message': "3. Please do not post anything that may be construed as academic misconduct"
    })

    message_id6 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user2.json()['token'],
        'channel_id':channel1.json()['channel_id'],
        'message': "Enjoy your time in this channel :D"
    })

    requests.post(f"{url}/message/pin/v1", json = {
        'token': user2.json()['token'],
        'message_id': message_id1.json()['message_id']
    })

    requests.post(f"{url}/message/pin/v1", json = {
        'token': user2.json()['token'],
        'message_id': message_id2.json()['message_id']
    })

    requests.post(f"{url}/message/pin/v1", json = {
        'token': user2.json()['token'],
        'message_id': message_id6.json()['message_id']
    })

    res = requests.get(f"{url}/channel/messages/v2", params = {
        'token': user2.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'start': 0
    })

    assert res.status_code == 200
    payload = res.json()

    assert payload['messages'][0]['message_id'] == message_id6.json()['message_id']
    assert payload['messages'][1]['message_id'] == message_id5.json()['message_id']
    assert payload['messages'][2]['message_id'] == message_id4.json()['message_id']
    assert payload['messages'][3]['message_id'] == message_id3.json()['message_id']
    assert payload['messages'][4]['message_id'] == message_id2.json()['message_id']
    assert payload['messages'][5]['message_id'] == message_id1.json()['message_id']

    assert payload['messages'][0]['u_id'] == user2.json()['auth_user_id']
    assert payload['messages'][1]['u_id'] == user2.json()['auth_user_id']
    assert payload['messages'][2]['u_id'] == user2.json()['auth_user_id']
    assert payload['messages'][3]['u_id'] == user2.json()['auth_user_id']
    assert payload['messages'][4]['u_id'] == user2.json()['auth_user_id']
    assert payload['messages'][5]['u_id'] == user2.json()['auth_user_id']

    assert payload['messages'][0]['message'] == "Enjoy your time in this channel :D"
    assert payload['messages'][1]['message'] == "3. Please do not post anything that may be construed as academic misconduct"
    assert payload['messages'][2]['message'] == "2. Do not spam"
    assert payload['messages'][3]['message'] == "1. Do not be rude!"
    assert payload['messages'][4]['message'] == "Please read the channel rules"
    assert payload['messages'][5]['message'] == "Hello, Welcome to COMP1531"
    
    assert payload['messages'][0]['is_pinned'] == True
    assert payload['messages'][1]['is_pinned'] == False
    assert payload['messages'][2]['is_pinned'] == False
    assert payload['messages'][3]['is_pinned'] == False
    assert payload['messages'][4]['is_pinned'] == True
    assert payload['messages'][5]['is_pinned'] == True
    
    assert payload['end'] == -1 


def test_message_pin_unauthorized_notmember():
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

    message_id1 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user3.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello, Welcome to COMP1531"
    })

    msg_id1_pin = requests.post(f"{url}/message/pin/v1", json = {
        'token': user4.json()['token'],
        'message_id': message_id1.json()['message_id']
    })

    assert msg_id1_pin.status_code == 403

def test_message_pin_unauthorized_notowner():
    requests.delete(f"{url}/clear/v1")

    user5 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'lanesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Lane',
        'name_last': 'Smith',
    })

    user6 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'ranesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Rane',
        'name_last': 'Smith',
    })

    channel1 = requests.post(f"{url}/channels/create/v2", json = {
        'token': user5.json()['token'], 
        'name': 'COMP1531', 
        'is_public': True
    })
    
    requests.post(f"{url}/channel/invite/v2", json = {
        'token' : user5.json()['token'],
        'channel_id' : channel1.json()['channel_id'],
        'u_id' : user6.json()['auth_user_id'],
    })

    message_id1 = requests.post(f"{url}/message/send/v2", json = { 
        'token': user5.json()['token'],
        'channel_id': channel1.json()['channel_id'],
        'message': "Hello, Welcome to COMP1531"
    })

    msg_id1_pin = requests.post(f"{url}/message/pin/v1", json = {
        'token': user6.json()['token'],
        'message_id': message_id1.json()['message_id']
    })

    assert msg_id1_pin.status_code == 403


def test_message_pin_not_exist():
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
    assert message_id1.status_code == 400

    msg_id1_pin = requests.post(f"{url}/message/pin/v1", json = {
        'token': user7.json()['token'],
        'message_id': 100
    })

    assert(msg_id1_pin.status_code == 400)


def test_message_pin_by_owner():
    requests.delete(f"{url}/clear/v1")

    user8 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'Hanesmith@gmail.com',
        'password': 'password123',
        'name_first': 'Hane',
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
        'message': "Hello, Welcome to COMP1531"
    })

    msg_id1_pin = requests.post(f"{url}/message/pin/v1", json = {
        'token': user8.json()['token'],
        'message_id': message_id1.json()['message_id']
    })

    assert msg_id1_pin.status_code == 200

    msg_id2_pin = requests.post(f"{url}/message/pin/v1", json = {
        'token': user8.json()['token'],
        'message_id': message_id1.json()['message_id']
    })

    assert msg_id2_pin.status_code == 400
