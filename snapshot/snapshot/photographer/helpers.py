from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


# this func returns hashed password using argon2
def hash_pass(password):
    ph = PasswordHasher()
    return ph.hash(password)


# this func checks correctness of password with hashed val
def is_password(password, hashed):
    ph = PasswordHasher()
    try:
        if ph.verify(hashed, password):
            return True
        return False
    except VerifyMismatchError:
        return False
