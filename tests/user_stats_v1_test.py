import pytest

from src.user import user_stats_v1
from src.error import AccessError
from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_leave_v1
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.message import message_send_v2
from src.other import clear_v1
from src.helper import generate_token

@pytest.fixture
def register_user():
    clear_v1()
    user = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    token = user['token']
    return token

def test_valid_input(register_user):
    token = register_user
    res = user_stats_v1(token)
    assert res['channels_joined'][-1]['num_channels_joined'] == 0
    assert res['dms_joined'][-1]['num_dms_joined'] == 0
    assert res['messages_sent'][-1]['num_messages_sent'] == 0
    assert res['involvement_rate'] == 0

def test_channels_stats(register_user):
    # Clear the data structure
    token1 = register_user
    user2 = auth_register_v2("batman@gmail.com", "123456", "bat", "man")
    token2 = user2["token"]

    channel1 = channels_create_v2(token1, "General", True)
    channel_id1 = channel1['channel_id']

    channel_join_v2(token2, channel_id1)

    # check that the user stats are updated accordingly
    res = user_stats_v1(token1)
    assert res['channels_joined'][-1]['num_channels_joined'] == 1
    assert res['dms_joined'][-1]['num_dms_joined'] == 0
    assert res['messages_sent'][-1]['num_messages_sent'] == 0
    assert res['involvement_rate'] == 0.5

    # Now the user leaves the channel, check that the stats are updated correctly
    channel_leave_v1(token1, channel_id1)

    res = user_stats_v1(token1)
    assert res['channels_joined'][-1]['num_channels_joined'] == 0
    assert res['dms_joined'][-1]['num_dms_joined'] == 0
    assert res['messages_sent'][-1]['num_messages_sent'] == 0
    assert res['involvement_rate'] == 0

def test_dm_stats():
    clear_v1()
    user1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    token1 = user1['token']
    id1 = user1['auth_user_id']
    user2 = auth_register_v2("batman@gmail.com", "123456", "bat", "man")
    id2 = user2['auth_user_id']
    ids = [id1, id2]
    dm_create_v1(token1, ids)
    res = user_stats_v1(token1)
    assert res['channels_joined'][-1]['num_channels_joined'] == 0
    assert res['dms_joined'][-1]['num_dms_joined'] == 1
    assert res['messages_sent'][-1]['num_messages_sent'] == 0
    assert res['involvement_rate'] == 0.5

def test_messages_stats(register_user):
    token = register_user
    channel1 = channels_create_v2(token, "General", True)
    channel_id1 = channel1['channel_id']
    message_send_v2(token, channel_id1, "Hello world")

    res = user_stats_v1(token)
    assert res['channels_joined'][-1]['num_channels_joined'] == 1
    assert res['dms_joined'][-1]['num_dms_joined'] == 0
    assert res['messages_sent'][-1]['num_messages_sent'] == 1
    assert res['involvement_rate'] == 1

def test_invalid_token(register_user):
    token = generate_token(42)
    with pytest.raises(AccessError):
        user_stats_v1(token)