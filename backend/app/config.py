import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    # When deployed from backend/ as service root, static uploads live at backend/app/static/uploads.
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'backend/app/static/uploads')
    
    # Get DATABASE_URL from environment
    database_url = os.environ.get('DATABASE_URL', '')
    
    # Convert postgres:// to postgresql:// if needed (for compatibility)
    if database_url:
        database_url = database_url.replace('postgres://', 'postgresql://')
    
    SQLALCHEMY_DATABASE_URI = database_url or 'postgresql://shen@localhost/driftdater_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_SUPPORTS_CREDENTIALS = True
    # Credentials requests must use explicit origins (not '*'). Comma-separated, no path.
    # On Render: include your static site, e.g. https://your-frontend.onrender.com
    _cors_default = "http://localhost:5173,http://localhost:5174"
    _cors_raw = os.environ.get("CORS_ORIGINS", _cors_default)
    CORS_ORIGINS = [
        origin.strip()
        for origin in _cors_raw.split(",")
        if origin.strip()
    ]
    # Empty env (e.g. CORS_ORIGINS=) breaks flask-cors; fall back to local dev origins
    if not CORS_ORIGINS:
        CORS_ORIGINS = [
            o.strip() for o in _cors_default.split(",") if o.strip()
        ]

    # Same-origin SPA on Render: browser Origin is the API URL; include it so credentialed XHR is allowed.
    _render_public = (os.environ.get("RENDER_EXTERNAL_URL") or "").strip().rstrip("/")
    if _render_public and _render_public not in CORS_ORIGINS:
        CORS_ORIGINS = CORS_ORIGINS + [_render_public]

    # HTTPS cookies behind Render's proxy.
    _on_render = os.environ.get("RENDER", "").lower() == "true" or bool(_render_public)
    _same_site_only = os.environ.get("SAME_SITE_SESSION_ONLY", "").lower() in ("1", "true", "yes")
    if _on_render:
        SESSION_COOKIE_SECURE = True
        # Split SPA + API on different hosts (e.g. two *.onrender.com URLs) needs SameSite=None for
        # credentialed XHR/fetch; SameSite=Lax cookies are not sent on those cross-site requests, so
        # login returns 200 but the next GET /api/profile gets 401. Default to None on Render unless
        # SAME_SITE_SESSION_ONLY forces Lax (rare; same-host-only setups).
        if _same_site_only:
            SESSION_COOKIE_SAMESITE = "Lax"
        else:
            SESSION_COOKIE_SAMESITE = "None"