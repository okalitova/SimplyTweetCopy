from datetime import datetime

from flask import request, redirect, url_for, abort

from app import app
from app.base_template_render import render_over_base_template
from app.current_user_info import UserInfo
from app.images import ImagesStorage
from app.forms import NewPostForm, FollowForm


def get_posts_to_show(posts):
    posts_to_show = []
    for post in posts:
        post["time"] = datetime.fromtimestamp(post["timestamp"])\
                                    .strftime('%Y-%m-%d %H:%M:%S')
        if "image_key" in post and post["image_key"] is not None:
            images_storage = ImagesStorage()
            image_link = images_storage.get_image(post["image_key"])
            post["image_link"] = image_link
        posts_to_show.append(post)
    return posts_to_show


@app.route('/<username>', methods=["GET", "POST"])
def user_page(username):
    # check that user exists
    if not UserInfo.check_user_exists(username):
        abort(404)
    # if follow button was pressed
    follow_form = FollowForm(request.form)
    if request.method == "POST" and follow_form.validate_on_submit():
        if follow_form.follow.data:
            return redirect(url_for("user_follow", username=username))
    # page filling
    new_post_form = NewPostForm(request.form)
    current_user_username = UserInfo.get_current_user_username()
    current_user_page = False
    if username == current_user_username:
        current_user_page = True
    posts = UserInfo.get_posts(username)
    posts_to_show = get_posts_to_show(posts)
    is_following = username in UserInfo.get_followings(current_user_username)
    return render_over_base_template("user_page.html",
                                     username=username,
                                     current_user_page=current_user_page,
                                     is_following=is_following,
                                     posts=posts_to_show,
                                     follow_form=follow_form,
                                     new_post_form=new_post_form)
