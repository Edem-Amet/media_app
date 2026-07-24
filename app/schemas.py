from pydantic import BaseModel, EmailStr
from datetime import datetime


# ======================
# User Schemas
# ======================

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str



# ======================
# Post Schemas
# ======================


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True



class PostOut(BaseModel):
    title: str
    content: str
    published: bool
    owner: UserOut
    owner_id: int


    class Config:
        from_attributes = True