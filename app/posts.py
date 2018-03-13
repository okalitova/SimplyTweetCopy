from app import app
from flask import redirect, url_for
from flask import request
from app.forms import NewPostForm
from app.current_user_info import UserInfo
from app.base_page_render import render_over_base_template


@app.route("/posts")
def posts():
    current_username = UserInfo.get_current_user_username()
    followings = UserInfo.get_followings(current_username)
    followings_posts = UserInfo.get_followings_posts(followings)
    return render_over_base_template("posts_page.html", followings_posts=followings_posts)


@app.route("/new_post", methods=["POST"])
def new_post():
    new_post_form = NewPostForm(request.form)
    if request.method == "POST" and new_post_form.validate_on_submit():
        if new_post_form.tweet.data:
            UserInfo.add_post(UserInfo.get_current_user_username(), new_post_form.text.data)
    return redirect(url_for("profile"))
