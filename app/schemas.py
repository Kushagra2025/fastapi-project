from pydantic import BaseModel, EmailStr
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class Post_response(Post):
    id: int
    # created_at: datetime

    # So, basically we get the response back in the from of SQl_Alchemy model (sice the response comes from db).
    # Therefore this piece of code converts he sql_alchemy model back to pydantic model so that the schema validation can take place.
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class ConfigDict:
        from_attributes = True