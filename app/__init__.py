from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
from .db import db
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['WTF_CSRF_ENABLED'] = False
# Explicit allowlist when withCredentials is used. OPTIONS preflight must succeed.
CORS(
    app,
    supports_credentials=True,
    origins=app.config["CORS_ORIGINS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
# Outermost: fix X-Forwarded-* from Render before Flask / CORS see the request.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
# API-only app: do not redirect to login_view (that would GET /api/login, which is POST-only → 405).
login_manager.login_view = None


@login_manager.unauthorized_handler
def _unauthorized():
    return jsonify(error="Authentication required"), 401


@login_manager.user_loader
def load_user(user_id):
    from .model import User
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None

from . import views