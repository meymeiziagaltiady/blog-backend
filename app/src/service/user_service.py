from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.src.db.model import User
from app.src.utils.password_util import hash_password
from app.src.schema.user_schema import UserCreate, UserUpdate


def create_user(db: Session, payload: UserCreate):
    # check whether new usn is already used
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    # insert new user
    user = User(username=payload.username, password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_user_by_username(db: Session, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")

    return user


def update_user(db: Session, id: int, payload: UserUpdate):
    user = get_user(db, id)

    # update username
    if payload.username:
        user.username = payload.username

    # update password
    if payload.password:
        user.password = hash_password(payload.password)

    # update role
    if payload.role:
        user.role = payload.role

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, id: int):
    user = get_user(db, id)
    db.delete(user)
    db.commit()

    return user
