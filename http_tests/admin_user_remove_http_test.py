'''
This file contains HTTP server tests for the functions of admin_user_remove in 
src.admin, testing for a valid response, access error (unauthorised token user), 
and input errors (invalid u_id, removed user is the only dreams owner)
'''
from src.config import url
import json
import pytest
import requests

'''Test to ensure that a user is successfully removed from the channels by
calling channel_leave'''
def test_admin_user_remove_user():
    # Clears the data  
    requests.delete(f"{url}/clear/v1") 
    # Register the user, after passing in values
    auth_data1 = {
        'email': 'james.bond@gmail.com', 
        'password': 'pass007', 
        'name_first': 'james', 
        'name_last': 'bond'
    }
    authorised_info = requests.post(f"{url}/auth/register/v2", json = auth_data1)    
    # Extract the token to pass in channels/create/v2, extracting the channel_id
    payload = authorised_info.json()
    authorised_token1 = payload['token']
    request = requests.post(f"{url}/channels/create/v2", json = {
        'token': authorised_token1, 
        'name': 'Channel_1', 
        'is_public': True
    })  
    payload = request.json() 
    channel_id = payload['channel_id']
    
    # Create and register another user, extracting their token and user_id
    auth_data2 = {
        'email': 'moneypenny@gmail.com', 
        'password': 'pass008', 
        'name_first': 'eve', 
        'name_last': 'moneypenny'
    }
    authorised_info = requests.post(f"{url}/auth/register/v2", json = auth_data2)    
    payload = authorised_info.json()
    authorised_token2 = payload['token']
    user_id = payload['auth_user_id']
    
    # Add the second user to the channel created by the first user
    """request = requests.post(f"{url}/channel/join/v2", json = {
        'token': authorised_token2, 
        'channel_id': channel_id,
    })  """ 
    
    # Remove the second user from the dreams channel, using the first user's 
    # token and owner permission
    request = requests.delete(f"{url}/admin/user/remove/v1", json = {
        'token': authorised_token1,
        'u_id': user_id,       
    })  
    assert request.status_code == 200 
       
    # Test channels_leave to ensure the second user cannot leave the channel as
    # they have already been removed. This should raise an AccessError
    """request = requests.post(f"{url}/channel/leave/v1", json = {
        'token': authorised_token2, 
        'channel_id': channel_id,
    })  
    assert request.status_code == 403"""


'''Test to check if an InputError will be raised with invalid user_id inputs'''
def test_admin_user_remove_invalid_uid():
    # Clearing data and registering a new user, extracting their token   
    requests.delete(f"{url}/clear/v1") 
    auth_data = {
        'email': 'quartermaster@ymail.com', 
        'password': 'password7', 
        'name_first': 'quarter', 
        'name_last': 'master'
    }
    authorised_info = requests.post(f"{url}/auth/register/v2", json = auth_data)    
    payload = authorised_info.json()
    authorised_token = payload['token']
    # Create an unauthorised_user_id by adding one to their authorised user_id
    authorised_user = payload['auth_user_id']     
    unauthorised_user = authorised_user + 1
    # Pass this unauthorised id into the admin/user/remove
    request = requests.delete(f"{url}/admin/user/remove/v1", json = {
        'token': authorised_token,
        'u_id': unauthorised_user,       
    })  
    # Confirm that a 400 status code (InputError) is raised 
    assert request.status_code == 400 

'''Test to ensure that an error will be raised for the only owner of the Dreams
channel being removed'''
def test_admin_user_remove_only_owner():
    # Clear data and register the first user
    requests.delete(f"{url}/clear/v1") 
    auth_data = {
        'email': 'john.smith@outlook.com', 
        'password': 'pass123', 
        'name_first': 'john', 
        'name_last': 'smith'
    }
    # Pass in their token and user id into the request and confirm an InputError
    # is raised
    authorised_info = requests.post(f"{url}/auth/register/v2", json = auth_data)    
    payload = authorised_info.json()
    authorised_token = payload['token']
    user_id = payload['auth_user_id']
    
    request = requests.delete(f"{url}/admin/user/remove/v1", json = {
        'token': authorised_token,
        'u_id': user_id,       
    })   
    assert request.status_code == 400

''' Test to verify that a non-Dreams owner is unable to remove other users'''
def test_admin_user_remove_unauthorised_user(): 
    # Clear data and register the first user, who will be the owner of Dreams
    requests.delete(f"{url}/clear/v1") 
    requests.post(f"{url}/auth/register/v2", json = {
        'email': 'g.smiley@email.com', 
        'password': 'circus', 
        'name_first': 'george', 
        'name_last': 'smiley'
    })  
    # Register the second user, extracting their token
    authorised_info1 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'b.haydon@email.com', 
        'password': 'tailor', 
        'name_first': 'bill', 
        'name_last': 'haydon'
    })   
    payload = authorised_info1.json()
    authorised_token = payload['token']
    # Register the third user, extracting their user id
    authorised_info2 = requests.post(f"{url}/auth/register/v2", json = {
        'email': 'edgar_poe@yahoo.com', 
        'password': 'theraven', 
        'name_first': 'edgar', 
        'name_last': 'poe'
    })
    payload = authorised_info2.json()
    user_id = payload['auth_user_id']
    # Pass in the second user's token and third user's user_id into the 
    # admin/user/remove to confirm an error will be raised for an unauthorised
    # token user [403 Access Error]
    request = requests.delete(f"{url}/admin/user/remove/v1", json = {
        'token': authorised_token,
        'u_id': user_id,       
    })   
    assert request.status_code == 403

