'''This file consists of Python tests for standup_start_v1 in standup.py'''

import pytest
from src.auth import auth_register_v2
from src.channels import channels_create_v2, channels_list_v2
from src.error import InputError, AccessError
from src.helper import generate_token
from src.other import clear_v1
from src.standup import standup_start_v1, standup_active_v1
from datetime import datetime, timezone

# Confirms that a valid startup can be started 
def test_standup_start_valid():
    # Clear data 
    clear_v1() 
    # Register a user and create a channel 
    authorised_info = auth_register_v2('j.smith@gmail.com', 'newpassword', 
                           'jack', 'smith')
    token = authorised_info['token'] 
    channel = channels_create_v2(token, "Channel_1", True) 
    channel_id = channel["channel_id"]
    # Call the standup start function and ensure the result is a dictionary, 
    # containing an integer
    timestamp = standup_start_v1(token, channel_id, 5)
    assert (isinstance(timestamp, dict) == True)
    time_finish = timestamp["time_finish"]
    assert (isinstance(time_finish, int) == True)
    # Confirm that the current timestamp is less than the called timestamp
    now = datetime.now()
    now_timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    assert (time_finish > now_timestamp)
   
# Test confirming an error is raised when the standup_start is called when the
# standup is already active
def test_standup_start_repeated():
    # Clear all data, register a dummy account and create a channel 
    clear_v1() 
    authorised_info = auth_register_v2('j.smith@gmail.com', 'newpassword', 
                           'jack', 'smith')
    token = authorised_info['token'] 
    channel = channels_create_v2(token, "Channel_2", False) 
    channel_id = channel["channel_id"]
    # Begin a standup and quickly try and begin a second open for the same 
    # channel_id
    standup_start_v1(token, channel_id, 100)
    with pytest.raises(InputError):
        standup_start_v1(token, channel_id, 1)

# Test that an invalid channel input would raise an error
def test_standup_start_invalid_channel():
    # Clear data and register an user
    clear_v1() 
    authorised_info = auth_register_v2('j.smith@gmail.com', 'newpassword', 
                           'jack', 'smith')
    token = authorised_info['token'] 
    # Create a channel and increment its channel id by one
    channel = channels_create_v2(token, "Channel_3", True) 
    invalid_channel_id = channel["channel_id"] + 1
    # Pass this new id into the standup and test that an error is raised
    with pytest.raises(InputError): 
        standup_start_v1(token, invalid_channel_id, 1)

# Test that an AccessError is raised when an invalid token is passed in 
def test_standup_start_invalid_token():
    # Clear data, register a user and create a channel 
    clear_v1() 
    authorised_info = auth_register_v2('j.smith@gmail.com', 'newpassword', 
                           'jack', 'smith')
    token = authorised_info['token'] 
    channel = channels_create_v2(token, "Channel_4", False) 
    channel_id = channel["channel_id"]
    
    # Generate a token for an unauthorised user, by incrementing the user id by 
    # one and calling it in the generate_token function.
    non_authorised_user = authorised_info['auth_user_id'] + 1
    token2 = generate_token(non_authorised_user)
    # Confirm an AccessError is raised for this invalid input
    with pytest.raises(AccessError): 
        standup_start_v1(token2, channel_id, 1)

# Test that an authorised user who is not a member of the channel cannot 
# start a standup
def test_standup_start_unauthorised_user():
    # Clear data, register a user and create a channel 
    clear_v1() 
    authorised_info = auth_register_v2('j.smith@gmail.com', 'newpassword', 
                           'jack', 'smith')
    token = authorised_info['token'] 
    channel = channels_create_v2(token, "Channel_5", True) 
    channel_id = channel["channel_id"]
    # Register a second user and extract their token
    authorised_info = auth_register_v2('jane.doe@gmail.com', 'password1', 
                           'jane', 'doe')
    token2 = authorised_info['token'] 
    # Test that an AccessError is raised when this second token is passed in
    with pytest.raises(AccessError): 
        standup_start_v1(token2, channel_id, 1)
