from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

MAX_BCRYPT_LENGTH = 72

def _normalize_password(password: str) -> str:
    if len(password.encode("utf-8")) > MAX_BCRYPT_LENGTH:
        return password.encode("utf-8")[:MAX_BCRYPT_LENGTH].decode("utf-8", errors="ignore")
    return password

def hash_password(password: str) -> str:
    password = _normalize_password(password)
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    password = _normalize_password(password)
    return pwd_context.verify(password, hashed_password)
