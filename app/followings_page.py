from app import app
from app.base_template_render import render_over_base_template
from app.current_user_info import UserInfo


@app.route("/followings/<username>")
def user_follow(username):
    UserInfo.add_following(UserInfo.get_current_user_username(), username)
    posts = UserInfo.get_posts(username)
    return render_over_base_template("user_page.html",
                                     username=username,
                                     current_user_page=False,
                                     is_following=True,
                                     posts=posts)


@app.route("/followings")
def followings():
    current_username = UserInfo.get_current_user_username()
    followings = UserInfo.get_followings(current_username)
    return render_over_base_template("followings_page.html",
                                     followings=followings)
