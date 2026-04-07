from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
from .model import db


import os

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
upload_dir = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(upload_dir, exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db)


# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from .model import User
    return User.query.get(int(user_id))

from . import views