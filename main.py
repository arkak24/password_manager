import os
from auth import setup_master_password, verify_master_passsword

def main():
    if not os.path.exists("master.hash"):
        print("No master password present. Set new!")
        setup_master_password()
    else:
        print("Enter the master password : ")
        if verify_master_passsword():
            print("Access granted!")
            # menu for vault here
        else:
            print("Access denied. Exiting")

if __name__ == "__main__":
    main()
