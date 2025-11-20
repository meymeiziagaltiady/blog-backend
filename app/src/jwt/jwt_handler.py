from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer

from app.src.config.config import settings
from app.src.schema.jwt_schema import JwtUserData

bearer_scheme = HTTPBearer()


def create_access_token(*, data: dict, expires_minutes: int | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    # decode and verify token
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid or expired",
        )


def get_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid token",
        )

    return auth_header.replace("Bearer ", "")


def get_user_data(token: str) -> JwtUserData:
    payload = decode_token(token)

    try:
        user_id = payload.get("id")
        username = payload.get("usn")
        role = payload.get("role")

        if user_id is None or username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token missing required fields",
            )

        return JwtUserData(id=user_id, username=username, role=role)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JWT payload structure",
        )
