from app import app
from flask import render_template
from app.base_page_render import render_over_base_template

def get_current_username():
    return "Current username"


def get_followings(username):
    return ["Following username 1",
            "Following username 2",
            "Following isername 3"]


@app.route("/followings")
def followings():
    current_username = get_current_username()
    followings = get_followings(current_username)
    return render_over_base_template("followings_page.html",
                        followings=followings)
