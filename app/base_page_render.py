from flask import render_template
from app.current_user_info import UserInfo


def render_over_base_template(*args, **kwargs):
    return render_template(*args,
                           **kwargs,
                           logged_in=UserInfo.is_logged_in(),
                           username=UserInfo.get_current_user_username())
