from flask import Flask
from flask_redis import FlaskRedis


app = Flask(__name__)
app.config.from_object('config')
redis_store = FlaskRedis(app)

from app import views
