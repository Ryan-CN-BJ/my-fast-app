from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, Argon2Error


class PasswordService:
    def __init__(self):
        self.ph = PasswordHasher()

    def hash_password(self, password):
        return self.ph.hash(password)

    def verify_password(self, hashed: str, password: str) -> bool:
        try:
            self.ph.verify(hashed, password)
            return True
        except VerifyMismatchError:
            return False
        except Argon2Error:
            return False
