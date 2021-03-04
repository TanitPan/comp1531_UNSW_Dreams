from src.channels import channels_create_v1, channels_list_v1
from src.channel import channel_join_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.other import clear_v1

# Test the function's return value to ensure it produces the right type (list)
def test_channels_listall_channeltype():
    clear_v1()
    authorised_token = auth_register_v1('smithjack@outlook.com', 'newpassword', 
                       'jack', 'smith')
    dict_channel = channels_list_v1(authorised_token)
    list_channel = dict_channel.values()
    for channel in list_channel:
        assert(isinstance(channel, list) == True)  

# Tests the elements inside the return value to make sure they are a dictionary     
def test_channels_listall_element_type():
    clear_v1()
    authorised_token = auth_register_v1('comp1531@student.com', 'student1531', 
                       'john', 'smith')
    dict_channel = channels_listall_v1(authorised_token)
    for element in dict_channel['channels']:
        assert(isinstance(element, dict) == True) 
        
# Tests the function when there are no input parameters and raises an InputError
def channels_list_empty_parameters():
    with pytest.raises(InputError):
        assert channels_list_v1()

# Tests that the channels created by an unauthorised user is not listed as 
def test_channels_listall_multiplechannel_length():
    clear_v1()
    authorised_token = auth_register_v1('user1@yahoo.com', 'password1234', 
                       'anne', 'smith')
    non-authorised_token = authorised_token + 1
    channel_id1 = channels_create_v1(authorised_token, 'Channel0', True)
    channel_id2 = channels_create_v1(non_authorised_token, 'Channel1', True)
    assert (len(channels_list_v1(authorised_token)) = 1


