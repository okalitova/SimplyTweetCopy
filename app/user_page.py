from app import app
from app.base_page_render import render_over_base_template
from app.current_user_info import UserInfo
from app.forms import NewPostForm


def get_posts(username):
    return ["This post #1", "This is post #2"]


@app.route('/<username>', methods=["GET", "POST"])
def user_page(username):
    form = NewPostForm()
    current_user_page = False
    if username == UserInfo.get_current_user_username():
        current_user_page = True
    posts = get_posts(username)
    return render_over_base_template("user_page.html",
                                     current_user_page=current_user_page,
                                     posts=posts,
                                     form=form)
