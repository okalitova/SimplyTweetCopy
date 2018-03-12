from app import app
from app.base_page_render import render_over_base_template
from app.current_user_info import UserInfo
from app.forms import NewPostForm, FollowForm
from app.followings_page import get_followings
from flask import request, redirect, url_for
from app.posts import get_posts


@app.route('/<username>', methods=["GET", "POST"])
def user_page(username):
    # if follow button was pressed
    follow_form = FollowForm(request.form)
    if request.method == "POST" and follow_form.validate_on_submit():
        if follow_form.follow.data:
            return redirect(url_for("user_follow", username=username))
    # if new post was tweeted
    new_post_form = NewPostForm(request.form)
#    if request.method == "POST" and new_post_form.validate_on_submit():
#        if new_post_form.tweet.data:
#            return redirect(url_for("new_post", text=new_post_form.data))
    current_user_username = UserInfo.get_current_user_username()
    current_user_page = False
    if username == current_user_username:
        current_user_page = True
    posts = get_posts(username)
    is_following = username in get_followings(current_user_username)
    return render_over_base_template("user_page.html",
                                     username=username,
                                     current_user_page=current_user_page,
                                     is_following=is_following,
                                     posts=posts,
                                     follow_form=follow_form,
                                     new_post_form=new_post_form)
