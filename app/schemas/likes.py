from pydantic import BaseModel

class LikeBase(BaseModel):
    post_id: int

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    id: int
    username: str

    class Config:
        orm_mode = True
