from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    password: str
    phone_number: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str