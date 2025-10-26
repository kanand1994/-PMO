import os
from dotenv import load_dotenv

load_dotenv()

# Import encryption utilities at module level
try:
    import cryptography
    from encryption_utils import decrypt_env_password
    ENCRYPTION_AVAILABLE = True
except ImportError as e:
    # Silently handle missing encryption in development reloader
    ENCRYPTION_AVAILABLE = False
    decrypt_env_password = None

def _decrypt_if_needed(value):
    """Helper function to decrypt values if they are encrypted"""
    if value and value.startswith('ENC:') and ENCRYPTION_AVAILABLE:
        try:
            return decrypt_env_password(value)
        except Exception as e:
            print(f"Warning: Could not decrypt value: {e}")
            return None
    return value

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///plan_my_outings.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    
    # Decrypt email credentials
    MAIL_USERNAME = _decrypt_if_needed(os.environ.get('MAIL_USERNAME'))
    MAIL_PASSWORD = _decrypt_if_needed(os.environ.get('MAIL_PASSWORD'))
    
    # API Keys
    GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    
    # Super Admin Configuration (Encrypted)
    SUPER_ADMIN_EMAIL = _decrypt_if_needed(os.environ.get('SUPER_ADMIN_EMAIL'))
    SUPER_ADMIN_USERNAME = _decrypt_if_needed(os.environ.get('SUPER_ADMIN_USERNAME'))
    SUPER_ADMIN_PASSWORD = _decrypt_if_needed(os.environ.get('SUPER_ADMIN_PASSWORD'))
    SUPER_ADMIN_FIRST_NAME = _decrypt_if_needed(os.environ.get('SUPER_ADMIN_FIRST_NAME'))
    SUPER_ADMIN_LAST_NAME = _decrypt_if_needed(os.environ.get('SUPER_ADMIN_LAST_NAME'))
