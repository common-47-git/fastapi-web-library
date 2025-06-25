from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt

from backend.env import auth_config
from backend.src import http_exceptions
from backend.src.users.auth import (
    get_password_hash,
    oauth2_scheme,
    verify_password,
)
from backend.src.users.models import UsersModel
from backend.src.users.repository import UsersRepository
from backend.src.users.schemas import tokens as tokens_schemas
from backend.src.users.schemas import users as users_schemas


async def create_user(
    user: users_schemas.UserCreate,
) -> UsersModel:
    user.password = get_password_hash(user.password)
    return await UsersRepository().create_one(pydantic_schema=user)


async def authenticate_user(
    user_to_auth: users_schemas.UserAuth,
) -> UsersModel | None:
    authed_user = await UsersRepository().read_one_by_property(
        property_name=UsersModel.username.key,
        property_value=user_to_auth.username,
    )
    if not verify_password(user_to_auth.password, authed_user.password):
        return None
    return authed_user


async def read_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UsersModel:
    try:
        payload = jwt.decode(
            token, auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM],
        )
        username = payload.get("sub")
        if username is None:
            raise http_exceptions.Unauthorized401
        token_data = tokens_schemas.TokenData(username=username)

        user = await UsersRepository().read_one_by_property(
            property_name=UsersModel.username.key,
            property_value=token_data.username,
        )
        if user is None:
            raise http_exceptions.Unauthorized401
    except JWTError as jwt_e:
        raise http_exceptions.Unauthorized401 from jwt_e
    return user
