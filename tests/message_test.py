import pytest
from src.channel import *
from src.message import *
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.error import *
from src.other import clear_v1
import datetime
import time
from datetime import timezone

def test_message_send():
    clear_v1()

    u_1 = auth_register_v2('johnsmith@gmail.com', 'pass123456', 'John', 'Smith')
    channel_1 = channels_create_v2(u_1['token'], 'Channel1', True)
    message_id_1 = message_send_v2(u_1['token'], channel_1['channel_id'], "Hello")

    message_1 = channel_messages_v2(u_1['token'], channel_1['channel_id'], 0)

    assert message_1['messages'][0]['message_id'] == message_id_1['message_id']
    assert message_1['messages'][0]['auth_user_id'] == u_1['auth_user_id']
    assert message_1['messages'][0]['message'] == 'Hello'
    assert message_1['end'] == -1


def test_message_send_multiple():
    clear_v1()

    u_1 = auth_register_v2('janesmith@gmail.com', 'pass123456', 'Jane', 'Smith')
    channel_1 = channels_create_v2(u_1['token'], 'Channel2', True)
    message_id_1 = message_send_v2(u_1['token'], channel_1['channel_id'], "Hello")
    message_id_2 = message_send_v2(u_1['token'], channel_1['channel_id'], "World")
    message_id_3 = message_send_v2(u_1['token'], channel_1['channel_id'], "COMP1531")

    message_1 = channel_messages_v2(u_1['token'], channel_1['channel_id'], 0)
    
    assert message_1['messages'][0]['message_id'] == message_id_3['message_id']
    assert message_1['messages'][1]['message_id'] == message_id_2['message_id']
    assert message_1['messages'][2]['message_id'] == message_id_1['message_id']

    assert message_1['messages'][0]['auth_user_id'] == u_1['auth_user_id']
    assert message_1['messages'][1]['auth_user_id'] == u_1['auth_user_id']
    assert message_1['messages'][2]['auth_user_id'] == u_1['auth_user_id']

    assert message_1['messages'][0]['message'] == 'COMP1531'
    assert message_1['messages'][1]['message'] == 'World'
    assert message_1['messages'][2]['message'] == 'Hello'
    
    assert message_1['end'] == -1


def test_message_send_mult_users():
    clear_v1()

    u_1 = auth_register_v2('banesmith@gmail.com', 'pass123456', 'Bane', 'Smith')
    u_2 = auth_register_v2('manesmith@gmail.com', 'pass78910', 'Mane', 'Smith')

    channel_1 = channels_create_v2(u_1['token'], 'Channel3', True)
    channel_invite_v2(u_1['token'], channel_1['channel_id'], u_2['auth_user_id'])

    message_id_1 = message_send_v2(u_1['token'], channel_1['channel_id'], "Hello")
    message_id_2 = message_send_v2(u_2['token'], channel_1['channel_id'], "Hi, Thanks for adding me")
    message_id_3 = message_send_v2(u_1['token'], channel_1['channel_id'], "No Problem, Welcome to Channel1")
    message_id_4 = message_send_v2(u_2['token'], channel_1['channel_id'], "I am excited")

    message_1 = channel_messages_v2(u_1['token'], channel_1['channel_id'], 0)

    assert message_1['messages'][0]['message_id'] == message_id_4['message_id']
    assert message_1['messages'][1]['message_id'] == message_id_3['message_id']
    assert message_1['messages'][2]['message_id'] == message_id_2['message_id']
    assert message_1['messages'][3]['message_id'] == message_id_1['message_id']

    assert message_1['messages'][0]['auth_user_id'] == u_2['auth_user_id']
    assert message_1['messages'][1]['auth_user_id'] == u_1['auth_user_id']
    assert message_1['messages'][2]['auth_user_id'] == u_2['auth_user_id']
    assert message_1['messages'][3]['auth_user_id'] == u_1['auth_user_id']

    assert message_1['messages'][0]['message'] == 'I am excited'
    assert message_1['messages'][1]['message'] == 'No Problem, Welcome to Channel1'
    assert message_1['messages'][2]['message'] == 'Hi, Thanks for adding me'
    assert message_1['messages'][3]['message'] == 'Hello'

    assert message_1['end'] == -1

def test_message_send_unauthorized():
    clear_v1()

    u_1 = auth_register_v2('greensquare@gmail.com', 'gs12345@', 'Green', 'Square')
    u_2 = auth_register_v2('mascot@gmail.com', 'mascot12345@', 'Mascot', 'Mascot')
    channel_1 = channels_create_v2(u_1['token'], 'Channel4', True)

    with pytest.raises(AccessError):
        message_send_v2(u_2['token'], channel_1['channel_id'], "Hello")

def test_message_send_long_1000():
    clear_v1()

    u_1 = auth_register_v2('kingsford@gmail.com', 'kf12345@', 'Kings', 'Ford')
    channel_1 = channels_create_v2(u_1['token'], 'Channel5', True)

    msg = "A" * 1001

    with pytest.raises(InputError):
        message_send_v2(u_1['token'], channel_1['channel_id'], msg)

