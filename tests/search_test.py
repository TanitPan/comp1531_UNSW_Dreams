'''This file consists of Python tests for search_v2 in other.py'''

import pytest

from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.message import message_send_v1
from src.helper import generate_token
from src.other import clear_v1, search_v2

def test_search_empty():
    clear_v1()
    authorised_info = auth_register_v2("z555555@unsw.com", "password", "unsw", 
                      "student")
    token = authorised_info["token"]
    messages = search_v2(token, "hello")
    assert (messages == [])
    assert(isinstance(messages, list) == True) 
    
def test_search_toolarge_querystr():
    clear_v1()
    authorised_info = auth_register_v2("z555555@unsw.com", "password", "unsw", 
                      "student")
    token = authorised_info["token"]
    query_str = "abcde" * 201
    with pytest.raises(InputError):
        search_v2(token, query_str)
"""   
# Need to adjust when updated code is pushed      
def test_search_messages():
    clear_v1()
    authorised_info = auth_register_v2("z555555@unsw.com", "password", "unsw", 
                      "student")
    token = authorised_info["token"]
    channel = channels_create_v2(token, "Channel0", False)
    channel_id = channel["channel_id"]
    message_send_v1(token, channel_id, "Hello everyone")  ##
    messages = search_v2(token, "Hello")  
    msg = messages[0]     ###
    assert (msg["message"] == "Hello everyone")"""
                     
def test_search_invalidtoken():
    clear_v1()
    authorised_info = auth_register_v2("z555555@unsw.com", "password", "unsw", 
                      "student")
    invalid_id = authorised_info["auth_user_id"] + 1
    invalid_token = generate_token(invalid_id)
    with pytest.raises(AccessError):
        search_v2(invalid_token, "Hello World")    
