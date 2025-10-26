import os
from dotenv import load_dotenv

load_dotenv()

class ProductionConfig:
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///plan_my_outings.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'plan-my-outings-secret-key-2025'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'plan-my-outings-jwt-key-2025'
    
    # Email Configuration - Use plain text values in production
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'outingplanmy@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'ckkymhmweqvrtrfz'
    
    # Super Admin Configuration - Use plain text values in production
    SUPER_ADMIN_USERNAME = os.environ.get('SUPER_ADMIN_USERNAME') or 'superadmin'
    SUPER_ADMIN_PASSWORD = os.environ.get('SUPER_ADMIN_PASSWORD') or 'SuperAdmin@2025'
    SUPER_ADMIN_EMAIL = os.environ.get('SUPER_ADMIN_EMAIL') or 'planmyouting@outlook.com'
    SUPER_ADMIN_FIRST_NAME = os.environ.get('SUPER_ADMIN_FIRST_NAME') or 'Super'
    SUPER_ADMIN_LAST_NAME = os.environ.get('SUPER_ADMIN_LAST_NAME') or 'Admin'
    
    # API Keys
    GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')