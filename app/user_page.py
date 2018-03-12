from app import app
from app.base_page_render import render_over_base_template
from app.current_user_info import UserInfo
from app.forms import NewPostForm, FollowForm
from app.followings_page import get_followings
from flask import request, redirect, url_for


def get_posts(username):
    return ["This post #1", "This is post #2"]


@app.route('/<username>', methods=["GET", "POST"])
def user_page(username):
    follow_form = FollowForm(username_to_follow=username)
    if request.method == "POST" and follow_form.validate():
        app.logger.debug("Send request to add following {}".format(username))
        return redirect(url_for("user_follow", username=username))
    current_user_username = UserInfo.get_current_user_username()
    form = NewPostForm()
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
                                     form=form)
