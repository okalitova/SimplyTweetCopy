import json
import uuid

from flask import session

from app import redis_store


class UserInfo():
    def is_logged_in():
        return "userid" in session

    def get_current_user_userid():
        if UserInfo.is_logged_in():
            return session["userid"]

    def get_current_user_email():
        if UserInfo.is_logged_in():
            return session["email"]

    def add_current_user(email):
        if redis_store.get(email) is None:
            new_userid = uuid.uuid1().hex
            redis_store.set(new_userid,
                            json.dumps({"email": email,
                                        "followings": [],
                                        "posts": []}))
            redis_store.set(email, new_userid)
            session["userid"] = new_userid
        else:
            userid = UserInfo.get_userid(email)
            session["userid"] = userid
        session["email"] = email

    def remove_current_user():
        session.clear()

    def check_user_exists(userid):
        return redis_store.get(userid) is not None

    def get_userid(email):
        return redis_store.get(email).decode("utf-8")

    def get_user_info(userid):
        user_info_str = redis_store.get(userid).decode("utf-8")
        user_info_json = json.loads(user_info_str)
        return user_info_json

    def get_user_email(userid):
        return UserInfo.get_user_info(userid)["email"]
