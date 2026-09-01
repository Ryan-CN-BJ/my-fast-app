from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, Argon2Error
from datetime import datetime, timedelta, timezone
import jwt
import uuid


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


def create_token(data: dict, secret_key: str, *, expire_delta: timedelta | None = None):
    payload = data.copy()
    if "sub" in payload and not isinstance(payload["sub"], str):
        payload["sub"] = str(payload["sub"])

    now = datetime.now(timezone.utc)
    payload.update(
        {
            "jti": str(uuid.uuid4()),
            "iat": now,
            "exp": now + (expire_delta or timedelta(hours=2)),
        }
    )

    return jwt.encode(payload=payload, key=secret_key, algorithm="HS256")


def verify_token(token: str, secret_key: str):
    return jwt.decode(token, key=secret_key, algorithms=["HS256"])
