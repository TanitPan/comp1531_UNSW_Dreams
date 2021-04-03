'''This file consists of Python tests for admin_user_remove_v1 in admin.py'''

from src.admin import admin_user_remove_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.channel import channel_removeowner, channel_leave_v1, channel_messages_v2
from src.channels import channels_create_v2
from src.messages import message_send_v2
from src.other import clear_v1

def admin_user_remove_owners():
    clear_v1()
    user1 = auth_register_v2("smithj@outlook.com", "s1234", "john", "smith")
    token1 = user1['token']
    user2 = auth_register_v2("willpower@gmail.com", "tempest", "will", "power")
    user_id = user2['auth_user_id']
    token2 = user2['token']
    channel_id = channels_create_v2(token, "Channel_1", True)
    channel_join_v2(token2, channel_id['channel_id'])   
    admin_user_remove_v1(token1, user_id)
    with pytest.raises(AccessError):
        channel_removeowner(token, channel_id, u_id)

def admin_user_remove_members():
    clear_v1()
    user1 = auth_register_v2("j.smith@aol.com", "jjsmith", "john", "smith")
    token1 = user1['token']
    user2 = auth_register_v2("z1234567@unsw.com", "unsw", "unsw", "student")
    user_id = user2['auth_user_id']
    token2 = user2['token']
    channel_id = channels_create_v2(token1, "Channel_1", True)
    channel_join_v2(token2, channel_id['channel_id'])   
    admin_user_remove_v1(token2, user_id)
    with pytest.raises(AccessError):
        channel_leave_v1(token2, channel_id)

def admin_user_remove_messages():
    clear_v1()
    user1 = auth_register_v2("j.smith@aol.com", "jjsmith", "john", "smith")
    token1 = user1['token']
    user2 = auth_register_v2("z1234567@unsw.com", "unsw", "unsw", "student")
    user_id = user2['auth_user_id']
    token2 = user2['token']
    channel_id = channels_create_v2(token1, "Channel_1", True)
    message_send_v2(token1, "Channel_1", "Hello")
    admin_user_remove_v1(token1, user_id)
    messages = channel_messages_v2(token2, channel_id, 0)
    for message in messages['message']:
        assert message == {'Removed user'}
        
def test_admin_user_remove_only_owner():
    clear_v1()
    user = auth_register_v2("john.smith@gmail.com", "pass2021", "john", "smith")
    token = user['token']
    u_id = user['auth_user_id']
    with pytest.raises(InputError):
        admin_user_remove_v1(token, u_id)

def test_admin_user_remove_invalid_user():
    clear_v1()
    user = auth_register_v2("john.smith@yahoo.com", "passwd", "johnny", "smith")
    token = user['token']
    unauthorised_user_id = user['auth_user_id'] + 1
    with pytest.raises(InputError):
        admin_user_remove_v1(token, unauthorised_user_id)

def test_admin_user_remove_unauthorised_user(): 
    clear_v1()
    auth_register_v2("tom.smith@ymail.com", "tommo", "tom", "smith")
    user1 = auth_register_v2("john.smith@yahoo.com", "passwd", "johnny", "smith")
    invalid_token = user1['token']
    user2 = auth_register_v2("kevin2000@yahoo.com", "kevin1", "kevin", "jones")   
    user_id = user2['auth_user_id']
    with pytest.raises(AccessError):
        admin_user_remove_v1(invalid_token, user_id)


