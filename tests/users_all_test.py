import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.other import users_all_v1
from src.other import clear_v1
from src.helper import generate_token

@pytest.fixture
def register_user():
    clear_v1()
    auth_register_v2("batman@gmail.com", "123456", "bat", "man")
    user = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    token = user['token']
    return token

def test_valid_token(register_user):
    token = register_user
    res = users_all_v1(token)
    assert res == {
        'users': [
            {
                "auth_user_id": 0,
                "email": "batman@gmail.com",
                "name_first": "bat",
                "name_last": "man",
                "handle_str": "batman"              
            },
            {
                "auth_user_id": 1,
                "email": "johnsmith@gmail.com",
                "name_first": "john",
                "name_last": "smith",
                "handle_str": "johnsmith"    
            }
        ]
    }

def test_invalid_token(register_user):
    token = generate_token(42)
    with pytest.raises(AccessError):
        users_all_v1(token)
