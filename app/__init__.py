from flask import Flask
from logging.config import dictConfig


app = Flask(__name__)
app.config.from_object('config')
