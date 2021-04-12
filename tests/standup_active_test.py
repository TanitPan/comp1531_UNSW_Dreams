'''This file consists of Python tests for standup_active_v1 in standup.py'''

import pytest
from src.auth import auth_register_v2
from src.channels import channels_create_v2, channels_list_v2
from src.error import InputError, AccessError
from src.helper import generate_token
from src.other import clear_v1
from src.standup import standup_start_v1, standups, standup_active_v1
from datetime import datetime, timezone

# Test confirming that standup_active works successfully when no standup is 
# running
def test_standup_active_norunning():
    # Clear data
    clear_v1() 
    standups.clear() 
    # Register a user and create a channel, extracting token and id
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token = authorised_info["token"] 
    channel = channels_create_v2(token, "Channel1", False) 
    channel_id = channel["channel_id"]
    # Call the function, confirminng the return value is a dictionary and the 
    # values for is_active and time_finish are False and None
    standup_return = standup_active_v1(token, channel_id)
    assert (isinstance(standup_return, dict) == True)
    assert standup_return["is_active"] == False
    assert standup_return["time_finish"] == None

# Test confirming standup_active works when a standup is currently running
def test_standup_active_running():
    # Clear data
    clear_v1() 
    standups.clear() 
    # Register a user and create a channel
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token = authorised_info["token"] 
    channel = channels_create_v2(token, "Channel2", True) 
    channel_id = channel["channel_id"]
    # Start a standup using the channel_id and token 
    standup_start_v1(token, channel_id, 100)
    # Check standup_active and validate the is_active and time_finish values 
    # are correct, checking the type of the latter
    standup_return = standup_active_v1(token, channel_id)
    assert standup_return["is_active"]
    assert isinstance(standup_return["time_finish"], int)

# Test confirming standup_active works when multiple standups are running for 
# separate channels 
def test_standup_active_multiple():
    # Clear all data
    clear_v1() 
    standups.clear() 
    # Register a user and create two channels
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token = authorised_info["token"] 
    channel1 = channels_create_v2(token, "Channel3", False) 
    channel_id1 = channel1["channel_id"]
    channel2 = channels_create_v2(token, "Channel4", True) 
    channel_id2 = channel2["channel_id"]
    
    # Start a standup using the first channel_id and the user's token 
    standup_start_v1(token, channel_id1, 100)
    # Start a second standup for the second channel
    standup_start_v1(token, channel_id2, 100)
    # Confirm both have a True reading for their is_active value
    standup_return1 = standup_active_v1(token, channel_id1)
    assert standup_return1["is_active"]
    standup_return2 = standup_active_v1(token, channel_id2)
    assert standup_return2["is_active"]

# Test confirming an InputError is raised for an invalid channel id 
def test_standup_active_channelinvalid():
    # Clear all data
    clear_v1() 
    standups.clear() 
    # Register a user and create a channel
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token = authorised_info["token"] 
    channel = channels_create_v2(token, "Channel5", False) 
    # Obtaining the channel_id, increase it by one to create an invalid id
    invalid_channel_id = channel["channel_id"] + 1
    # Check that an InputError is raised for the invalid_channel_id being used
    # as a parameter
    with pytest.raises(InputError): 
        standup_active_v1(token, invalid_channel_id)

# Test the token to make sure it's valid or else raise an AccessError
def test_standup_start_invalidtoken():
    # Clear all data, generate a token from a valid user and create a channel 
    clear_v1() 
    standups.clear() 
    authorised_info = auth_register_v2("hayden.smith@gmail.com", "pass1234", 
                           "hayden", "smith")
    token = authorised_info["token"]
    channel = channels_create_v2(token, "Channel6", True) 
    channel_id = channel["channel_id"]
    # Generate a second token by increasing the auth_user_id by one and 
    # calling the generate_token function
    unauthorised_auth_id = authorised_info["auth_user_id"] + 1
    unauthorised_token = generate_token(unauthorised_auth_id)
    # Check that an AccessError is raised in response to the invalid token
    with pytest.raises(AccessError): 
        standup_active_v1(unauthorised_token, channel_id)
