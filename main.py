import os
import getpass
from auth import setup_master_password, verify_master_password
from vault import generate_key, add_entry, get_entry

def menu(key):
    while True:
        print("\nPassword Vault Menu")
        print("1. Add Entry")
        print("2. Get Entry")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            site = input("Enter site name: ")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            add_entry(site, username, password, key)

        elif choice == "2":
            site = input("Enter site name to retrieve: ")
            get_entry(site, key)

        elif choice == "3":
            print("Exiting vault.")
            break
        else:
            print("Invalid choice. Try again.")

def main():
    if not os.path.exists("master.hash"):
        print("No master password present. Set new!")
        setup_master_password()
    else:
        print("Enter the master password : ")
        if verify_master_password():
            print("Access granted!")
            master_password = getpass.getpass("Re-enter master password for vault access: ")
            key = generate_key(master_password)
            menu(key)
        else:
            print("Access denied. Exiting")

if __name__ == "__main__":
    main()
