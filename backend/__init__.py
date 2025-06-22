"""Backend part of the app. Consists entire business logic."""

from fastapi import APIRouter

from backend.src.authors.endpoints import router as authors_router
from backend.src.books.endpoints import router as books_router
from backend.src.books_authors.endpoints import router as books_authors_router
from backend.src.books_tags.endpoints import router as books_tags_router
from backend.src.chapters.endpoints import router as chapters_router
from backend.src.tags.endpoints import router as tags_router
from backend.src.users.endpoints import router as users_router
from backend.src.volumes.endpoints import router as volumes_router

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
headers = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
]

main_router = APIRouter()
main_router.include_router(books_router)
main_router.include_router(authors_router)
main_router.include_router(books_authors_router)
main_router.include_router(tags_router)
main_router.include_router(books_tags_router)
main_router.include_router(volumes_router)
main_router.include_router(chapters_router)
main_router.include_router(users_router)
