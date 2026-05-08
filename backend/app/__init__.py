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


@login_manager.request_loader
def load_user_from_request(request):
    """Fallback when cross-site session cookies are not stored or sent (common on split SPA/API deploys)."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    raw = auth_header[7:].strip()
    if not raw:
        return None
    from .auth_token import verify_token
    from .model import User

    uid = verify_token(app.config.get("SECRET_KEY") or "", raw)
    if uid is None:
        return None
    try:
        return db.session.get(User, int(uid))
    except (TypeError, ValueError):
        return None


from . import views


@app.after_request
def _partition_cross_site_session_cookies(response):
    """iOS / Chrome: cross-site credentialed cookies often need SameSite=None + Partitioned (CHIPS)."""
    if str(app.config.get("SESSION_COOKIE_SAMESITE", "")).lower() != "none":
        return response
    try:
        lines = response.headers.getlist("Set-Cookie")
    except AttributeError:
        v = response.headers.get("Set-Cookie")
        lines = [v] if v else []
    if not lines:
        return response
    new_lines = []
    changed = False
    for line in lines:
        if not line:
            continue
        low = line.lower()
        if "partitioned" in low:
            new_lines.append(line)
        elif "samesite=none" in low:
            new_lines.append(line + "; Partitioned")
            changed = True
        else:
            new_lines.append(line)
    if changed and new_lines:
        response.headers.setlist("Set-Cookie", new_lines)
    return response