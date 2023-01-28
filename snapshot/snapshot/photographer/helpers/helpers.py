from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jwt import encode

from django.conf import settings


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


# return jwt token for logging in
def login_photographer(user):
    payload = {
        'id': user.id,
        'email': user.email,
        'photographer': True,
    }
    return encode(payload, settings.SECRET_KEY, algorithm='HS256')
