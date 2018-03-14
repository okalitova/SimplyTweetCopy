from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextField, SubmitField
from wtforms.validators import required, length


images = UploadSet('images', IMAGES)


class NewPostForm(FlaskForm):
    text = TextField("text", validators=[required(), length(max=200)])
    image = FileField("image",
                      validators=[FileAllowed(images, "Images only!")])
    tweet = SubmitField("tweet")


class FollowForm(FlaskForm):
    follow = SubmitField("follow")
