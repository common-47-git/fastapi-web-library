from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.authors.endpoints import router as authors_router
from src.books.endpoints import router as books_router
from src.books_authors.endpoints import router as books_authors_router
from src.books_tags.endpoints import router as books_tags_router
from src.chapters.endpoints import router as chapters_router
from src.tags.endpoints import router as tags_router
from src.users.endpoints import router as users_router
from src.volumes.endpoints import router as volumes_router

app = FastAPI(title="Books site")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app.include_router(books_router)
app.include_router(authors_router)
app.include_router(books_authors_router)
app.include_router(tags_router)
app.include_router(books_tags_router)
app.include_router(volumes_router)
app.include_router(chapters_router)
app.include_router(users_router)
