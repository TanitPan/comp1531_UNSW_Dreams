"""
This file contains the tests for the implementation of users_stats function
"""

import pytest

from src.error import AccessError
from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_leave_v1
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.message import message_send_v2
from src.other import clear_v1, users_stats_v1
from src.helper import generate_token

@pytest.fixture
def register_user():
    clear_v1()
    user = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    auth_register_v2("batman@gmail.com", "123456", "bat", "man")
    token = user['token']
    return token

def test_valid_input(register_user):
    token = register_user
    res = users_stats_v1(token)

    assert res['channels_exist'][-1]['num_channels_exist'] == 0
    assert res['dms_exist'][-1]['num_dms_exist'] == 0
    assert res['messages_exist'][-1]['num_messages_exist'] == 0
    assert res['utilization_rate'] == 0

def test_channels_stats(register_user):
    token = register_user
    channel1 = channels_create_v2(token, "General", True)
    channel_id1 = channel1['channel_id']

    res = users_stats_v1(token)
    # make sure the channels_exist stat and utilization rate are updated
    assert res['channels_exist'][-1]['num_channels_exist'] == 1
    assert res['dms_exist'][-1]['num_dms_exist'] == 0
    assert res['messages_exist'][-1]['num_messages_exist'] == 0
    assert res['utilization_rate'] == 0.5

def test_dms_stats():
    clear_v1()
    user1 = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    token1 = user1['token']
    id1 = user1['auth_user_id']
    user2 = auth_register_v2("batman@gmail.com", "123456", "bat", "man")
    id2 = user2['auth_user_id']
    ids = [id1, id2]
    dm_create_v1(token1, ids)
    res = users_stats_v1(token1)
    assert res['channels_exist'][-1]['num_channels_exist'] == 0
    assert res['dms_exist'][-1]['num_dms_exist'] == 1
    assert res['messages_exist'][-1]['num_messages_exist'] == 0
    assert res['utilization_rate'] == 1

def test_messages_stats(register_user):
    token = register_user
    channel1 = channels_create_v2(token, "General", True)
    channel_id1 = channel1['channel_id']
    message_send_v2(token, channel_id1, "Hello world")

    res = users_stats_v1(token)
    assert res['channels_exist'][-1]['num_channels_exist'] == 1
    assert res['dms_exist'][-1]['num_dms_exist'] == 0
    assert res['messages_exist'][-1]['num_messages_exist'] == 1
    assert res['utilization_rate'] == 0.5

def test_invalid_token(register_user):
    token = generate_token(42)
    with pytest.raises(AccessError):
        users_stats_v1(token)