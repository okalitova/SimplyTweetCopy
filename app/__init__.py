from flask import Flask
from flask_redis import FlaskRedis


app = Flask(__name__)
app.config.from_object('config')
redis_store = FlaskRedis(app)

from app import main_page
from app import user_page
from app import followings_page
from app import app
from app import logout
from app import login
from app import profile
from app import posts

