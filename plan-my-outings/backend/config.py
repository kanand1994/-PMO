import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///plan_my_outings.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.office365.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    
    # Decrypt email password if encrypted
    @staticmethod
    def _decrypt_password():
        password = os.environ.get('MAIL_PASSWORD')
        if password and password.startswith('ENC:'):
            try:
                from encryption_utils import decrypt_env_password
                return decrypt_env_password(password)
            except Exception as e:
                print(f"Error decrypting email password: {e}")
                return None
        return password
    
    MAIL_PASSWORD = _decrypt_password()
    
    # API Keys
    GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    
    # Super Admin Configuration (Encrypted)
    @staticmethod
    def _decrypt_admin_field(field_name):
        value = os.environ.get(field_name)
        if value and value.startswith('ENC:'):
            try:
                from encryption_utils import decrypt_env_password
                return decrypt_env_password(value)
            except Exception as e:
                print(f"Error decrypting {field_name}: {e}")
                return None
        return value
    
    SUPER_ADMIN_EMAIL = _decrypt_admin_field('SUPER_ADMIN_EMAIL')
    SUPER_ADMIN_USERNAME = _decrypt_admin_field('SUPER_ADMIN_USERNAME')
    SUPER_ADMIN_PASSWORD = _decrypt_admin_field('SUPER_ADMIN_PASSWORD')
    SUPER_ADMIN_FIRST_NAME = _decrypt_admin_field('SUPER_ADMIN_FIRST_NAME')
    SUPER_ADMIN_LAST_NAME = _decrypt_admin_field('SUPER_ADMIN_LAST_NAME')
