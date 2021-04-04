'''
This file contains HTTP server tests for channel_removeowner in src.channel, 
testing a valid owner is correctly removed and input/access errors are raised
'''

from src.config import url
from src.helper import generate_token
import json
import pytest
import requests

@pytest.fixture
def registered_user():
    # Registers an user
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        "email": "jane.doe@gmail.com",
        "password": "jane2021",
        "name_first": "jane",
        "name_last": "doe",
    })
    payload = authorised_info.json()
    return payload

# Test that a removed owner can be re-added as an owner successfully 
def test_channel_removeowner_adding_again():
    # Clear and register two users
    requests.delete(f"{url}/clear/v1") 
    authorised_info1 = registered_user()     
    token = authorised_info1["token"]  
    auth_user_id1 = authorised_info1["auth_user_id"] 
                             
    authorised_info2 = requests.post(f"{url}/auth/register/v2", json = {
        "email": "john.smith@gmail.com",
        "password": "password1",
        "name_first": "john",
        "name_last": "smith",
    })
    payload = authorised_info2.json()
    auth_user_id2 = payload["auth_user_id"]
    token2 = payload["token"]
 
    # Create a channel using the first user's token 
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Channel_1', 
        'is_public': False,
    })
    payload = channel.json()
    channel_id = payload["channel_id"]
    
    # Add the second user to the channel as an owner and subsequently remove 
    # the first user from owner status 
    request = requests.post(f"{url}/channel/addowner/v1", json = {
        'token': token, 
        'channel_id': channel_id,
        'u_id': auth_user_id2,
    })
    request = requests.post(f"{url}/channel/removeowner/v1", json = {
        'token': token2, 
        'channel_id': channel_id,
        'u_id': auth_user_id1,
    })
    assert request.status_code == 200 # Should return an success code 
    
    # Confirm that the removed owner can be added again as an owner, which is 
    # only possible if they do not have owner status
    request = requests.post(f"{url}/channel/addowner/v1", json = {
        'token': token2, 
        'channel_id': channel_id,
        'u_id': auth_user_id1,
    })
    # Confirm a success code is raised 
    assert request.status_code == 200 

# Test that an invalid channel id would create an InputError
def test_channel_removeowner_invalid_channelid():
    # Clear and register an user
    requests.delete(f"{url}/clear/v1") 
    authorised_info = registered_user()   
    token = authorised_info["token"]
    user_id = authorised_info["auth_user_id"]  
     
    # Create a channel, obtain its id and increment the id by one to create an 
    # invalid channel id       
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Channel_2', 
        'is_public': True
    })
    payload = channel.json()
    invalid_channel_id = payload["channel_id"] + 1
    
    # Attempt to remove the owner from the new and invalid channel_id should  
    # raise an InputError as it uses an invalid channel id
    request = requests.post(f"{url}/channel/removeowner/v1", json = {
        'token': token, 
        'channel_id': invalid_channel_id,
        'u_id': user_id,
    })
    assert request.status_code == 400 

# Test that prevents the owner that is being removed from the sole owner by 
# raising an error
def test_channel_removeowner_sole_owner():
    # Clear data and register an user
    requests.delete(f"{url}/clear/v1") 
    authorised_info = registered_user()   
    token = authorised_info["token"]
    user_id = authorised_info["auth_user_id"]  
    
    # Create a channel and make the registered user the only owner   
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Channel_3', 
        'is_public': True
    }) 
    payload = channel.json()
    channel_id = payload["channel_id"]
    
    # Removing this owner would give rise to an InputError as they are the only 
    # channel owner as per the specs
    request = requests.post(f"{url}/channel/removeowner/v1", json = {
        'token': token, 
        'channel_id': channel_id,
        'u_id': user_id,
    })
    assert request.status_code == 400 

# Test that confirms that an unauthorised user token (not an owner of Dreams or the 
# channel) will give rise to an AccessError 
def test_channel_removeowner_unauthorised_usertoken():       
    # Clear data and register an user
    requests.delete(f"{url}/clear/v1") 
    authorised_info = registered_user()   
    token = authorised_info["token"]
    user_id = authorised_info["auth_user_id"]  
    
    # Create a new channel, making the user its owner and the Dreams owner 
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Channel_3', 
        'is_public': True
    }) 
    
    # Register a second user and add them as a channel owner 
    authorised_info2 = requests.post(f"{url}/auth/register/v2", json = {
        "email": "john.smith@gmail.com",
        "password": "password1",
        "name_first": "john",
        "name_last": "smith",
    })
    payload = authorised_info2.json()
    auth_user_id2 = payload["auth_user_id"]
    
    request = requests.post(f"{url}/channel/addowner/v1", json = {
        'token': token, 
        'channel_id': channel_id,
        'u_id': auth_user_id2,
    })
   
    # Register a third user and, using their token, attempt to remove a previous 
    # owner from the channel 
    authorised_info3 = requests.post(f"{url}/auth/register/v2", json = {
        "email": "ben.franklin@gmail.com",
        "password": "lightning",
        "name_first": "ben",
        "name_last": "frankling",
    })
    payload = authorised_info3.json()
    token3 = payload["token"]
    
    request = requests.post(f"{url}/channel/removeowner/v1", json = {
        'token': token3, 
        'channel_id': channel_id,
        'u_id': auth_user_id2,
    })
    # Confirm this raises a 403 error code
    assert request.status_code == 403

# Test that an AccessError is raised if the user_id passed in does not belong to
# an owner of the channel
def test_channel_removeowner_unauthorised_user():
    # Clear data and register an user, using their token to create a channel 
    requests.delete(f"{url}/clear/v1") 
    payload = registered_user()
    token1 = payload["token"]
    
    channel = requests.post(f"{url}/channels/create/v2", json = {
        'token': token1, 
        'name': 'Channel_4', 
        'is_public': False
    })
    payload = channel.json()
    channel_id = payload["channel_id"]

    # Register another user and make them the owner of the channel
    authorised_info2 = requests.post(f"{url}/auth/register/v2", json = {
        "email": "john.smith@gmail.com",
        "password": "password1",
        "name_first": "john",
        "name_last": "smith",
    })
    payload = authorised_info2.json()
    auth_user_id2 = payload["auth_user_id"] 
    
    request = requests.post(f"{url}/channel/addowner/v1", json = {
        'token': token, 
        'channel_id': channel_id
        'u_id': auth_user_id2,
    })
   
    # Create a new user_id, which does not belong to an existing owner
    new_user = auth_user_id2 + 1
    # Using the valid token of the first owner, attempt to remove this new_user
    # and check an AccessError will be raised (403 status code)
    request = requests.post(f"{url}/channel/removeowner/v1", json = {
        'token': token1, 
        'channel_id': channel_id,
        'u_id': new_user,
    })
    assert request.status_code == 403



