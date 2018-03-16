from flask import request, redirect, url_for, abort, session

from app import app
from app.base_template_render import render_over_base_template
from app.followings import get_followings, add_following, get_followings_ids
from app.forms import NewPostForm, FollowForm, SearchForm
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
                            userid=UserInfo.get_current_user_userid()))


@app.route('/<userid>', methods=["GET", "POST"])
def user_page(userid):
    # check that user exists
    if not UserInfo.check_user_exists(userid):
        abort(404)
    # if follow button was pressed
    follow_form = FollowForm(request.form)
    if request.method == "POST" and follow_form.validate_on_submit():
        if follow_form.follow.data:
            return redirect(url_for("new_following", userid=userid))
    # page filling
    new_post_form = NewPostForm(request.form)
    current_user_userid = UserInfo.get_current_user_userid()
    current_user_page = False
    if userid == current_user_userid:
        current_user_page = True
    posts_to_show = get_posts_to_show(userid)
    is_following = userid in get_followings_ids(current_user_userid)
    return render_over_base_template("user_page.html",
                                     userid=userid,
                                     current_user_page=current_user_page,
                                     is_following=is_following,
                                     posts=posts_to_show,
                                     follow_form=follow_form,
                                     new_post_form=new_post_form)


@app.route("/followings/<userid>")
def new_following(userid):
    add_following(UserInfo.get_current_user_userid(), userid)
    posts_to_show = get_posts_to_show(userid)
    email = UserInfo.get_user_email(userid)
    return render_over_base_template("user_page.html",
                                     userid=userid,
                                     current_user_page=False,
                                     is_following=True,
                                     posts=posts_to_show,
                                     email=email)


@app.route("/followings")
def followings():
    current_userid = UserInfo.get_current_user_userid()
    followings = get_followings(current_userid)
    return render_over_base_template("followings_page.html",
                                     followings=followings)


@app.route("/posts")
def posts():
    current_userid = UserInfo.get_current_user_userid()
    followings_ids = get_followings_ids(current_userid)
    followings_posts = get_followings_posts(followings_ids)
    return render_over_base_template("posts_page.html",
                                     followings_posts=followings_posts)


@app.route("/new_post", methods=["POST"])
def new_post():
    new_post_form = NewPostForm()
    if request.method == "POST" and new_post_form.validate_on_submit():
        if new_post_form.tweet.data:
            image = new_post_form.image.data
            add_post(UserInfo.get_current_user_userid(),
                     new_post_form.text.data, image)
    return redirect(url_for("profile"))

@app.route("/search", methods=["GET", "POST"])
def search():
    search_form = SearchForm()
    if request.method == "POST" and search_form.validate_on_submit():
        if search_form.search.data:
            email = search_form.text.data
            userid = UserInfo.get_userid(email)
            return redirect(url_for("user_page", userid=userid))
    return render_over_base_template("search_page.html",
                                     search_form=search_form)

@app.route("/accept_token", methods=["POST"])
def accept_token():
    idinfo = get_token_idinfo(request.form["idtoken"])
    validate_iss(idinfo)
    set_user_info(idinfo)
    return UserInfo.get_current_user_userid()
