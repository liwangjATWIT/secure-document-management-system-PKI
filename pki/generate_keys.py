import os
import getpass

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Define PKI directories
BASE_DIR = os.path.dirname(__file__)

PRIVATE_DIR = os.path.join(BASE_DIR, 'private')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')

def generate_user_keys(user_id, passphrase):
    
    # Create directories if they don't exist
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    
    # Define key file paths
    private_key_path = os.path.join(PRIVATE_DIR, f"user_{user_id}_private.pem")
    public_key_path = os.path.join(PUBLIC_DIR, f"user_{user_id}_public.pem")
    
    # Prevent overwriting existing keys
    if os.path.exists(private_key_path) or os.path.exists(public_key_path):
        raise FileExistsError(f"Keys for user {user_id} already exist.")
    
    # Generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=3072
    )
    
    # Obtain the public key from the private key
    public_key = private_key.public_key()
    
    # Encrypt and serialize the private key
    encrypted_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase.encode("utf-8"))
    )
    
    with open(private_key_path, "xb") as private_file:
        private_file.write(encrypted_private_key)
    
    # Serialize the public key
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(public_key_path, "xb") as public_file:
        public_file.write(public_key_bytes)
        
    print(f"Keys for user {user_id} generated successfully.")
  
# Run script to generate keys for testing  
if __name__ == "__main__":
    user_id = input("Enter user ID: ").strip()
    
    if not user_id.isdigit() or int(user_id) <= 0:
        raise ValueError("User ID must be a positive integer.")
    
    passphrase = getpass.getpass("Enter passphrase for private key encryption: ")
    
    if len(passphrase) < 8:
        raise ValueError("Passphrase must be at least 8 characters long.")
    
    confirm_passphrase = getpass.getpass("Confirm private key passphrase: ")
    
    if passphrase != confirm_passphrase:
        raise ValueError("Passphrases don't match.")
    
    generate_user_keys(int(user_id), passphrase)