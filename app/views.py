from flask import request, redirect, url_for, abort

from app import app
from app.base_template_render import render_over_base_template
from app.followings import get_followings, add_following
from app.forms import NewPostForm, FollowForm
from app.login import get_token_idinfo, validate_iss, set_user_info
from app.posts import get_posts_to_show, get_followings_posts, add_post
from app.user_info import UserInfo


@app.route("/")
def main_page():
    return render_over_base_template("main_page.html")


@app.route("/login")
def login_page():
    return render_over_base_template("login_page.html")


@app.route("/logout")
def logout():
    UserInfo.remove_current_user()
    return redirect(url_for("main_page"))


@app.route("/profile")
def profile():
    return redirect(url_for("user_page",
                            username=UserInfo.get_current_user_username()))


@app.route('/<username>', methods=["GET", "POST"])
def user_page(username):
    # check that user exists
    if not UserInfo.check_user_exists(username):
        abort(404)
    # if follow button was pressed
    follow_form = FollowForm(request.form)
    if request.method == "POST" and follow_form.validate_on_submit():
        if follow_form.follow.data:
            return redirect(url_for("new_following", username=username))
    # page filling
    new_post_form = NewPostForm(request.form)
    current_user_username = UserInfo.get_current_user_username()
    current_user_page = False
    if username == current_user_username:
        current_user_page = True
    posts_to_show = get_posts_to_show(username)
    is_following = username in get_followings(current_user_username)
    return render_over_base_template("user_page.html",
                                     username=username,
                                     current_user_page=current_user_page,
                                     is_following=is_following,
                                     posts=posts_to_show,
                                     follow_form=follow_form,
                                     new_post_form=new_post_form)


@app.route("/followings/<username>")
def new_following(username):
    add_following(UserInfo.get_current_user_username(), username)
    posts_to_show = get_posts_to_show(username)
    return render_over_base_template("user_page.html",
                                     username=username,
                                     current_user_page=False,
                                     is_following=True,
                                     posts=posts_to_show)


@app.route("/followings")
def followings():
    current_username = UserInfo.get_current_user_username()
    followings = get_followings(current_username)
    return render_over_base_template("followings_page.html",
                                     followings=followings)


@app.route("/posts")
def posts():
    current_username = UserInfo.get_current_user_username()
    followings = get_followings(current_username)
    followings_posts = get_followings_posts(followings)
    return render_over_base_template("posts_page.html",
                                     followings_posts=followings_posts)


@app.route("/new_post", methods=["POST"])
def new_post():
    new_post_form = NewPostForm()
    if request.method == "POST" and new_post_form.validate_on_submit():
        if new_post_form.tweet.data:
            image = new_post_form.image.data
            add_post(UserInfo.get_current_user_username(),
                     new_post_form.text.data, image)
    current_user_username = UserInfo.get_current_user_username()
    posts_to_show = get_posts_to_show(current_user_username)
    return render_over_base_template("user_page.html",
                                     username=current_user_username,
                                     current_user_page=True,
                                     posts=posts_to_show,
                                     new_post_form=new_post_form)


@app.route("/accept_token", methods=["POST"])
def accept_token():
    idinfo = get_token_idinfo(request.form["idtoken"])
    validate_iss(idinfo)
    set_user_info(idinfo)
    return UserInfo.get_current_user_username()
