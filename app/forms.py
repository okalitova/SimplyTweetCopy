import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import TextField, SubmitField
from wtforms.validators import required, length

from app.user_info import UserInfo


class NewPostForm(FlaskForm):
    text = TextField("text", validators=[required(), length(max=200)])
    image = FileField("image")
    tweet = SubmitField("tweet")


class FollowForm(FlaskForm):
    follow = SubmitField("follow")


class SearchForm(FlaskForm):
    text = TextField("text", validators=[required(), length(max=500)])
    search = SubmitField("search")

    def is_email(self, email):
        regex = r"[^@]+@[^@]+\.[^@]+"
        return re.match(regex, email)

    def validate_on_submit(self):
        rv = FlaskForm.validate_on_submit(self)
        if not rv:
            return False

        email = self.text.data
        if not self.is_email(email):
            self.text.errors.append("Specify an email")
            return False
        if not UserInfo.check_user_exists(email):
            self.text.errors.append("User not found")
            return False
        return True
