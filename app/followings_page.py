from app import app
from app.base_page_render import render_over_base_template
from app.current_user_info import UserInfo


def get_followings(username):
    return ["Following username 1",
            "Following username 2",
            "Following isername 3"]


@app.route("/followings")
def followings():
    current_username = UserInfo.get_current_user_username()
    followings = get_followings(current_username)
    return render_over_base_template("followings_page.html",
                                     followings=followings)
