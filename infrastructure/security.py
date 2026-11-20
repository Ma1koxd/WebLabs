import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()


def get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET", "")
    if len(secret) < 32 or secret.startswith("replace_"):
        raise RuntimeError("Укажите JWT_SECRET длиной не меньше 32 символов в .env")
    return secret


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm="HS256")


def read_token(token: str) -> int:
    payload = jwt.decode(
        token, get_jwt_secret(), algorithms=["HS256"], options={"require": ["exp", "sub"]}
    )
    return int(payload["sub"])
