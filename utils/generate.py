import random as r
import string as s

def generatePassword(len):
    if len <= 0:
        raise ValueError("Password length must be greater than 0")
    return ''.join(r.choice(s.ascii_letters + s.digits + s.punctuation ) for _ in range(len))
