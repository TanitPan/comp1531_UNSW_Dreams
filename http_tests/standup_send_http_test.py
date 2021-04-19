'''This file consists of HTTP server tests for standup_send_v1 in standup.py'''

from src.config import url
from src.helper import generate_token
import json
import pytest
import requests
import time

def test_standup_send_valid():
    """ Test for a valid sending of a message within a standup"""
    # Clear all data, extract token and channel_id
    requests.delete(url + "clear/v1")
    authorised_info = requests.post(url + "auth/register/v2", json = {
        'email': 'standuplover@gmail.com',
        'password': 'sendhttp',
        'name_first': 'stan',
        'name_last': 'lover',
    })
    payload = authorised_info.json()
    token = payload['token']

    request = requests.post(url + "channels/create/v2", json = {
        'token': token,
        'name': 'Channel_1',
        'is_public': False,
    })
    payload = request.json()
    channel_id = payload['channel_id']

    # Start up a standup, passing in a token, channel_id and length
    requests.post(url + "standup/start/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'length': 5,
    })
  
    # Attempt to send a simple string message
    request = requests.post(url + "standup/send/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'message': "Hello everyone",
    })
    # Sleep the test function for a couple of seconds before checking the status
    # code and the payload to be 200 and an empty dictionary respectively
    time.sleep(5)
    assert request.status_code == 200
    payload = request.json()
    assert payload == {}

def test_standup_send_invalid_channel():
    """ Test that a channel_id that hasn't been created cannot be used to send a
    message"""
    # Clear data and extract token
    requests.delete(url + "clear/v1")
    authorised_info = requests.post(url + "auth/register/v2", json = {
        'email': 'unswstudent@gmail.com',
        'password': 'kensington',
        'name_first': 'unsw',
        'name_last': 'student',
    })
    payload = authorised_info.json()
    token = payload['token']

    # Create a legitimate channel-id for the standup start function
    request = requests.post(url + "channels/create/v2", json = {
        'token': token,
        'name': 'Channel_2',
        'is_public': True,
    })
    payload = request.json()
    channel_id = payload['channel_id']

    # Start up a standup, passing in a token, channel_id and length
    requests.post(url + "standup/start/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'length': 2,
    })

    # Increment the valid channel_id by one for an invalid id and pass that in 
    # standup/send. Ensure an InputError is raised
    invalid_channel_id = channel_id + 1
    request = requests.post(url + "standup/send/v1", json = {
        'token': token,
        'channel_id': invalid_channel_id,
        'message': "G'day",
    })
    assert request.status_code == 400

def test_standup_send_long_message():
    """ Test that a message over 1000 characters cannot be sent in the standup"""
    # Clear data and obtain both the token and channel_id
    requests.delete(url + "clear/v1")
    authorised_info = requests.post(url + "auth/register/v2", json = {
        'email': 'p.watson@gmail.com',
        'password': 'penny2020',
        'name_first': 'penelope',
        'name_last': 'watson',
    })
    payload = authorised_info.json()
    token = payload['token']
 
    request = requests.post(url + "channels/create/v2", json = {
        'token': token,
        'name': 'Channel3',
        'is_public': False,
    })
    payload = request.json()
    channel_id = payload['channel_id']

    # Start up a standup with the required arguments
    requests.post(url + "standup/start/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'length': 4,
    })
    # Try to pass in a very long string (over 1000 characters). A 400 error
    # should be raised
    message = "comp1531" * 127
    request = requests.post(url + "standup/send/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'message': message,
    })
    assert request.status_code == 400

def test_standup_send_inactive_standup():
    """ Test checking that no messages will be sent with a standup that is not
    running"""
    # Clear data, registering a user and making a channel
    requests.delete(url + "clear/v1")
    authorised_info = requests.post(url + "auth/register/v2", json = {
        'email': 'prue.vines@gmail.com',
        'password': 'pruevines',
        'name_first': 'prue',
        'name_last': 'vines',
    })
    payload = authorised_info.json()
    token = payload['token']

    request = requests.post(url + "channels/create/v2", json = {
        'token': token,
        'name': 'Channel4',
        'is_public': True,
    })
    payload = request.json()
    channel_id = payload['channel_id']

    # Without calling standup_start, test if the standup can send a message
    request = requests.post(url + "standup/send/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'message': "this is a message",
    })
    # Confirm a 400 message is raised
    assert request.status_code == 400
    
def test_standup_send_not_member():
    """ Test checking a message that is sent by a user who is not a member of
    channel cannot be sent"""
    # Following the clearing of data, register a user
    requests.delete(url + "clear/v1")
    authorised_info1 = requests.post(url + "auth/register/v2", json = {
        'email': 'alex.steel@gmail.com',
        'password': 'alexsteel2000',
        'name_first': 'alex',
        'name_last': 'steel',
    })
    payload = authorised_info1.json()
    token1 = payload['token']

    # Create a channel using that user's token
    request = requests.post(url + "channels/create/v2", json = {
        'token': token1,
        'name': 'Channel5',
        'is_public': True,
    })
    payload = request.json()
    channel_id = payload['channel_id']

    # Register a second user, who does not belong to any channel
    authorised_info2 = requests.post(url + "auth/register/v2", json = {
        'email': 'david.brown@gmail.com',
        'password': 'password2',
        'name_first': 'david',
        'name_last': 'brown',
    })
    payload = authorised_info2.json()
    token2 = payload['token']

    # Start up a standup with the token of the channel member
    requests.post(url + "standup/start/v1", json = {
        'token': token1,
        'channel_id': channel_id,
        'length': 4,
    })

    # Send a message with the second user's details and check to see if a 403
    # message has been raised as expected
    request = requests.post(url + "standup/send/v1", json = {
        'token': token2,
        'channel_id': channel_id,
        'message': "TERM ONE",
    })

    # Confirm a 403 message is raised
    assert request.status_code == 403

def test_standup_send_invalid_token():
    """ Generating an invalid token, this test ensures this user will not be
    able to use standup_send"""
        # Following the clearing of data, register a user
    requests.delete(url + "clear/v1")
    authorised_info1 = requests.post(url + "auth/register/v2", json = {
        'email': 'kate.sharma@outlook.com',
        'password': 'password1234',
        'name_first': 'kate',
        'name_last': 'sharma',
    })
    payload = authorised_info1.json()
    token1 = payload['token']
    # Increase their user_id by one and generate a new token
    invalid_auth_user_id = payload["auth_user_id"] + 1
    token2 = generate_token(invalid_auth_user_id)
    # Using the first valid token, create a channel and start a standup
    request = requests.post(url + "channels/create/v2", json = {
        'token': token1,
        'name': 'Channel6',
        'is_public': False,
    })
    payload = request.json()
    channel_id = payload['channel_id']

    requests.post(url + "standup/start/v1", json = {
        'token': token1,
        'channel_id': channel_id,
        'length': 4,
    })

    # Send a message with the invalid token and confirm that a 403 status code
    # has been raised
    request = requests.post(url + "standup/send/v1", json = {
        'token': token2,
        'channel_id': channel_id,
        'message': "Invalid token",
    })

    # Confirm a 403 message is raised
    assert request.status_code == 403
