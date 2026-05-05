"""
WSGI entry for Gunicorn on Render.

Use start command:
  gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 wsgi:application
"""
from app import app as application

__all__ = ["application"]
