from fastapi import Header, HTTPException, status
from Configurations_Settings.authorization_config import BEARER_TOKEN


def verify_bearer_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Missing Bearer token.",
        )
    token = authorization.split("Bearer ")[1]
    if token != BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token.",
        )
