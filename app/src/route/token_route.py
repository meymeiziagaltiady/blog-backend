from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.src.db.database import get_db
from app.src.schema.token_schema import TokenResponse
from app.src.schema.token_schema import LoginRequest
from app.src.service.token_service import authenticate_user

router = APIRouter(tags=["Authentication"])


@router.post("/token", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    access_token = authenticate_user(db, payload)
    return TokenResponse(access_token=access_token, token_type="bearer")
