from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
from .model import db
from flask_wtf.csrf import CSRFProtect

import os

app = Flask(__name__)
app.config.from_object(Config)  # Load config first
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF globally
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

db.init_app(app)  # Initialize db after config
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