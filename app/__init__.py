from flask import Flask
from flask_redis import FlaskRedis
from flask_uploads import configure_uploads, UploadSet, IMAGES


app = Flask(__name__)
app.config.from_object('config')
redis_store = FlaskRedis(app)
configure_uploads(app, UploadSet('images', IMAGES))

from app import views
