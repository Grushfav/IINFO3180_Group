import os
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()


def _origin_netloc(origin):
    try:
        if not origin or not str(origin).startswith("http"):
            return ""
        return urlparse(origin).netloc.lower()
    except Exception:
        return ""  

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/static/uploads')
    
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
    _api_host = _origin_netloc(_render_public)
    # Static site on another host (e.g. frontend-*.onrender.com) + API on drift-dater: session must be
    # SameSite=None. Auto-detect from CORS vs RENDER_EXTERNAL_URL so deploys don't miss USE_CROSS_SITE_SESSION.
    _cross_site_auto = False
    if _on_render and _api_host:
        for _o in CORS_ORIGINS:
            h = _origin_netloc(_o)
            if not h or h.startswith("localhost") or h.startswith("127."):
                continue
            if h != _api_host:
                _cross_site_auto = True
                break
    _cross_site_explicit = os.environ.get("USE_CROSS_SITE_SESSION", "").lower() in ("1", "true", "yes")
    _same_site_only = os.environ.get("SAME_SITE_SESSION_ONLY", "").lower() in ("1", "true", "yes")
    _session_cross_site = not _same_site_only and (_cross_site_explicit or _cross_site_auto)
    if _on_render:
        SESSION_COOKIE_SECURE = True
        SESSION_COOKIE_SAMESITE = "None" if _session_cross_site else "Lax"