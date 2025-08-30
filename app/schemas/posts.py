from pydantic import BaseModel, Field
from datetime import datetime


# app/schemas.py
import datetime
from pydantic import BaseModel

# This is the base Pydantic model for a post.
# It defines the fields that are common to all post-related schemas.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# This is the model for a post when a user creates it.
# It inherits from PostBase and is what FastAPI uses to validate incoming data.
class PostCreate(PostBase):
    pass

# This is the model for a post when it's sent back as a response.
# It inherits from PostBase but also includes the 'id' and 'created_at' fields.
# The 'Config' class tells Pydantic to work with SQLAlchemy models.
class PostOut(PostBase):
    id: int
    created_at: datetime.datetime


    class Config:
        orm_mode = True
