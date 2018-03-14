#!simply_tweet/bin/python3
from secret_keys import KeysAccessor
from app import app as application


if __name__ == "__main__":
    key_accessor = KeysAccessor()
    application.secret_key = key_accessor.get_app_secret_key()
    application.run()
