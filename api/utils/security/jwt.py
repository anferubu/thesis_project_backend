"""
Defines the JWT utilities (token creation and decoding).

It includes:
  - create_access_token()
  - create_refresh_token()
  - create_confirmation_token()
  - create_reset_password_token()
  - decode_token()

"""

from datetime import datetime, timedelta, UTC

from jose import jwt

from api.utils.security.hashing import ALGORITHM, SECRET_KEY



ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7   # 7 días
CONFIRMATION_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 día
RESET_PASSWORD_TOKEN_EXPIRE_MINUTES = 60



def _create_token(sub:str, expires_delta:timedelta) -> str:
    """
    Create a JWT token.

    Args:
      - sub (str): The user's identifier (email) to encode in the token.
      - expires_delta (timedelta): The duration for which the token is valid.

    Returns:
      - str: The encoded JWT token.
    """

    expire = datetime.now(UTC) + expires_delta
    to_encode = {"sub": sub, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def create_access_token(sub:str) -> str:
    """Create a JWT access token for authenticating API requests."""

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(sub, expires)



def create_refresh_token(sub:str) -> str:
    """Create a JWT refresh token for obtaining new access tokens."""

    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return _create_token(sub, expires)



def create_confirmation_token(sub:str) -> str:
    """Create a JWT confirmation token for confirming user accounts."""

    expires = timedelta(minutes=CONFIRMATION_TOKEN_EXPIRE_MINUTES)
    return _create_token(sub, expires)



def create_reset_password_token(sub:str) -> str:
    """Create a JWT reset password token for resetting user passwords."""

    expires = timedelta(minutes=RESET_PASSWORD_TOKEN_EXPIRE_MINUTES)
    return _create_token(sub, expires)



def decode_token(token: str) -> dict:
    """Decode a JWT token and return its payload as a dictionary."""

    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
