from app import app
from app.base_page_render import render_over_base_template
from app.current_user_info import UserInfo
from app import redis_store


def get_posts(username):
    return ["Post 1", "Post 2"]


@app.route("/followings/<username>")
def user_follow(username):
    app.logger.debug("Adds new following %s", username)
    add_following(UserInfo.get_current_user_username(), username)
    posts = get_posts(username)
    return render_over_base_template("user_page.html",
                                     username=username,
                                     current_user_page=False,
                                     is_following=True,
                                     posts=posts)


@app.route("/redis_followings")
def add_following(current_user, user_to_follow):
    current_followings = get_followings(current_user)
    current_followings.add(user_to_follow)
    redis_store.set(current_user, ";".join(current_followings))
    app.logger.debug("New following: %s", get_followings(current_user))


@app.route("/redis_followers")
def get_followings(username):
    user_followings_str = redis_store.get(username).decode("utf-8")
    user_followings = set(user_followings_str.split(";"))
    app.logger.debug("Followings: %s", user_followings)
    return user_followings


@app.route("/followings")
def followings():
    current_username = UserInfo.get_current_user_username()
    followings = get_followings(current_username)
    return render_over_base_template("followings_page.html",
                                     followings=followings)
