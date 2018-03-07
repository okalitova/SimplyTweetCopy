from secret_keys import KeysAccessor


CSRF_ENABLED = True
key_accessor = KeysAccessor()
SECRET_KEY = key_accessor.get_csrf_secret_key()
