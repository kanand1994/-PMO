#!/usr/bin/env python3
"""
Encryption utilities for sensitive data
"""

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordEncryption:
    def __init__(self, master_key=None):
        """Initialize encryption with a master key"""
        if master_key is None:
            # Use a combination of SECRET_KEY and a fixed salt for consistency
            master_key = os.getenv('SECRET_KEY', 'plan-my-outings-secret-key-2025')
        
        # Create a key from the master key
        salt = b'plan_my_outings_salt_2025'  # Fixed salt for consistency
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        self.cipher_suite = Fernet(key)
    
    def encrypt_password(self, password):
        """Encrypt a password"""
        try:
            encrypted_password = self.cipher_suite.encrypt(password.encode())
            return base64.urlsafe_b64encode(encrypted_password).decode()
        except Exception as e:
            print(f"Error encrypting password: {e}")
            return None
    
    def decrypt_password(self, encrypted_password):
        """Decrypt a password"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_password.encode())
            decrypted_password = self.cipher_suite.decrypt(encrypted_bytes)
            return decrypted_password.decode()
        except Exception as e:
            print(f"Error decrypting password: {e}")
            return None

def encrypt_env_password():
    """Utility function to encrypt the current password in .env"""
    from dotenv import load_dotenv
    load_dotenv()
    
    current_password = os.getenv('MAIL_PASSWORD')
    if not current_password:
        print("No MAIL_PASSWORD found in .env file")
        return
    
    # Check if already encrypted (starts with 'ENC:')
    if current_password.startswith('ENC:'):
        print("Password is already encrypted")
        return
    
    encryptor = PasswordEncryption()
    encrypted = encryptor.encrypt_password(current_password)
    
    if encrypted:
        print(f"Original password: {current_password}")
        print(f"Encrypted password: ENC:{encrypted}")
        print("\nReplace MAIL_PASSWORD in .env with:")
        print(f"MAIL_PASSWORD=ENC:{encrypted}")
        return f"ENC:{encrypted}"
    else:
        print("Failed to encrypt password")
        return None

def decrypt_env_password(encrypted_password):
    """Utility function to decrypt password from .env"""
    if not encrypted_password.startswith('ENC:'):
        # Not encrypted, return as is
        return encrypted_password
    
    # Remove 'ENC:' prefix
    encrypted_data = encrypted_password[4:]
    
    encryptor = PasswordEncryption()
    decrypted = encryptor.decrypt_password(encrypted_data)
    
    return decrypted

if __name__ == "__main__":
    # Test the encryption
    encrypt_env_password()