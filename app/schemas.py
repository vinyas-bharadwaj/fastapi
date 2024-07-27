from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional

class BasePost(BaseModel):
  title: str
  content: str
  published: bool = True # Default value set to be True

class CreatePost(BasePost):
  pass

class UpdatePost(BasePost):
  published: bool


class ResponseUser(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

  class Config:
    orm_mode = True

class ResponsePost(BasePost):
  id: int
  created_at: datetime
  owner_id: int
  owner: ResponseUser

  class Config: # We need to add this line since the pydantic model expects a dictionary to be returned
    # this line makes it so that pydantic converts any object into a dictionary automatically 
    orm_mode = True

class PostOut(BaseModel):
  Post: ResponsePost
  votes: int

  class Config:
    orm_mode = True

class CreateUser(BaseModel):
  email: EmailStr
  password: str

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[int] = None

class Vote(BaseModel):
  post_id: int
  dir: conint(le=1) # type: ignore