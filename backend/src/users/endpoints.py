from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from backend.env import auth_config
from backend.src import http_exceptions
from backend.src.enums import ModulesEnum
from backend.src.users.models import UsersModel
from backend.src.users.schemas import tokens as tokens_schemas
from backend.src.users.schemas import users as users_schemas
from backend.src.users.services import UsersServices

router = APIRouter(
    prefix=f"/{ModulesEnum.USERS.value}",
    tags=[ModulesEnum.USERS],
)


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> tokens_schemas.Token:
    user = await UsersServices().authenticate_user(
        user_to_auth=users_schemas.UserAuth(
            username=form_data.username,
            password=form_data.password,
        ),
    )
    if not user:
        raise http_exceptions.Unauthorized401

    access_token_expires = timedelta(
        minutes=auth_config.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = UsersServices().create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return tokens_schemas.Token(access_token=access_token, token_type="bearer")


@router.post(
    "/add",
    response_model=users_schemas.UserRead,
    summary="Create a user.",
)
async def users_add(
    user: users_schemas.UserCreate,
) -> UsersModel:
    """Create a user with properties specified in given schema."""
    try:
        new_user = await UsersServices().create_user(user=user)
    except IntegrityError as e:
        raise http_exceptions.Conflict409(exception=e) from e
    else:
        return new_user


@router.get(
    "/me",
    response_model=users_schemas.UserRead,
    summary="Get current user.",
)
async def users_me(
    current_user: Annotated[
        users_schemas.UserRead,
        Depends(UsersServices().read_current_user),
    ],
) -> users_schemas.UserRead:
    """Get current user as a user schema."""
    return current_user
