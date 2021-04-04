'''This file consists of Python tests for channels_leave_v1 in channel.py'''

import pytest

from src.auth import auth_register_v2
from src.channel import channel_addowner_v1, channel_invite_v2, channel_leave_v1
from src.channels import channels_create_v2, channels_list_v2
from src.helper import generate_token
from src.error import InputError, AccessError
from src.other import clear_v1

# Test if an owner can leave a channel
def test_channel_leave_owner():
    # Clear data and register an user, obtaining their token id
    clear_v1() 
    authorised_info1 = auth_register_v2("j.smith@gmail.com", "password", 
                      "john", "smith")     
    authorised_token1 = authorised_info1["token"] 
    # Using the token id create a channel and extract the channel_id    
    channel = channels_create_v2(authorised_token1, "channel1", False) 
    channel_id = channel["channel_id"]         
    
    # Create a new user and add them as an owner
    authorised_info2 = auth_register_v2("j.smith@ymail.com", "pass1234", 
                      "jane", "smith")  
    authorised_id2 = authorised_info2["auth_user_id"]    
    channel_addowner_v1(authorised_token1, channel_id, authorised_id2)
    # Allow the first owner to leave the channel, looking through their list 
    # joined channels to confirm they have been removed
    channel_leave_v1(authorised_token1, channel_id)
    joined_channels = channels_list_v2(authorised_token1)
    assert (joined_channels == {'channels': []})
 
# Test if a member can leave a channel once they have been added in    
def test_channel_leave_member():
    # Clear data, register an user and a channel using that user's token
    clear_v1() 
    authorised_info1 = auth_register_v2("j.smith@gmail.com", "password", 
                      "john", "smith")     
    authorised_token1 = authorised_info1["token"]    
    channel = channels_create_v2(authorised_token1, "channel1", False) 
    channel_id = channel["channel_id"]         
    
    # Register a second user and invite them to the channel successfully
    authorised_info2 = auth_register_v2("j.smith@ymail.com", "pass1234", 
                      "jane", "smith")  
    authorised_id2 = authorised_info2["auth_user_id"]    
    authorised_token2 = authorised_info2["token"]    
    channel_invite_v2(authorised_token1, channel_id, authorised_id2)
    
    # Retrieve the list of the channels this second user has joined to confirm
    # they have been added in, using the assert
    joined_channels = channels_list_v2(authorised_token2)
    assert (joined_channels == {'channels': [{'channel_id': 1, 
            'name': 'channel1'},]})
    # Let this user leave the channel as a member and confirm they are no longer
    # listed as a member of the channel 
    channel_leave_v1(authorised_token2, channel_id)
    joined_channels = channels_list_v2(authorised_token2)
    assert (joined_channels == {'channels': []})

# Test that attempts to use an invalid channel id and ensures it raises an
# InputError   
def test_channel_leave_invalid_channel():
    clear_v1() # Clear data
    # Register an user and obtain their token 
    authorised_info = auth_register_v2("j.smith@gmail.com", "password", 
                      "john", "smith")     
    authorised_token = authorised_info["token"]  
    # Create a channel and increase it by one to create an invalid id  
    channel = channels_create_v2(authorised_token, "channel1", False) 
    invalid_channel_id = channel["channel_id"] + 1     
  
    # Test that an InputError is raised when this invalid channel id is used
    # as an argument
    with pytest.raises(InputError):
        channel_leave_v1(authorised_token, invalid_channel_id)

# Test to confirm an attempt to create an invalid token and pass it will result
# in an AccessError         
def test_channel_leave_invalid_token():
    # Clear data and register a new user
    clear_v1() 
    authorised_info = auth_register_v2("j.smith@gmail.com", "password", 
                      "john", "smith")     
    authorised_token = authorised_info["token"] 
   
    # After obtaining the user id, increase it by one to make it invalid. Use
    # this ID to generate an unauthorised_token
    unauthorised_id = authorised_info["auth_user_id"] + 1  
    unauthorised_token = generate_token(unauthorised_id)
    
    # Create a channel and obtain its ID    
    channel = channels_create_v2(authorised_token, "channel1", False) 
    channel_id = channel["channel_id"]         
    # Attempt to leave this channel using the unauthorised token 
    with pytest.raises(AccessError):
        channel_leave_v1(unauthorised_token, channel_id)

# Test that a non-member attempting to leave a channel will raise an AccessError        
def test_channel_leave_notamember():
    # Clear data, register an user and a channel using that user's token
    clear_v1() 
    authorised_info1 = auth_register_v2("j.smith@gmail.com", "password", 
                      "john", "smith")     
    authorised_token1 = authorised_info1["token"]    
    channel = channels_create_v2(authorised_token1, "channel1", False) 
    channel_id = channel["channel_id"]         
    
    # Create a new user, obtaining their token
    authorised_info2 = auth_register_v2("j.smith@ymail.com", "pass1234", 
                      "jane", "smith")  
    authorised_token2 = authorised_info2["token"]     
    
    # Confirm that passing in the second user's token will raise an AccessError
    # as they are not a member         
    with pytest.raises(AccessError):
        channel_leave_v1(authorised_token2, channel_id)
