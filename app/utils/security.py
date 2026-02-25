# utils/security.py

from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(
    memory_cost=65536,
    time_cost=4,
    parallelism=2,
    hash_len=64,
    type=Type.ID
)

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(hash: str, password: str) -> bool:
    try:
        return ph.verify(hash, password)
    except VerifyMismatchError:
        return False

def needs_rehash(hash: str) -> bool:
    return ph.check_needs_rehash(hash)