from src.error import AccessError
from data import data

def check_valid_user(user_token):
    valid_user_id = False    
    print("----------------")
    print(user_token)
    print("----------------")
    print(data)
    user_id = user_token['auth_user_id']
    for user in data['users']:
        if user['auth_user_id'] == user_id :
            valid_user_id = True
            break
    if valid_user_id == False:
        raise AccessError("The auth_user_id input is not a valid id.")

