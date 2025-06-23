from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy import select

from backend.env.config import ALGORITHM, SECRET_KEY
from backend.src import http_exceptions
from backend.src.database import async_session_dependency
from backend.src.users.auth import (
    get_password_hash,
    oauth2_scheme,
    verify_password,
)
from backend.src.users.models import UsersModel
from backend.src.users.schemas import tokens as tokens_schemas
from backend.src.users.schemas import users as users_schemas


async def read_user_by_username(
    session: async_session_dependency,
    username: str,
) -> UsersModel | None:
    stmt = select(UsersModel).filter(UsersModel.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_user(
    session: async_session_dependency,
    user: users_schemas.UserCreate,
) -> UsersModel:
    user.password = get_password_hash(user.password)
    new_user = UsersModel(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def authenticate_user(
    session: async_session_dependency,
    username: str,
    password: str,
) -> UsersModel | None:
    user = await read_user_by_username(session=session, username=username)
    if not verify_password(password, user.password):
        return None
    return user


async def read_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: async_session_dependency,
) -> UsersModel:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise http_exceptions.Unauthorized401
        token_data = tokens_schemas.TokenData(username=username)

        user = await read_user_by_username(session=session, username=token_data.username)
        if user is None:
            raise http_exceptions.Unauthorized401
    except JWTError as jwt_e:
        raise http_exceptions.Unauthorized401 from jwt_e
    return user
