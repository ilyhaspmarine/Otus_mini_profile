from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=100)
    lastName: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=12, max_length=12)

class UserCreate(UserBase):
    username: str = Field(..., min_length=1, max_length=100)

class UserUpdate(UserBase):
    pass

class User(UserCreate):

    class Config:
        from_attributes = True