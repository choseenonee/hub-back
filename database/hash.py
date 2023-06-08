import bcrypt


def get_hashed_password(password: str):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode()


def check_hash_password(password: str, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())