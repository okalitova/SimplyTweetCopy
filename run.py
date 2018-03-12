#!simply_tweet/bin/python3
from secret_keys import KeysAccessor
from app import app


if __name__ == "__main__":
    key_accessor = KeysAccessor()
    app.secret_key = key_accessor.get_app_secret_key()
    app.debug = True
    app.run(host="0.0.0.0", port=10443)
