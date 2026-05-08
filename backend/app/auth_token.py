"""Signed bearer tokens for API auth when cross-site session cookies are blocked."""

from typing import Optional

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

SALT = "drift-api-bearer"
MAX_AGE_SEC = 60 * 60 * 24 * 14  # 14 days


def issue_token(secret_key: str, user_id: int) -> str:
    s = URLSafeTimedSerializer(secret_key, salt=SALT)
    return s.dumps({"u": int(user_id)})


def verify_token(secret_key: str, token: Optional[str]) -> Optional[int]:
    if not token or not secret_key:
        return None
    s = URLSafeTimedSerializer(secret_key, salt=SALT)
    try:
        data = s.loads(token, max_age=MAX_AGE_SEC)
        return int(data["u"])
    except (BadSignature, SignatureExpired, KeyError, TypeError, ValueError):
        return None
