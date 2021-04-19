"""
This file contains the tests for the implementation of user_profile_uploadphoto
"""

import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.user import user_profile_v2, user_profile_uploadphoto_v1
from src.other import clear_v1
from src.helper import generate_token
from src import config

@pytest.fixture
def register_user():
    clear_v1()
    user = auth_register_v2("johnsmith@gmail.com", "123456", "john", "smith")
    return user

def test_invalid_token():
    clear_v1()
    url_path = config.url
    token = generate_token(42)
    cute_cat_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Khaomanee_cat.jpg/1200px-Khaomanee_cat.jpg"
    with pytest.raises(AccessError):
        user_profile_uploadphoto_v1(token, url_path, cute_cat_url, 50, 50, 1000, 1000)

def test_valid_input(register_user):
    user = register_user
    token = user['token']
    id = user['auth_user_id']
    url_path = config.url
    cute_cat_url = "https://thumbs.dreamstime.com/b/scottish-fold-cat-14577759.jpg"
    res = user_profile_uploadphoto_v1(token, url_path, cute_cat_url, 50, 50, 500, 500)
    assert res == {}
    profile = user_profile_v2(token, id)
    assert profile['user']['profile_img_url'] != config.url + 'src/static/default.jpg'

def test_invalid_inputs(register_user):
    user = register_user
    token = user['token']
    url_path = config.url
    fake_url = "not_a_url"
    # test invalid url
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url_path, fake_url, 50, 50, 1000, 1000)
    # test invalid cropping dimensions
    scottish_fold_kitty = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Scottish_fold_cat.jpg/220px-Scottish_fold_cat.jpg"
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url_path, scottish_fold_kitty, 50, 50, 5000, 5000)
    # test inversed cropping dimensions
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url_path, scottish_fold_kitty, 5000, 5000, 50, 50)
    # test non-jpg file
    png_file_cat = "https://icatcare.org/app/uploads/2018/09/Scottish-fold-2.png"
    # test invalid url
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(token, url_path, png_file_cat, 50, 50, 800, 800)