import pytest
from src.error import InputError
from src.auth import auth_register_v2
from src.user import user_profile_v2
from src.other import clear_v1

@pytest.fixture
def register_user():
    clear_v1()
    user = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    token = user['token']
    id = user['auth_user_id']
    return token, id

def test_valid_input(register_user):
    token, id = register_user
    res = user_profile_v2(token, id)
    assert res == {
        'user': {
            'auth_user_id': id,
            'email': 'johnsmith@gmail.com',
            'name_first' : 'john', 
	        'name_last' : 'smith', 
            'handle_str' : 'johnsmith', 
        }
    }

def test_invalid_uid(register_user):
    token, id = register_user
    id += 1
    with pytest.raises(InputError):
        user_profile_v2(token, id)
