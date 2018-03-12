from app import app
from app.base_page_render import render_over_base_template
from app.current_user_info import UserInfo
from app import redis_store
import json


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
    user_info_json = get_user_info(current_user)
    user_info_json["followings"].append(user_to_follow)
    app.logger.debug("New user info: %s", user_info_json)
    user_info_str = json.dumps(user_info_json)
    redis_store.set(current_user, user_info_str)
    app.logger.debug("New following: %s", get_followings(current_user))


@app.route("/redis_followers")
def get_user_info(username):
    user_info_str = redis_store.get(username).decode("utf-8")
    app.logger.debug("User info str: %s", user_info_str)
    user_info_json = json.loads(user_info_str)
    app.logger.debug("User info json: %s", user_info_json)
    return user_info_json


@app.route("/redis_followers")
def get_followings(username):
    user_info_json = get_user_info(username)
    app.logger.debug("User info json: %s", user_info_json)
    user_followings = set(user_info_json["followings"])
    app.logger.debug("Followings: %s", user_followings)
    return user_followings


@app.route("/followings")
def followings():
    current_username = UserInfo.get_current_user_username()
    followings = get_followings(current_username)
    return render_over_base_template("followings_page.html",
                                     followings=followings)
