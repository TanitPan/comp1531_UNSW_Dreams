import pytest
from src.channel import channel_invite_v1, users, channelData

def test_channel_invite():
    channel_invite_v1(1, 33, 2)
    # assert print(channelData) == {}
    assert channelData == {
        "33":{'name': 'Hayden',
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                },
                {
                    'u_id': 2,
                    'name_first': 'Mark',
                    'name_last': 'Smith',
                }
                
            ],
        }
    }

# test_channel_invite()