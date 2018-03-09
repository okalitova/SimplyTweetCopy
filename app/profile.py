from app import app
from flask import redirect, url_for
from app.current_user_info import UserInfo


@app.route("/profile")
def profile():
    return redirect(url_for("user_page", username=UserInfo.get_current_user_username()))
