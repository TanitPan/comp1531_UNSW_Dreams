'''This file consists of Python tests for standup_send_v1 in standup.py'''

import pytest
from src.auth import auth_register_v2
from src.channels import channels_create_v2, channels_list_v2
from src.error import InputError, AccessError
from src.helper import generate_token
from src.other import clear_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from datetime import datetime, timezone
import time

def test_standup_send_typecheck():
    """ Test that the type is correct when sending a message in standup_send"""
    # Clear data, register a user, token and channel_id
    clear_v1()
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token = authorised_info["token"]
    channel = channels_create_v2(token, "Channel1", False)
    channel_id = channel["channel_id"]
    
    # Start a standup for five seconds and then send two message in the buffered
    # queue 
    standup_start_v1(token, channel_id, 5)
    return_value1 = standup_send_v1(token, channel_id, "Hello World")
    return_value2 = standup_send_v1(token, channel_id, "Byebye")
    # Let the function do nothing for 5 seconds
    time.sleep(5)
    # Check the return value type to be a dictionary and an empty dictionary
    assert isinstance(return_value1, dict)    
    assert return_value1 == {}
    assert isinstance(return_value2, dict)
    assert return_value2 == {}    
    # Will call messages_send function and compare the ids once it has been written

def test_standup_send_invalidchannel():
    """Test that an invalid channel id will be discounted"""
    # Clear data, register a user and token
    clear_v1()
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token = authorised_info["token"]
    
    # Create a valid channel id and then add one to it for an invalid id
    channel = channels_create_v2(token, "Channel2", True)
    channel_id = channel["channel_id"]
    invalid_channel_id = channel_id + 1
    # Using the channel_id of the first channel, start a standup 
    standup_start_v1(token, channel_id, 5)
    # Attempt to send a message with the invalid ID should raise an error 
    with pytest.raises(InputError):
        standup_send_v1(token, invalid_channel_id, "2021")

def test_standup_send_different_channels():
    """Test two messages can be delayed in different standups"""
    # Clear all data, register a user and token
    clear_v1()
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token = authorised_info["token"]
    # Create two channels with their respective channel IDs
    channel1 = channels_create_v2(token, "Channel3", True)
    channel_id1 = channel1["channel_id"]
    channel2 = channels_create_v2(token, "Channel4", False)
    channel_id2 = channel2["channel_id"]
    
    # Using the first channel's channel_id, start a standup and send a message
    standup_start_v1(token, channel_id1, 5)
    value1 = standup_send_v1(token, channel_id1, "COMP1531")
    assert value1 == {}
    # Using the second channel's channel_id, start a standup and send a message
    standup_start_v1(token, channel_id2, 5)
    value2 = standup_send_v1(token, channel_id2, "Project is due")
    assert value2 == {}

def test_standup_send_toolong_message():
    """Test to check that a message over 1000 characters will not be sent"""
    # Clear data, register a user, extract a token and start a standup
    clear_v1()
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token = authorised_info["token"]
    channel = channels_create_v2(token, "Channel5", True)
    channel_id = channel["channel_id"]
    standup_start_v1(token, channel_id, 5)
    # Create a message with 1005 characters
    message = "abcde" * 201
    # Attempting to send a message over 1000 characters should raise an InputError 
    with pytest.raises(InputError):
        standup_send_v1(token, channel_id, message)
        
def test_standup_send_inactive():
    """Test verifying an inactive standup will raise an InputError"""
    # Clear data, register a user and get a token (without starting a standup)
    clear_v1()
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token = authorised_info["token"]
    channel = channels_create_v2(token, "Channel6", False)
    channel_id = channel["channel_id"]
    # Calling standup_send should register an InputError as an active standup is
    # not running 
    with pytest.raises(InputError):
        standup_send_v1(token, channel_id, "New message")  

def test_standup_send_notmember():
    """Test checking that a non-member of the channel cannot send a message"""
    # Clear data, register a user, get a token and channel_id
    clear_v1()
    authorised_info1 = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token1 = authorised_info1["token"]
    channel = channels_create_v2(token1, "Channel7", True)
    channel_id = channel["channel_id"]
    # Register a new user who is not added as a member of the channel
    authorised_info2 = auth_register_v2("john.doe@yahoo.com", "password2021", 
                           "john", "doe")
    token2 = authorised_info2["token"]
    # An AccessError should be raised if the token of a non-member is passed in
    with pytest.raises(AccessError):
        standup_send_v1(token2, channel_id, "New message")  

    
def test_standup_send_unauthorised_user():
    """Test verifying an unauthorised user cannot send a message in the standup"""
    # Clear all data, register a user,  get a token and channel_id
    clear_v1()
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token1 = authorised_info["token"]
    channel = channels_create_v2(token1, "Channel6", True)
    channel_id = channel["channel_id"]
    # Increase the auth_user_id by one and use it to generate a second (invalid)
    # token
    user_id = authorised_info["auth_user_id"] + 1
    token2 = generate_token(user_id)
    # Calling standup_send should register an InputError as an active standup is
    # not running 
    with pytest.raises(AccessError):
        standup_send_v1(token2, channel_id, "Today is a good day")  
