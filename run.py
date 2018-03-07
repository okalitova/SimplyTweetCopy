#!simply_tweet/bin/python3
from flask import Flask
from app import main_page
from app import user_page
from app import login_page
from app import followings_page
from app import app
from app import logout_page
from secret_keys import KeysAccessor

if __name__ == "__main__":
    key_accessor = KeysAccessor()
    app.secret_key = key_accessor.get_app_secret_key()
    app.debug = True
    app.run(host="0.0.0.0", port=10443)
