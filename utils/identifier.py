import hashlib
from datetime import datetime

def genHash(value, length):
    s = str(value) + str(datetime.now().timestamp())
    return hashlib.shake_256(s.encode('utf-8')).hexdigest(length//2)
