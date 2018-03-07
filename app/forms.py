from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import required, length

class NewPostForm(Form):
    text = TextField('text', validators=[required(), length(max=200)])
