from google.oauth2 import id_token
from google.auth.transport import requests

from app.user_info import UserInfo
from secret_keys import KeysAccessor


def get_token_idinfo(token):
    keys_accessor = KeysAccessor()
    idinfo = id_token.verify_oauth2_token(token,
                                          requests.Request(),
                                          keys_accessor.get_google_client_id())
    return idinfo


def validate_iss(idinfo):
    true_issuers = ['accounts.google.com', 'https://accounts.google.com']
    if idinfo['iss'] not in true_issuers:
        raise ValueError('Wrong issuer.')


def set_user_info(idinfo):
    UserInfo.add_current_user(idinfo["email"])
