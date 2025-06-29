from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from auth import services
from auth.models import UserRegister
from database.core import DbSession

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)

@router.post("/" , status_code=HTTP_201_CREATED)
def register_user(db: DbSession, user: UserRegister):
    return services.register_user(db , user)

@router.post("/token" , status_code=HTTP_200_OK)
def login_user(db: DbSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return services.login_for_access_token(db, form_data)