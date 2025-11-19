from pydantic import BaseModel
from typing import Optional


class JwtUserData(BaseModel):
    id: int
    username: str
    role: str
