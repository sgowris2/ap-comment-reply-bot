import bcrypt
import getpass
import os

password = getpass.getpass("Enter password: ")
pepper = os.getenv("PASSWORD_PEPPER") or getpass.getpass("Enter pepper: ")

hashed = bcrypt.hashpw(
    (password + pepper).encode(),
    bcrypt.gensalt()
).decode()

print("\nCopy this into secrets.toml:\n")
print(hashed)