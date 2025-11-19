from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="admin123")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
