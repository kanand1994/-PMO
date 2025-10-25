import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///plan_my_outings.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp-mail.outlook.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # API Keys
    GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    
    # Super Admin Configuration
    SUPER_ADMIN_EMAIL = os.environ.get('SUPER_ADMIN_EMAIL')
    SUPER_ADMIN_USERNAME = os.environ.get('SUPER_ADMIN_USERNAME')
    SUPER_ADMIN_PASSWORD = os.environ.get('SUPER_ADMIN_PASSWORD')
    SUPER_ADMIN_FIRST_NAME = os.environ.get('SUPER_ADMIN_FIRST_NAME')
    SUPER_ADMIN_LAST_NAME = os.environ.get('SUPER_ADMIN_LAST_NAME')
