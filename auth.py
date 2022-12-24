from flask_api import bcrypt


def hash_password(password: str):
    password = password.encode()
    hashed = bcrypt.generate_password_hash(password)
    return hashed.decode()
