from pydantic import BaseModel, Field


class LikeResponse(BaseModel):
    post_id: int
    likes: int

class LikeCreate(BaseModel):
    username: str
    post_id: int

class LikeDelete(BaseModel):
    username: str
    post_id: int
