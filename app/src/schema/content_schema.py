from pydantic import BaseModel, Field
from typing import Optional


class ContentBase(BaseModel):
    title: str = Field(..., example="Blog Title")
    body: str = Field(..., example="Blog body")


class ContentCreate(ContentBase):
    pass


class ContentUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Updated title")
    body: Optional[str] = Field(None, example="Updated body")


class ContentResponse(ContentBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
