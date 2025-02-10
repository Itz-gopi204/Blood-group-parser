import os
import uuid
from functools import wraps
from flask import request, jsonify
from config import Config
from cryptography.fernet import Fernet

# Initialize an encryption key (In production, securely store and load this key)
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

def token_required(f):
    """
    Decorator to enforce token-based authentication.
    Expects a header 'x-access-token' with a token matching the SECRET_KEY.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token or token != Config.SECRET_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

def secure_store(file, filename):
    """
    Securely store the uploaded file.
    - Generates a unique filename.
    - Saves the file in the configured upload folder.
    - Optionally encrypts the file content (demonstrative encryption shown).
    Returns the path to the stored file.
    """
    secure_filename = str(uuid.uuid4()) + "_" + filename
    file_path = os.path.join(Config.UPLOAD_FOLDER, secure_filename)
    
    # Ensure upload folder exists
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
    
    # Save the file
    file.save(file_path)
    
    # Read and encrypt the file content (for demonstration purposes)
    with open(file_path, "rb") as f:
        file_data = f.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path, "wb") as f:
        f.write(encrypted_data)
    
    # For processing, immediately decrypt (in production, decrypt only when needed)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(file_path, "wb") as f:
        f.write(decrypted_data)
    
    return file_path
