from flask import request, redirect, url_for, abort

from app import app
from app.base_template_render import render_over_base_template
from app.followings import get_followings, add_following, get_followings_ids
from app.followings import delete_following
from app.forms import NewPostForm, DeletePostForm, FollowForm, UnfollowForm
from app.forms import SearchForm
from app.login import get_token_idinfo, validate_iss, set_user_info
from app.posts import get_posts_to_show, get_followings_posts
from app.posts import add_post, delete_post
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
    # page filling
    new_post_form = NewPostForm(request.form)
    current_user_userid = UserInfo.get_current_user_userid()
    current_user_page = False
    if userid == current_user_userid:
        current_user_page = True
    posts_to_show = get_posts_to_show(userid)
    is_following = userid in get_followings_ids(current_user_userid)
    follow_form = FollowForm()
    unfollow_form = UnfollowForm()
    delete_post_form = DeletePostForm()
    return render_over_base_template("user_page.html",
                                     userid=userid,
                                     current_user_page=current_user_page,
                                     is_following=is_following,
                                     posts=posts_to_show,
                                     follow_form=follow_form,
                                     unfollow_form=unfollow_form,
                                     new_post_form=new_post_form,
                                     delete_post_form=delete_post_form)


@app.route("/followings/new/<userid>", methods=["POST"])
def following_new(userid):
    follow_form = FollowForm()
    if follow_form.validate_on_submit():
        add_following(UserInfo.get_current_user_userid(), userid)
        posts_to_show = get_posts_to_show(userid)
        unfollow_form = UnfollowForm()
        return render_over_base_template("user_page.html",
                                         userid=userid,
                                         current_user_page=False,
                                         is_following=True,
                                         posts=posts_to_show,
                                         unfollow_form=unfollow_form)
    else:
        follow_form = FollowForm()
        return render_over_base_template("user_page.html",
                                         userid=userid,
                                         current_user_page=False,
                                         is_following=False,
                                         follow_form=follow_form)


@app.route("/followings/delete/<userid>", methods=["POST"])
def followings_delete(userid):
    unfollow_form = UnfollowForm()
    if unfollow_form.validate_on_submit():
        delete_following(UserInfo.get_current_user_userid(), userid)
        follow_form = FollowForm()
        return render_over_base_template("user_page.html",
                                         userid=userid,
                                         current_user_page=False,
                                         is_following=False,
                                         follow_form=follow_form)
    else:
        posts_to_show = get_posts_to_show(userid)
        unfollow_form = UnfollowForm()
        return render_over_base_template("user_page.html",
                                         userid=userid,
                                         current_user_page=False,
                                         is_following=True,
                                         posts=posts_to_show,
                                         unfollow_form=unfollow_form)


@app.route("/delete_post/<timestamp>", methods=["POST"])
def post_delete(timestamp):
    delete_post_form = DeletePostForm()
    if delete_post_form.validate_on_submit():
        userid = UserInfo.get_current_user_userid()
        delete_post(userid, timestamp)
        return redirect(url_for("profile"))
    else:
        return ""


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
    current_user_userid = UserInfo.get_current_user_userid()
    if request.method == "POST" and new_post_form.validate_on_submit():
        if new_post_form.tweet.data:
            image = new_post_form.image.data
            add_post(UserInfo.get_current_user_userid(),
                     new_post_form.text.data, image)
            return redirect(url_for("user_page",
                                    userid=current_user_userid))
    posts_to_show = get_posts_to_show(current_user_userid)
    delete_post_form = DeletePostForm()
    return render_over_base_template("user_page.html",
                                     userid=current_user_userid,
                                     current_user_page=True,
                                     posts=posts_to_show,
                                     new_post_form=new_post_form,
                                     delete_post_form=delete_post_form)


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
