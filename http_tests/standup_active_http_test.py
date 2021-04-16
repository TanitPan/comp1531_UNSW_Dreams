'''This file consists of HTTP server tests for standup_active_v1 in standup.py'''

from src.config import url
from src.helper import generate_token
import json
import pytest
import requests
    
# Test confirming that standup_active returns False and None respectively when  
# there is no active standup returns 
def test_standup_active_inactivestandup():
    # Clear all data and obtain the token and channel_id
    requests.delete(f"{url}/clear/v1")
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'z5555555@gmail.com', 
        'password': 'unswstudent', 
        'name_first': 'termone', 
        'name_last': 'student',
    })  
    payload = authorised_info.json()
    token = payload['token']    
    
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Channel1', 
        'is_public': False,
    })     
    payload = request.json()
    channel_id = payload['channel_id']
   
    # Test the status code of the request will be successful 
    payload = {
        "token": token,
        "channel_id": channel_id,
    }
    request = requests.get(f"{url}/standup/active/v1", 
    params = payload)
    assert request.status_code == 200
    
    # Extract the is_active and time_finish values, checking them against the 
    # expected values of False and None respectively
    payload = request.json()
    is_active = payload["is_active"]
    assert is_active == False
    time_finish = payload["time_finish"]
    assert time_finish == None
    
# Test confirming that standup_active returns True and the UTC timezone when  
# an active standup is called 
def test_standup_active_activestandup():
    # Clear all data and obtain the token and channel_id
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'h.smith@gmail.com', 
        'password': 'hayden', 
        'name_first': 'hayden', 
        'name_last': 'smith',
    })  
    payload = authorised_info.json()
    token = payload['token']    
    
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': token, 
        'name': 'Channel2', 
        'is_public': True,
    })     
    payload = request.json()
    channel_id = payload['channel_id']
    # Start a standup for 100 seconds
    r = requests.post(f"{url}/standup/start/v1", json = {
        "token": token,
        "channel_id": channel_id,
        "length": 100,
    })
    print(r.json())
    # Test the status code of the request to check if the standup is active and 
    # the call is successful 
    payload = {
        "token": token,
        "channel_id": channel_id,
    }
    request = requests.get(f"{url}/standup/active/v1", params = payload)
    assert request.status_code == 200 
    
    # Extract the is_active and time_finish values, checking them against the 
    # expected values of True and the expected integer return 
    payload = request.json()
    print(payload)
    is_active = payload["is_active"]
    assert is_active == True 
    time_finish = payload["time_finish"]
    assert isinstance(time_finish, int)

# Test checking that an invalid channel id will raise an InputError
def test_standup_active_invalidchannel():
    # Clear all data and obtain the token
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'james.cook@ymail.com', 
        'password': 'australia', 
        'name_first': 'james', 
        'name_last': 'cook',
    })  
    payload = authorised_info.json()
    token = payload['token']   
     
    # Add a random integer, which hasn't been called, generate an 
    # invalid_channel_id, passing it as a parameter to the standup_active call 
    invalid_channel_id =  100
    # Pass this invalid id into the standup/start POST request
    payload = {
        "token": token,
        "channel_id": invalid_channel_id,
    }
    request = requests.get(f"{url}/standup/active/v1", params = payload)
    # Confirm an input error is raised (400 error code)
    assert request.status_code == 400 

# Test that an invalid token being passed in as a parameter will cause an 
# AccessError
def test_standup_active_invalidtoken():
    # Clear all data
    requests.delete(f"{url}/clear/v1") 
    authorised_info = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'e.hillary@ymail.com', 
        'password': 'everest', 
        'name_first': 'edmund', 
        'name_last': 'hillary',
    })  
    payload = authorised_info.json()
    token1 = payload["token"]
    # Using a random user_id, generate a token
    token2 = generate_token(100)
    # Use the code to obtain a channel id
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': token1, 
        'name': 'Channel3', 
        'is_public': True,
    })     
    payload = request.json()
    print(payload)
    channel_id1 = payload["channel_id"] 
    
    # Pass the generated token into the GET request and ensure it returns a 
    # 403 Forbidden request
    payload = {
        "token": token2,
        "channel_id": channel_id1,
    }
    request = requests.get(f"{url}/standup/active/v1", params = payload)
    assert request.status_code == 403
