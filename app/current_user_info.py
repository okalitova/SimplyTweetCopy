from flask import session


class UserInfo():
    def is_logged_in():
        return "username" in session

    def get_current_user_username():
        if UserInfo.is_logged_in():
            return session["username"]
        else:
            return ""
