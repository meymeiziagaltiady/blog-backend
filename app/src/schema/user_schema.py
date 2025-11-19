from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., example="example_user")
    role: str = Field(..., example="user")


class UserCreate(UserBase):
    password: str = Field(..., example="example_pass123")
    role: Optional[str] = Field("user", example="user")


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, example="new_username")
    password: Optional[str] = Field(None, example="new_pass")
    role: Optional[str] = Field(None, example="admin")


class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True
