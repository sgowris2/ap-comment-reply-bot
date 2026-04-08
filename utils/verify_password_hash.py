import bcrypt

password = "your_password_here"
PEPPER = "your_pepper_here"

stored_hash = "your_stored_hash_here"

print(bcrypt.checkpw(
    (password + PEPPER).encode(),
    stored_hash.strip().encode()
))