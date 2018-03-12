from secret_keys import KeysAccessor


# CSRF configuration
CSRF_ENABLED = True
key_accessor = KeysAccessor()
SECRET_KEY = key_accessor.get_csrf_secret_key()
# redis configuration
REDIS_URL = "redis://:{password}@localhost:6379/redis_followers".format(password=key_accessor.get_redis_password())
