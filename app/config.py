import os
from dotenv import load_dotenv

load_dotenv()  

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

    # Separate static frontend (e.g. two Render services): session cookie must be cross-site.
    _cross_site = os.environ.get("RENDER", "").lower() == "true" or os.environ.get(
        "USE_CROSS_SITE_SESSION", ""
    ).lower() in ("1", "true", "yes")
    if _cross_site:
        SESSION_COOKIE_SECURE = True
        SESSION_COOKIE_SAMESITE = "None"