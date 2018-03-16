import json

from flask import session

from app import redis_store


class UserInfo():
    def is_logged_in():
        return "userid" in session

    def get_current_user_username():
        if UserInfo.is_logged_in():
            return session["username"]

    def get_current_user_email():
        if UserInfo.is_logged_in():
            return session["email"]

    def add_current_user(userid, email, username):
        if redis_store.get(username) is None:
            redis_store.set(username,
                            json.dumps({"followings": [], "posts": []}))
        session["userid"] = userid
        session["email"] = email
        session["username"] = username

    def remove_current_user():
        session.clear()

    def check_user_exists(username):
        return redis_store.get(username) is not None

    def get_user_info(username):
        user_info_str = redis_store.get(username).decode("utf-8")
        user_info_json = json.loads(user_info_str)
        return user_info_json
