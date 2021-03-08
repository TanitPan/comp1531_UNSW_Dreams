import pytest
from src.error import InputError
from src.error import AccessError
from src.auth import auth_register_v1
from src.other import clear_v1 as clear
from src.channel import channel_details_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1
from data import data

# testing 1 channel 1 member
def test_channel_details_1():
    clear()

    auth_id1 = auth_register_v1("johnsmith@gmail.com", "pass123", "John", "Smith")
    channel1 = channels_create_v1(auth_id1['auth_user_id'], "Channel1", True)

    assert channel_details_v1(auth_id1['auth_user_id'], channel1["channel_id"]) == {
        'name': 'Channel1',
        'owner_members': [
            {
                'auth_user_id': auth_id1['auth_user_id'],
                'name_first': "John",
                'name_last': "Smith",
                'email' : "johnsmith@gmail.com",
                'handle_str': 'johnsmith'
            }
        ],
        'all_members': [
            {
                'auth_user_id': auth_id1['auth_user_id'],
                'name_first': "John",
                'name_last': "Smith",
                'email' : "johnsmith@gmail.com",
                'handle_str': 'johnsmith'
            }
        ]
    }

# testing 1 channel 1 member
def test_channel_details_2():
    clear()

    auth_id2 = auth_register_v1("batman@gmail.com", "Alfred123", "Bat", "Man")
    auth_id3 = auth_register_v1("aquabandit@gmail.com", "Rabbit1010", "Neo", "Amidis")
    channel2 = channels_create_v1(auth_id2['auth_user_id'], "Channel2", True)

    channel_invite_v1(auth_id2["auth_user_id"], channel2["channel_id"], auth_id3["auth_user_id"])

    assert channel_details_v1(auth_id2['auth_user_id'], channel2["channel_id"]) == {
        'name': 'Channel2',
        'owner_members': [
            {
                'auth_user_id': auth_id2['auth_user_id'],
                'name_first': "Bat",
                'name_last': "Man",
                'email' : "batman@gmail.com",
                'handle_str': 'batman'
            }
        ],
        'all_members': [
            {
                'auth_user_id': auth_id2['auth_user_id'],
                'name_first': "Bat",
                'name_last': "Man",
                'email' : "batman@gmail.com",
                'handle_str': 'batman'
            },
            {
                'auth_user_id': auth_id3['auth_user_id'],
                'name_first': "Neo",
                'name_last': "Amidis",
                'email' : "aquabandit@gmail.com",
                'handle_str': 'neoamidis'
            }
        ]
    }

# Testing for input error
def test_channel_details_Input_Error():
    clear()
    auth_id1 = auth_register_v1("johnsmith@gmail.com", "pass123", "John", "Smith")

    with pytest.raises(InputError):
        channel_details_v1(auth_id1['auth_user_id'], -1)

# Testing for access error
def test_channel_details_Access_Error():
    clear()
    auth_id1 = auth_register_v1("wanokuroku@gmail.com", "Rockstar123", "Toru", "Darwin")
    auth_id2 = auth_register_v1("bravecookie01@gmail.com", "devsistes", "Oscar", "Wood")

    channel3 = channels_create_v1(auth_id1['auth_user_id'], "Channel2", True)

    with pytest.raises(AccessError):
        channel_details_v1(auth_id2['auth_user_id'], channel3['channel_id'])


