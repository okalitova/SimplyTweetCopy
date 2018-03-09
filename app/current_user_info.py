from flask import session
from app import app


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
