from data import data 
import pytest
from src.channels import channels_create_v1, channels_listall_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1

# Test the type of the return value of channels_listall to ensure it produces a
# dictionary (Specs 6.1.1)
def test_channels_listall_type():
    # Clear the contents of the data file
    clear_v1()
    authorised_dict = auth_register_v1('janedoe@hotmail.com', '1234567', 
                       'jane', 'doe')        
    # Extracts the authorised user ID from the dictionary  
    authorised_token = authorised_dict['auth_user_id'] 
    channels_create_v1(authorised_token, 'Channel0', False)
    channel_dict = channels_listall_v1(authorised_token)
    #  Confirms that the type of the channel is a dictionary 
    assert(isinstance(channel_dict, dict) == True)  

# Tests the contents of the return value to ensure it meets the specs of being a
# list of dictionaries (Specs 6.1.1)        
def test_channels_listall_channeltype():
    clear_v1()
    authorised_dict = auth_register_v1('johnsmith@email.com', 'password', 
                       'john', 'smith')
    authorised_token = authorised_dict['auth_user_id'] 
    channels_create_v1(authorised_token, 'Channel1', True)
    channel_dict = channels_listall_v1(authorised_token)    
    # Firstly test if the value of the dict is of type list 
    assert(isinstance(channel_dict['channels'], list) == True)    
    # Tests each element in the value pair to ensurre it is a dictionarry
    for element in channel_dict['channels']:
        assert(isinstance(element, dict) == True) 
 
# Tests the function to make sure an AccessError arises when there's no 
# appropriate authorised user
def test_channels_listall_nonauthorised_user():
    clear_v1()
    authorised_dict = auth_register_v1('student@email.com', 'studunsw', 
                       'tom', 'student')
    authorised_token = authorised_dict['auth_user_id'] 
    channels_create_v1(authorised_token, 'Channel2', True)  
    # Created a non authorised token, which had a value one higher than the 
    # authorised token. 
    non_authorised_token = authorised_token + 1
    channel_dict = channels_listall_v1(authorised_token)  
    # Expected that an AccessError will be raised  
    with pytest.raises(AccessError):
        assert (channels_listall_v1(non_authorised_token))

# Tests the number of lists are added to the channel once the channels_create 
# function is called twice.  
def test_channels_listall_multiplechannel():
    clear_v1()
    # Created two auth_user_ids 
    authorised_dict1 = auth_register_v1('user1@yahoo.com', 'password1234', 
                       'anne', 'smith')
    authorised_token1 = authorised_dict1['auth_user_id']
    authorised_dict2 = auth_register_v1('user2@yahoo.com', 'password1234', 
                       'anna', 'smiths')
    authorised_token2 = authorised_dict2['auth_user_id'] 
    # Created a channel, each authorised by a different authorised users
    channels_create_v1(authorised_token1, 'Channel3', True)
    channels_create_v1(authorised_token2, 'Channel4', True)
    channel_dict = channels_listall_v1(authorised_token1)
    channel_value = channel_dict['channels']
    # Test that two channels have been recorded
    assert(len(channel_value) == 2)
    # Test for appropriate format
    assert (channel_dict == {'channels': [{'channel_id': 1, 'name': 'Channel3'}, 
            {'channel_id': 2, 'name': 'Channel4'}]})

