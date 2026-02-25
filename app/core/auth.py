from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
import os

security = HTTPBearer()

SUPABASE_JWKS_URL = os.getenv("SUPABASE_JWKS_URL")
SUPABASE_AUDIENCE = "authenticated"

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials # 실제 토큰 문자열만 추출 

    # Supabase 공개키 가져오기
    jwks = requests.get(SUPABASE_JWKS_URL).json()

    try:
        payload = jwt.decode(
            token,
            jwks,
            algorithms=["ES256"],
            audience=SUPABASE_AUDIENCE
        )
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
