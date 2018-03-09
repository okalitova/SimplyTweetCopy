from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import required, length

class NewPostForm(FlaskForm):
    text = TextField('text', validators=[required(), length(max=200)])
