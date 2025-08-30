from pydantic import BaseModel, Field
from datetime import datetime, timezone

# User Schemas
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    # The 'id' field is now an integer to match the database
    id: int
    joined_at: datetime

    class Config:
        from_attributes = True

# Pydantic model for the JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str
