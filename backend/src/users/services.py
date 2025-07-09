from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from backend.env.config import AuthConfig
from backend.src import http_exceptions
from backend.src.services import BaseServices
from backend.src.users.models import UsersModel
from backend.src.users.repository import UsersRepository
from backend.src.users.schemas import tokens as tokens_schemas
from backend.src.users.schemas import users as users_schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class UsersServices(BaseServices):
    alchemy_model: type[UsersModel] = UsersModel
    repository: type[UsersRepository] = UsersRepository

    async def create_user(
        self,
        user: users_schemas.UserCreate,
    ):
        try:
            user.password = self._get_password_hash(user.password)
            new_alchemy_object = UsersModel(
                **user.model_dump(),
            )
            return await UsersRepository().create_one(
                alchemy_object=new_alchemy_object,
            )
        except IntegrityError as e:
            raise http_exceptions.Conflict409(exception=e) from e

    async def authenticate_user(
        self,
        user_to_auth: users_schemas.UserAuth,
    ) -> UsersModel:
        user = await UsersRepository().read_one_by_property(
            property_name=UsersModel.username.key,
            property_value=user_to_auth.username,
        )

        if not user:
            raise http_exceptions.NotFound404

        if not self._verify_password(
            user_to_auth.password,
            user.password,
        ):
            raise http_exceptions.Unauthorized401
        return user

    async def read_current_user(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UsersModel:
        try:
            payload = jwt.decode(
                token,
                AuthConfig().SECRET_KEY,
                algorithms=[AuthConfig().ALGORITHM],
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
        except ExpiredSignatureError as jwt_expired_e:
            raise http_exceptions.Unauthorized401(jwt_expired_e) from jwt_expired_e
        except JWTError as jwt_e:
            raise http_exceptions.Unauthorized401(jwt_e) from jwt_e
        return user

    def _verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            AuthConfig().SECRET_KEY,
            algorithm=AuthConfig().ALGORITHM,
        )
