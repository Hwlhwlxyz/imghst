from flask import Flask
app = Flask(__name__)

from . import database
database.init_app(app)

from app import views


