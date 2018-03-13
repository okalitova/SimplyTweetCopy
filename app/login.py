from flask import request
from google.oauth2 import id_token
from google.auth.transport import requests

from app import app
from app.base_template_render import render_over_base_template
from app.current_user_info import UserInfo
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
    # ID token is valid.
    # Gets the user's Google Account ID from the decoded token.
    userid = idinfo['sub']
    UserInfo.add_current_user(userid,
                              idinfo["email"],
                              idinfo["email"].split('@')[0])


@app.route("/accept_token", methods=["POST"])
def accept_token():
    idinfo = get_token_idinfo(request.form["idtoken"])
    validate_iss(idinfo)
    set_user_info(idinfo)
    return UserInfo.get_current_user_username()


@app.route("/login")
def login_page():
    return render_over_base_template("login_page.html")
