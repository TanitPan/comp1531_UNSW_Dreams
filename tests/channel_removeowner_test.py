'''This file consists of Python tests for channels_removeowner_v1 in channel.py'''

import pytest

from src.channel import channel_addowner_v1, channel_removeowner_v1
from src.channels import channels_create_v2, channels_list_v2
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.other import clear_v1

# Test that a removevd owner is still part of the channel using channel_list
def test_channel_removeowner_channel_list():
    # Clear and register two users
    clear_v1() 
    authorised_info1 = auth_register_v2("j.smith@gmail.com", "john2021", 
                      "john", "smith")                    
    authorised_info2 = auth_register_v2("j.doe@gmail.com", "password", 
                      "jane", "doe")
    # Create a channel from the first owner's token 
    authorised_token1 = authorised_info1["token"]
    user_id1 = authorised_info1["auth_user_id"]
    channel_id = channels_create_v2(authorised_token1, "Channel1", True) 
    
    # Extract the second user's user_id and add them to the channel as an owner
    authorised_token2 = authorised_info1["token"]
    user_id2 = authorised_info2["auth_user_id"]
    channel_addowner_v1(authorised_token1, channel_id, user_id2)
    
    # Remove the original owner from the channel 
    channel_removeowner_v1(authorised_token2, channel_id, user_id1)
    
    # Confirm they are a part of the channel by looking at the channel list
    joined_channels = channels_list_v2(authorised_token1)
    assert (joined_channels == {'channels': [{'channel_id': 1, 
            'name': 'Channel1'},]})

# Test that an owner can be removed by re-adding them as an owner
def test_channel_removeowner_readd():
    clear_v1() # Clear
    # Register two users and create a channel using the first one's token 
    authorised_info1 = auth_register_v2("j.smith@gmail.com", "john2021", 
                      "john", "smith")                    
    authorised_info2 = auth_register_v2("j.doe@gmail.com", "password", 
                      "jane", "doe")
    authorised_token1 = authorised_info1["token"]
    user_id1 = authorised_info1["auth_user_id"]
    channel_id = channels_create_v2(authorised_token1, "Channel2", False) 
    
    # Extract the second user's user_id and add them to the channel as an owner
    authorised_token2 = authorised_info1["token"]
    user_id2 = authorised_info2["auth_user_id"]
    channel_addowner_v1(authorised_token1, channel_id, user_id2)
    
    # Remove the original owner from the channel 
    channel_removeowner_v1(authorised_token2, channel_id, user_id1)
    # Test if the owner can be re-added without raising an error
    channel_addowner_v1(authorised_token1, channel_id, user_id2)
    
# Test that passing in an invalid channel id will raise an InputError
def test_channel_removeowner_invalid_channel():
    # Clear and register an user
    clear_v1() 
    authorised_info = auth_register_v2("j.smith@gmail.com", "john2021", 
                      "john", "smith") 
    token = authorised_info["token"]
    user_id = authorised_info["auth_user_id"]  
     
    # Create an invalid channel_id by adding one to a valid id      
    invalid_channel_id = channels_create_v2(token, "Channel3", True) + 1
    # Validate that an InputError will be raised for this invalid channel_id
    with pytest.raises(InputError):
        channel_removeowner_v1(token, invalid_channel_id, user_id)

# Test confirming that if the owner being removed is the only owner, an Error
# will be raised
def test_channel_removeowner_onlyowner():
    # Clear and register an user
    clear_v1()
    authorised_info = auth_register_v2("j.smith@gmail.com", "john2021", 
                      "john", "smith") 
    token = authorised_info["token"]
    user_id = authorised_info["auth_user_id"]   
    
    # Create a new channel, making the user the only owner   
    channel_id = channels_create_v2(token, "Channel4", False) 
    # Attempt to remove this owner from the channel should create an InputError 
    # as they are the only owner of the channel
    with pytest.raises(InputError):
        channel_removeowner_v1(token, channel_id, user_id)

# Test that an AccessError will be raised if the authorised user is not 
# an owner of Dreams or of the channel 
def test_channel_removeowner_unauthorised_token():       
    # Clear and register an user
    clear_v1()
    authorised_info1 = auth_register_v2("j.smith@gmail.com", "john2021", 
                      "john", "smith") 
    token1 = authorised_info1["token"]    
    # Create a new channel, making the user its owner and the Dreams owner 
    channel_id = channels_create_v2(token1, "Channel4", False) 
    
    # Register a new user, adding them to the channel as an owner
    authorised_info2 = auth_register_v2("j.doe@gmail.com", "password", 
                      "jane", "doe") 
    auth_user_id2 = authorised_info2["auth_user_id"]   
    channel_addowner_v1(token1, channel_id, auth_user_id2)
    
    # Register a third user and, using their token, confirm removing this
    # second user from the channel will raise an AccessError
    authorised_info3 = auth_register_v2("t.jones@gmail.com", "1234", 
                      "tom", "jones") 
    token3 = authorised_info3["token"]
    with pytest.raises(AccessError):
        channel_removeowner_v1(token3, channel_id, auth_user_id2)

# Test that an AccessError is raised if the user with the user_id is not an 
# owner of the channel 
def test_channel_removeowner_unauthorised_user():
    # Clear and register an user
    clear_v1()
    authorised_info = auth_register_v2("j.smith@gmail.com", "john2021", 
                      "john", "smith") 
    token = authorised_info["token"]
    user_id = authorised_info["auth_user_id"]  
    
    # Create a new channel, making the user the only owner   
    channel_id = channels_create_v2(token, "Channel4", False) 
    # Create a new user_id, which does not belong to an owners
    new_user = user_id + 1
    # Attempt to remove the new user will generate an AccessError as they are 
    # not a channel owner 
    with pytest.raises(AccessError):
        channel_removeowner_v1(token, channel_id, new_user)

