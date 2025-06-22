from fastapi import APIRouter

from backend.src.enums import ModulesEnum

router = APIRouter(
    prefix=f"/{ModulesEnum.USERS_BOOKS.value}",
    tags=[ModulesEnum.USERS_BOOKS],
)
