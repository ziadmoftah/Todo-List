import datetime
import os
from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from utils import password_hashing
from sqlalchemy.orm import Session
from entities.user import User
from auth.models import UserRegister, UserLogin, Token, TokenData

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def register_user(db:Session , user: UserRegister):
    db_user = User(
        username= user.username,
        email= user.email,
        hashed_password= password_hashing.hash(user.password),
        phone_number= user.phone_number
    )
    db.add(db_user)
    db.commit()


def authenticate_user(db : Session , user : UserLogin) -> User | None:
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"No username: {user.username} was found")
    if not password_hashing.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED , detail=f"Incorrect password for username: {user.username}")
    return db_user

def create_access_token(username: str) -> str:
    encode = {
        'username' : username,
        'exp' : datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    }
    return jwt.encode(encode , os.getenv("SECRET_KEY") , algorithm=os.getenv("ALGORITHM"))

def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token , os.getenv("SECRET_KEY") , algorithms=[os.getenv("ALGORITHM")])
        username = payload.get("username")
        if not username:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
        return TokenData(username=username)
    except PyJWTError as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authentication")

def login_for_access_token( db: Session , form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(db , UserLogin(username=form_data.username , password=form_data.password))
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid Authentication")
    token = create_access_token(user.username)
    return Token(access_token=token, token_type="bearer")

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    return verify_token(token)

CurrentUser = Annotated[TokenData, Depends(get_current_user)]