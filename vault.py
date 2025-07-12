import os
import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

VAULT_FILE = "vault.dat"

def generate_key(master_password: str) -> bytes:
    password_bytes = master_password.encode()

    salt = b'\x13\x11\x99\xd7\xf4\xab\x12\xcd\xef\x11\xac\x98\xde\xad\xbe\xef'

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # type of hashing to be performed
        length=32,  # length of the output key(string)
        salt=salt,
        iterations=100_000, # number of times the hashing algorithm to apply
        backend=default_backend()   # engine to process all this
    )

    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key

def load_vault(key: bytes) -> dict:
    if not os.path.exists(VAULT_FILE):
        return {} 
    with open(VAULT_FILE, "rb") as f:
        encrypted_data = f.read()

    try:
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_data)
        vault_data = json.loads(decrypted.decode())
        return vault_data
    except Exception as e:
        print("Failed to decrypt vault. Wrong password or file corrupted.")
        return {}

def save_vault(vault_data: dict, key: bytes):
    try:
        fernet = Fernet(key)
        json_data = json.dumps(vault_data).encode()
        encrypted_data = fernet.encrypt(json_data)

        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted_data)
    except Exception as e:
        print("Failed to save vault:", str(e))

def add_entry(site: str, username: str, password: str, key: bytes):
    vault = load_vault(key)
    vault[site] = [username, password]
    save_vault(vault, key)
    print(f"Entry for '{site}' added successfully.")

def get_entry(site: str, key: bytes):
    vault = load_vault(key)
    if site in vault:
        username, password = vault[site]
        print(f"Site: {site}")
        print(f"Username: {username}")
        print(f"Password: {password}")
    else:
        print(f"No entry found for site: {site}")