from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.env.config import AuthConfig
from backend.src import http_exceptions
from backend.src.enums import ModulesEnum
from backend.src.users.schemas import tokens as tokens_schemas
from backend.src.users.schemas import users as users_schemas
from backend.src.users.services import UsersServices

router = APIRouter(
    prefix=f"/{ModulesEnum.USERS.value}",
    tags=[ModulesEnum.USERS],
)


@router.post(
    "/login",
    response_model=tokens_schemas.Token,
    summary="Log in to get a token.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        401: http_exceptions.Unauthorized401().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> tokens_schemas.Token:
    """Log in by OAuth2PasswordRequestForm credentials and get a token."""
    user = await UsersServices().authenticate_user(
        user_to_auth=users_schemas.UserAuth(
            username=form_data.username,
            password=form_data.password,
        ),
    )
    access_token_expires = timedelta(
        minutes=AuthConfig().ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = UsersServices().create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return tokens_schemas.Token(access_token=access_token, token_type="bearer")


@router.post(
    "/add",
    response_model=users_schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user.",
    responses={
        201: http_exceptions.Created201().get_response_body(),
        409: http_exceptions.Conflict409().get_response_body(),
    },
)
async def post_user(
    user: users_schemas.UserCreate,
):
    """Create a user with properties specified in given schema."""
    return await UsersServices().create_user(user=user)


@router.get(
    "/me",
    response_model=users_schemas.UserRead,
    summary="Get current user.",
    responses={
        200: http_exceptions.OK200().get_response_body(),
        404: http_exceptions.NotFound404().get_response_body(),
    },
)
async def get_me(
    current_user: Annotated[
        users_schemas.UserRead,
        Depends(UsersServices().read_current_user),
    ],
) -> users_schemas.UserRead:
    """Get current user as a user schema."""
    return current_user
