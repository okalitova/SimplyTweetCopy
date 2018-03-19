from flask import render_template

from app.forms import DeletePostForm, NewPostForm, FollowForm, UnfollowForm
from app.posts import get_posts_to_show
from app.user_info import UserInfo
from secret_keys import KeysAccessor


def render_over_base_template(*args, **kwargs):
    keys_accessor = KeysAccessor()
    google_client_id = keys_accessor.get_google_client_id()
    print(google_client_id)
    return render_template(*args,
                           **kwargs,
                           GOOGLE_CLIENT_ID=google_client_id)


def render_current_user_page(new_post_form=None):
    current_user_userid = UserInfo.get_current_user_userid()
    posts_to_show = get_posts_to_show(current_user_userid)
    delete_post_form = DeletePostForm()
    if new_post_form is None:
        new_post_form = NewPostForm()
    return render_over_base_template("user_page.html",
                                     userid=current_user_userid,
                                     current_user_page=True,
                                     posts=posts_to_show,
                                     new_post_form=new_post_form,
                                     delete_post_form=delete_post_form)


def render_following_user_page(userid):
    posts_to_show = get_posts_to_show(userid)
    unfollow_form = UnfollowForm()
    return render_over_base_template("user_page.html",
                                     userid=userid,
                                     current_user_page=False,
                                     is_following=True,
                                     posts=posts_to_show,
                                     unfollow_form=unfollow_form)


def render_not_following_user_page(userid):
    follow_form = FollowForm()
    return render_over_base_template("user_page.html",
                                     userid=userid,
                                     current_user_page=False,
                                     is_following=False,
                                     follow_form=follow_form)
