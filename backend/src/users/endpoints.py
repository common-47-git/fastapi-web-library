from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from env.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src import status_codes
from src.database import async_session_dependency
from src.users.auth import create_access_token
from src.users.crud import (
    authenticate_user,
    create_user,
    read_current_user,
)
from src.users.schemas import tokens as tokens_schemas
from src.users.schemas import users as users_schemas

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: async_session_dependency,
) -> tokens_schemas.Token:
    user = await authenticate_user(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    if not user:
        raise status_codes.Unauthorized_401()
    return tokens_schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/add", response_model=users_schemas.UserRead)
async def users_add(
    session: async_session_dependency,
    user: users_schemas.UserCreate,
):
    try:
        user = await create_user(session=session, user=user)
    except IntegrityError as e:
        raise status_codes.Conflict_409(exception=e)
    else:
        return user


@router.get("/me", response_model=users_schemas.UserRead)
async def users_me(
    current_user: Annotated[
        users_schemas.UserRead,
        Depends(read_current_user),
    ],
) -> users_schemas.UserRead:
    return current_user

