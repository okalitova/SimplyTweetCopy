class KeysAccessor():
    def __init__(self):
        self.__keys = {}
        with open("secret_keys", "r") as secret_keys:
            for line in secret_keys:
                line = line[:-1]
                [key_name, key] = line.split(' ')
                self.__keys[key_name] = key

    def get_app_secret_key(self):
        return self.__keys["app_secret_key"]

    def get_csrf_secret_key(self):
        return self.__keys["csrf_secret_key"]

    def get_google_client_id(self):
        return self.__keys["client_id"]
    
    def get_redis_password(self):
        return self.__keys["redis_password"]
