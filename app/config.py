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