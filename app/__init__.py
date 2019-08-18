from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

from . import database
database.init_app(app)

from app import views, models

login_manager = LoginManager()

login_manager.init_app(app)
app.secret_key = 'strong_session'
login_manager.session_protection = 'strong_session'
login_manager.login_view = 'login'
login_manager.login_message = 'please login'


@login_manager.user_loader
def load_user(user_id):
    return models.User.get_user(user_id)

#app.run(host='127.0.0.1', port=5000, debug=True)
