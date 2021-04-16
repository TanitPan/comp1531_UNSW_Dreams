from data import data
from src.helper import valid_token, update_user_stats, save_data

def message_send_v2(token, channel_id, message):
    valid_token(token) # raises AccessError on invalid token
    #update the user stats
    update_user_stats(token, 'messages_sent', 1)
    # save the data persistently
    save_data(data)
    return {
        'message_id': 1,
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }