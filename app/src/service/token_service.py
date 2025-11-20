from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.src.db.model import User
from app.src.utils.password_util import verify_password
from app.src.jwt.jwt_handler import create_access_token
from app.src.schema.token_schema import LoginRequest


def authenticate_user(db: Session, payload: LoginRequest):
    user = db.query(User).filter(User.username == payload.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )
    
    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    token = create_access_token(
        data={"id": user.id, "usn": user.username, "role": user.role}
    )

    return token
