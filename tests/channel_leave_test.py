'''This file consists of Python tests for channels_leave_v1 in channel.py'''

import pytest

from src.auth import auth_register_v2
from src.channel import channel_addowner_v1, channel_invite_v2, channel_leave_v1
from src.channels import channels_create_v2, channels_list_v2
from src.helper import generate_token
from src.error import InputError, AccessError
from src.other import clear_v1

def test_channel_leave_owner():
    clear_v1() 
    authorised_info1 = auth_register_v2("j.smith@gmail.com", "password", 
                      "john", "smith")     
    authorised_token1 = authorised_info1["token"]    
    channel = channels_create_v2(authorised_token1, "channel1", False) 
    channel_id = channel["channel_id"]         
    
    authorised_info2 = auth_register_v2("j.smith@ymail.com", "pass1234", 
                      "jane", "smith")  
    authorised_id2 = authorised_info2["auth_user_id"]    
    channel_addowner_v1(authorised_token1, channel_id, authorised_id2)
    channel_leave_v1(authorised_token1, channel_id)
    joined_channels = channels_list_v2(authorised_token1)
    assert (joined_channels == {'channels': []})
    
def test_channel_leave_member():
    clear_v1() 
    authorised_info1 = auth_register_v2("j.smith@gmail.com", "password", 
                      "john", "smith")     
    authorised_token1 = authorised_info1["token"]    
    channel = channels_create_v2(authorised_token1, "channel1", False) 
    channel_id = channel["channel_id"]         
    
    authorised_info2 = auth_register_v2("j.smith@ymail.com", "pass1234", 
                      "jane", "smith")  
    authorised_id2 = authorised_info2["auth_user_id"]    
    authorised_token2 = authorised_info2["token"]    
    channel_invite_v2(authorised_token1, channel_id, authorised_id2)
    joined_channels = channels_list_v2(authorised_token2)
    assert (joined_channels == {'channels': [{'channel_id': 1, 
            'name': 'channel1'},]})
    channel_leave_v1(authorised_token2, channel_id)
    joined_channels = channels_list_v2(authorised_token2)
    assert (joined_channels == {'channels': []})
    
def test_channel_leave_invalid_channel():
    clear_v1() 
    authorised_info = auth_register_v2("j.smith@gmail.com", "password", 
                      "john", "smith")     
    authorised_token = authorised_info["token"]    
    channel = channels_create_v2(authorised_token, "channel1", False) 
    invalid_channel_id = channel["channel_id"] + 1     

    with pytest.raises(InputError):
        channel_leave_v1(authorised_token, invalid_channel_id)
        
def test_channel_leave_invalid_token():
    clear_v1() 
    authorised_info = auth_register_v2("j.smith@gmail.com", "password", 
                      "john", "smith")     
    authorised_token = authorised_info["token"]    
    unauthorised_id = authorised_info["auth_user_id"] + 1  
    unauthorised_token = generate_token(unauthorised_id)
    channel = channels_create_v2(authorised_token, "channel1", False) 
    channel_id = channel["channel_id"]         
    
    authorised_info2 = auth_register_v2("j.smith@ymail.com", "pass1234", 
                      "jane", "smith")  
    with pytest.raises(AccessError):
        channel_leave_v1(unauthorised_token, channel_id)
        
def test_channel_leave_notamember():
    clear_v1() 
    authorised_info1 = auth_register_v2("j.smith@gmail.com", "password", 
                      "john", "smith")     
    authorised_token1 = authorised_info1["token"]    
    channel = channels_create_v2(authorised_token1, "channel1", False) 
    channel_id = channel["channel_id"]         
    
    authorised_info2 = auth_register_v2("j.smith@ymail.com", "pass1234", 
                      "jane", "smith")  
    authorised_token2 = authorised_info2["token"]              
    with pytest.raises(AccessError):
        channel_leave_v1(authorised_token2, channel_id)
