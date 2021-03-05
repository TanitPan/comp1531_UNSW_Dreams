import pytest

from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from src.other import clear_v1

# Test the type of the return value of channels_create to ensure it produces a
# dictionary (Specs 6.1.1)
def test_channels_create_type():
    clear_v1()
    authorised_token = auth_register_v1('john.smith@gmail.com', 'password', 
                       'john', 'smith')
    channel_id =  channels_create_v1(authorised_token, "Channel0", True) 
    return_value = channel_id['channel_id']
    assert(return_value == 1)
    assert(isinstance(channel_id, dict) == True) 

# Test the key value of the return value (assuming it is a dictionary) to ensure 
# the channel_id is a integer value (Specs 6.1.1)
def test_channels_create_multiple_channels():
    clear_v1()
    authorised_token = auth_register_v1('rujanair4@yahoo.com', 'ruja1nair',
                       'ruja', 'nair')
    
    channel1_id = channels_create_v1(authorised_token, 'Channel1', True)

    # Created two channels, confirmed the channel_id was an integer and the 
    # format was correct
    channel1_key = channel1_id['channel_id']
    assert (isinstance(channel1_key, int) == True)
    assert (channel1_id == {'channel_id': 1})
    
    channel2_id = channels_create_v1(authorised_token, 'Channel2', True)
    channel2_key = channel2_id['channel_id']
    assert (isinstance(channel2_key, int) == True)
    assert (channel2_id == {'channel_id': 2})

# Test the complete structure of the return value to ensure the channel_id is 
# formatted properly  
def test_channels_create_firstvalue():
    clear_v1()
    authorised_token = auth_register_v1('annethomas@hotmail.com', 'pass1234', 
                       'anne', 'thomas')
    channel_id =  channels_create_v1(authorised_token, "Channel3", True) 
    assert (channel_id == {'channel_id': 1})

# Test the name value to see if the function raises an InputError for a name 
# with a length greater than 20 (Specs 6.2)
def test_channels_create_long_name():
    clear_v1()
    authorised_token = auth_register_v1('jane.doe@me.com', 'janedoe2021',
                       'jane', 'doe')
    with pytest.raises(InputError):   
        channels_create_v1(authorised_token, "longnamefortestchannel", True) 
    with pytest.raises(InputError):
        channels_create_v1(authorised_token, "123456789012345678901", False)
    with pytest.raises(InputError):
        channels_create_v1(authorised_token, "#!!!!!!!!!!!!!!!!!!!!#", True)
        
# Test multiple calls of channels_create_v1 to verify the dict has been updated
    clear_v1()
    authorised_token = auth_register_v1('comp1531student@email.com', 'comp15', 
                       'comp', 'student')
    # Tested each element separately
    channel_id1 =  channels_create_v1(authorised_token, "Channel4", True) 
    assert (channel_id1 == {'channel_id': 1})
    channel_id2 =  channels_create_v1(authorised_token, "Channel5", True) 
    assert (channel_id2 == {'channel_id': 2})
    channel_id3 =  channels_create_v1(authorised_token, "Channel6", True) 
    assert (channel_id3 == {'channel_id': 3})
    