def test_message_delete():
    clear_v1()

    u_1 = auth_register_v2('batman@gmail.com', 'alfred123', 'Bruce', 'Wayne')
    channel_1 = channels_create_v2(u_1['token'], 'Channel6', True)
    message_id_1 = message_send_v2(u_1['token'], channel_1['channel_id'], "Hello")
    message_id_2 = message_send_v2(u_1['token'], channel_1['channel_id'], "World")
    message_id_3 = message_send_v2(u_1['token'], channel_1['channel_id'], "COMP1531")

    message_remove_v1(u_1['token'],message_id_2['message_id'])

    message_1 = channel_messages_v2(u_1['token'], channel_1['channel_id'], 0)
    
    assert message_1['messages'][0]['message_id'] == message_id_3['message_id']
    assert message_1['messages'][1]['message_id'] == message_id_1['message_id']

    assert message_1['messages'][0]['auth_user_id'] == u_1['auth_user_id']
    assert message_1['messages'][1]['auth_user_id'] == u_1['auth_user_id']

    assert message_1['messages'][0]['message'] == 'COMP1531'
    assert message_1['messages'][1]['message'] == 'Hello'

    assert message_1['end'] == -1

def test_message_edit():
    clear_v1()

    u_1 = auth_register_v2('alfred@gmail.com', 'batman123', 'alfred', 'alfred')
    channel_1 = channels_create_v2(u_1['token'], 'Channel7', True)
    message_id_1 = message_send_v2(u_1['token'], channel_1['channel_id'], "Hello")
    message_id_2 = message_send_v2(u_1['token'], channel_1['channel_id'], "World")
    
    message_edit_v1(u_1['token'],message_id_2['message_id'], "COMP1531")

    message_1 = channel_messages_v2(u_1['token'], channel_1['channel_id'], 0)
    
    assert message_1['messages'][0]['message_id'] == message_id_2['message_id']
    assert message_1['messages'][1]['message_id'] == message_id_1['message_id']

    assert message_1['messages'][0]['auth_user_id'] == u_1['auth_user_id']
    assert message_1['messages'][1]['auth_user_id'] == u_1['auth_user_id']

    assert message_1['messages'][0]['message'] == 'COMP1531'
    assert message_1['messages'][1]['message'] == 'Hello'

    assert message_1['end'] == -1

def test_message_pin():
    clear_v1()

    u_1 = auth_register_v2('sunnysideup@gmail.com', 'passw1234', 'Sunny', 'Up')
    channel_1 = channels_create_v2(u_1['token'], 'Channel8', True)
    message_id_1 = message_send_v2(u_1['token'], channel_1['channel_id'], "Hello")
    message_id_2 = message_send_v2(u_1['token'], channel_1['channel_id'], "World")
    message_id_3 = message_send_v2(u_1['token'], channel_1['channel_id'], "COMP1531")

    message_pin_v1(u_1['token'], message_id_1['message_id'])
    message_pin_v1(u_1['token'], message_id_3['message_id'])

    message_1 = channel_messages_v2(u_1['token'], channel_1['channel_id'], 0)

    assert message_1['messages'][0]['is_pinned'] == True
    assert message_1['messages'][1]['is_pinned'] == False
    assert message_1['messages'][2]['is_pinned'] == True

def test_message_unpin():
    clear_v1()

    u_1 = auth_register_v2('sunnysidedown@gmail.com', 'passw1234', 'Sunny', 'Down')
    channel_1 = channels_create_v2(u_1['token'], 'Channel9', True)

    message_id_1 = message_send_v2(u_1['token'], channel_1['channel_id'], "Hello")
    message_id_2 = message_send_v2(u_1['token'], channel_1['channel_id'], "World")
    message_id_3 = message_send_v2(u_1['token'], channel_1['channel_id'], "COMP1531")

    message_pin_v1(u_1['token'], message_id_1['message_id'])
    message_pin_v1(u_1['token'], message_id_3['message_id'])
    message_unpin_v1(u_1['token'], message_id_1['message_id'])
    message_pin_v1(u_1['token'], message_id_2['message_id'])
    message_unpin_v1(u_1['token'], message_id_3['message_id'])

    message_1 = channel_messages_v2(u_1['token'], channel_1['channel_id'], 0)

    assert message_1['messages'][0]['is_pinned'] == False
    assert message_1['messages'][1]['is_pinned'] == True
    assert message_1['messages'][2]['is_pinned'] == False

def test_message_sendlater():
    clear_v1()

    u_1 = auth_register_v2('sunnysideright@gmail.com', 'passw1234', 'Sunny', 'Right')
    channel_1 = channels_create_v2(u_1['token'], 'Channel10', True)

    now = datetime.datetime.now(timezone.utc)
    send_time = now + datetime.timedelta(0,3)

    message_timestamp = int(send_time.replace(tzinfo=timezone.utc).timestamp())

    message_sendlater_v1(u_1['token'], channel_1['channel_id'], "COMP1531", message_timestamp)
    
    message_send_v2(u_1['token'], channel_1['channel_id'], "Hello")

    message_1 = channel_messages_v2(u_1['token'], channel_1['channel_id'], 0)

    assert message_1['messages'][0]['message'] == "Hello"

    time.sleep(5)
    message_2 = channel_messages_v2(u_1['token'], channel_1['channel_id'], 0)
    assert message_2['messages'][0]['message'] == "COMP1531"
    






