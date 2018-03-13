from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import TextField, SubmitField
from wtforms.validators import required, length


class NewPostForm(FlaskForm):
    text = TextField("text", validators=[required(), length(max=200)])
    image = FileField("image")
    tweet = SubmitField("tweet")


class FollowForm(FlaskForm):
    follow = SubmitField("follow")
