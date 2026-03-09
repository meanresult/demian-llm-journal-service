import os
import time
import logging
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

logger = logging.getLogger(__name__)

security = HTTPBearer()

SUPABASE_JWKS_URL = os.getenv("SUPABASE_JWKS_URL")
SUPABASE_AUDIENCE = "authenticated"
_JWKS_TTL = 3600  # 1시간 캐시

_jwks_cache: dict = {"keys": None, "fetched_at": 0.0}


def _get_jwks() -> dict:
    now = time.time()
    if _jwks_cache["keys"] and now - _jwks_cache["fetched_at"] < _JWKS_TTL:
        return _jwks_cache["keys"]

    logger.info("Fetching JWKS from Supabase")
    response = requests.get(SUPABASE_JWKS_URL, timeout=5)
    response.raise_for_status()
    _jwks_cache["keys"] = response.json()
    _jwks_cache["fetched_at"] = now
    return _jwks_cache["keys"]


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        jwks = _get_jwks()
        payload = jwt.decode(
            token,
            jwks,
            algorithms=["ES256"],
            audience=SUPABASE_AUDIENCE,
        )
        return payload
    except JWTError as e:
        logger.warning("JWT validation failed: %s", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        logger.error("Auth error: %s", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
