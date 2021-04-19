import pytest
from src.error import InputError
from src.error import AccessError
from src.auth import auth_register_v2 as auth_register
from src.other import clear_v1 as clear
from src.channel import channel_details_v2 as channel_details
from src.channel import channel_invite_v2 as channel_invite
from src.channels import channels_create_v2 as channels_create
from src.helper import search_user_data
from data import data

# testing 1 channel 1 member
def test_channel_details_1():
    clear()

    auth_id1 = auth_register("johnsmith@gmail.com", "pass123", "John", "Smith")
    channel1 = channels_create(auth_id1['token'], "Channel1", True)

    assert channel_details(auth_id1['token'], channel1['channel_id']) == {
        'name': 'Channel1',
        'is_public' : True,
        'owner_members': [
            {
                'auth_user_id': auth_id1['auth_user_id'],
                'name_first': "John",
                'name_last': "Smith",
            }
        ],
        'all_members': [
            {
                'auth_user_id': auth_id1['auth_user_id'],
                'name_first': "John",
                'name_last': "Smith",
            }
        ]
    }


# testing 1 channel 1 member
def test_channel_details_2():
    clear()

    auth_id2 = auth_register("batman@gmail.com", "Alfred123", "Bat", "Man")
    auth_id3 = auth_register("aquabandit@gmail.com", "Rabbit1010", "Neo", "Amidis")
    channel2 = channels_create(auth_id2['token'], "Channel2", True)

    channel_invite(auth_id2['token'], channel2["channel_id"], auth_id3["auth_user_id"])

    assert channel_details(auth_id2['token'], channel2["channel_id"]) == {
        'name': 'Channel2',
        'is_public' : True,
        'owner_members': [
            {
                'auth_user_id': auth_id2['auth_user_id'],
                'name_first': "Bat",
                'name_last': "Man",
            }
        ],
        'all_members': [
            {
                'auth_user_id': auth_id2['auth_user_id'],
                'name_first': "Bat",
                'name_last': "Man",
            },
            {
                'auth_user_id': auth_id3['auth_user_id'],
                'name_first': "Neo",
                'name_last': "Amidis",
            }
        ]
    }

# Testing for input error
def test_channel_details_Input_Error():
    clear()
    auth_id1 = auth_register("johnsmith@gmail.com", "pass123", "John", "Smith")

    with pytest.raises(InputError):
        channel_details(auth_id1['token'], -1)

# Testing for access error
def test_channel_details_Access_Error():
    clear()
    auth_id1 = auth_register("wanokuroku@gmail.com", "Rockstar123", "Toru", "Darwin")
    auth_id2 = auth_register("bravecookie01@gmail.com", "devsistes", "Oscar", "Wood")

    channel3 = channels_create(auth_id1['token'], "Channel2", True)

    with pytest.raises(AccessError):
        channel_details(auth_id2['token'], channel3['channel_id'])
