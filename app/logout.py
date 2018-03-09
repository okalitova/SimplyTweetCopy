from app import app
from flask import redirect, url_for
from app.current_user_info import UserInfo


@app.route("/logout")
def logout():
    UserInfo.remove_current_user()
    return redirect(url_for("main_page"))
