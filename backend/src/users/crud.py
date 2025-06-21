from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy import select

from backend.env.config import ALGORITHM, SECRET_KEY
from backend.src import status_codes
from backend.src.database import async_session_dependency
from backend.src.users.auth import (
    get_password_hash,
    oauth2_scheme,
    verify_password,
)
from backend.src.users.models import UsersModel
from backend.src.users.schemas import tokens as tokens_schemas
from backend.src.users.schemas import users as users_schemas


async def read_user(session: async_session_dependency, username: str):
    stmt = select(UsersModel).filter(UsersModel.username == username)
    result = await session.execute(stmt)
    user = result.scalars().first()
    return users_schemas.UserInDB.model_validate(user, from_attributes=True)


async def create_user(
    session: async_session_dependency, user: users_schemas.UserCreate,
):
    user.password = get_password_hash(user.password)
    new_user = UsersModel(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def authenticate_user(
    session: async_session_dependency, username: str, password: str,
):
    user = await read_user(session=session, username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def read_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: async_session_dependency,
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise status_codes.Unauthorized_401()
        token_data = tokens_schemas.TokenData(username=username)

        user = await read_user(session=session, username=token_data.username)
        if user is None:
            raise status_codes.Unauthorized_401()
    except JWTError:
        raise status_codes.Unauthorized_401()
    return user

