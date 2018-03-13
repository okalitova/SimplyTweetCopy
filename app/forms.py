from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from wtforms.validators import required, length
from flask_wtf.file import FileField


class NewPostForm(FlaskForm):
    text = TextField("text", validators=[required(), length(max=200)])
    image = FileField("image")
    tweet = SubmitField("tweet")


class FollowForm(FlaskForm):
    follow = SubmitField("follow")
