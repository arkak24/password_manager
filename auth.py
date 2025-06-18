import bcrypt
import getpass

HASH_FILE = "master.hash"

def setup_master_password():
    while True:
        password = getpass.getpass("Set your master password : ")
        confirm = getpass.getpass("Confirm your master password : ")
        if password == confirm:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            with open(HASH_FILE, "wb") as f:
                f.write(hashed)
            print("Master password set and saved securely.")
            break
        else:
            print("Password dont match, try again!\n")

def verify_master_password():
    try:
        with open(HASH_FILE, "rb") as f:
            stored_hash = f.read()

        password = getpass.getpass("Enter your master password : ")
        if bcrypt.checkpw(password.encode(), stored_hash):
            return True
        else:
            return False
    except FileNotFoundError:
        print("Error : File not found.")
        return False
