from flask import redirect, url_for, request

from app import app
from app.base_template_render import render_over_base_template
from app.current_user_info import UserInfo
from app.forms import NewPostForm


@app.route("/posts")
def posts():
    current_username = UserInfo.get_current_user_username()
    followings = UserInfo.get_followings(current_username)
    followings_posts = UserInfo.get_followings_posts(followings)
    return render_over_base_template("posts_page.html",
                                     followings_posts=followings_posts)


@app.route("/new_post", methods=["POST"])
def new_post():
    new_post_form = NewPostForm()
    if request.method == "POST" and new_post_form.validate_on_submit():
        if new_post_form.tweet.data:
            image = new_post_form.image.data
            UserInfo.add_post(UserInfo.get_current_user_username(),
                              new_post_form.text.data, image)
    return redirect(url_for("profile"))
