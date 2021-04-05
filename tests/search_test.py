'''This file consists of Python tests for search_v2 in other.py'''

import pytest

from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.message import message_send_v2
from src.helper import generate_token
from src.other import clear_v1, search_v2

# Test for the type of the search function when no messages have been sent 
def test_search_type():
    # Clear and register the user
    clear_v1()
    authorised_info = auth_register_v2("z555555@unsw.com", "password", "unsw", 
                      "student")
    token = authorised_info["token"]
    # Call the search function, obtaining all messages with the substring
    messages = search_v2(token, "hello")
    # Confirms format of the messages
    assert (messages == {'messages': []})
    # Confirms the type of the messages to be a dictionary 
    assert(isinstance(messages, dict) == True) 

# Test that a too large query string will raise an InputError   
def test_search_toolarge_querystr():
    # Clear and register a user
    clear_v1()
    authorised_info = auth_register_v2("z555555@unsw.com", "password", "unsw", 
                      "student")
    token = authorised_info["token"]
    # Create a query string that is longer than 1000 characters and confirm 
    # an error is raised
    query_str = "abcde" * 201
    with pytest.raises(InputError):
        search_v2(token, query_str)
   
# Need to adjust when updated code is pushed   
# Test confirming that the code works for an instance where a particular message
# is in the list   
def test_search_messages():
    # Clear and register a user
    clear_v1()
    authorised_info = auth_register_v2("z555555@unsw.com", "password", "unsw", 
                      "student")
    token = authorised_info["token"]
    
    # Create a channel and send a message to that channel 
    channel = channels_create_v2(token, "Channel0", False)
    channel_id = channel["channel_id"]
    message_send_v2(token, channel_id, "Hello everyone")
    # Confirm this message is available after searching for it
    messages = search_v2(token, "Hello")  
    # Verify the type of the result (messages dict and list)
    assert (isinstance(messages, dict) == True)
    assert (isinstance(messages["messages"], list) == True)  
    
# Test that an invalid token will raise an AccessError                     
def test_search_invalidtoken():
    # Clear and register a user
    clear_v1()
    authorised_info = auth_register_v2("z555555@unsw.com", "password", "unsw", 
                      "student")
    # Increase the valid user ID by one and generate a token using this new ID
    invalid_id = authorised_info["auth_user_id"] + 1
    invalid_token = generate_token(invalid_id)
    # Check an error is raised
    with pytest.raises(AccessError):
        search_v2(invalid_token, "Hello World")    
