from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# --------------------------------------------------
# Password Hashing
# --------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# --------------------------------------------------
# Hash Password
# --------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    """
    return pwd_context.hash(password)


# --------------------------------------------------
# Verify Password
# --------------------------------------------------

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a password against its hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# --------------------------------------------------
# Create JWT Access Token
# --------------------------------------------------

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):
    """
    Create a JWT access token.
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


# --------------------------------------------------
# Decode JWT Token
# --------------------------------------------------

def decode_access_token(token: str):
    """
    Decode and validate a JWT token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None