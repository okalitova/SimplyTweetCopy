from app import app
from flask import redirect, url_for
from flask import request
from app.forms import NewPostForm
from app import redis_store
from app.current_user_info import UserInfo
import json
import time


@app.route("/new_post", methods=["POST"])
def new_post():
    new_post_form = NewPostForm(request.form)
    if request.method == "POST" and new_post_form.validate_on_submit():
        if new_post_form.tweet.data:
            add_post(UserInfo.get_current_user_username(), new_post_form.text.data)
    return redirect(url_for("profile"))


def add_post(username, text):
    user_info_json = get_user_info(username)
    user_info_json["posts"].append({"text": text, "timestamp": time.time()})
    app.logger.debug("New user info: %s", user_info_json)
    user_info_str = json.dumps(user_info_json)
    redis_store.set(username, user_info_str)
    app.logger.debug("New following: %s", get_posts(username))


def get_user_info(username):
    user_info_str = redis_store.get(username).decode("utf-8")
    app.logger.debug("User info str: %s", user_info_str)
    user_info_json = json.loads(user_info_str)
    app.logger.debug("User info json: %s", user_info_json)
    return user_info_json


def get_posts(username):
    user_info_json = get_user_info(username)
    app.logger.debug("User info json: %s", user_info_json)
    user_posts = user_info_json["posts"]
    app.logger.debug("Followings: %s", user_posts)
    posts_text = []
    for post in user_posts[::-1]:
        posts_text.append(post["text"])
    return posts_text
