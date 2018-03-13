from app import app
from app.base_page_render import render_over_base_template
from app.current_user_info import UserInfo
from app.forms import NewPostForm, FollowForm
from flask import request, redirect, url_for, abort


@app.route('/<username>', methods=["GET", "POST"])
def user_page(username):
    # check that user exists
    if not UserInfo.check_user_exists(username):
        app.logger.debug("App is about to abort")
        abort(404)
    app.logger.debug("User exists? Answer: %s", UserInfo.check_user_exists(username))
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
    is_following = username in UserInfo.get_followings(current_user_username)
    return render_over_base_template("user_page.html",
                                     username=username,
                                     current_user_page=current_user_page,
                                     is_following=is_following,
                                     posts=posts,
                                     follow_form=follow_form,
                                     new_post_form=new_post_form)
