from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.src.db.database import get_db
from app.src.schema.user_schema import UserCreate, UserUpdate, UserResponse
from app.src.schema.response_schema import ApiResponse
from app.src.service.user_service import (
    create_user,
    get_user,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["User Management"])


# create new user (register)
@router.post("/", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def create(payload: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, payload)

    return ApiResponse.success(
        data=UserResponse.model_validate(user),
        message="User created successfully",
        status_code=status.HTTP_201_CREATED,
    )


# get a user by id
@router.get("/{id}", response_model=ApiResponse)
def get(id: int, db: Session = Depends(get_db)):
    user = get_user(db, id)

    return ApiResponse.success(
        UserResponse.model_validate(user), "User retrieved successfully"
    )


# update user
@router.put("/{id}", response_model=ApiResponse)
def update(id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, id, payload)
    
    return ApiResponse.success(
        UserResponse.model_validate(user), "User updated successfully"
    )


# delete a user
@router.delete("/{id}", response_model=ApiResponse)
def delete(id: int, db: Session = Depends(get_db)):
    user = delete_user(db, id)

    return ApiResponse.success(
        UserResponse.model_validate(user), "User deleted successfully"
    )
