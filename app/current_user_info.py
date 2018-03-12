from flask import session
from app import app, redis_store
import json


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
            redis_store.set(username, json.dumps({"followings": [], "posts": []}))
        session["userid"] = userid
        session["email"] = email
        session["username"] = username
        app.logger.debug("New current user %s with email %s and userid %s",
                         session["username"],
                         session["email"],
                         session["userid"])

    def remove_current_user():
        session.clear()
        app.logger.debug("Current user removed")
