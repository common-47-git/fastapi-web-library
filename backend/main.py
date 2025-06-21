from fastapi import FastAPI

from backend import middleware
from backend.src.authors.endpoints import router as authors_router
from backend.src.books.endpoints import router as books_router
from backend.src.books_authors.endpoints import router as books_authors_router
from backend.src.books_tags.endpoints import router as books_tags_router
from backend.src.chapters.endpoints import router as chapters_router
from backend.src.tags.endpoints import router as tags_router
from backend.src.users.endpoints import router as users_router
from backend.src.volumes.endpoints import router as volumes_router
from frontend import main as frontend_main

app = FastAPI(title="Books site")

middleware.add_middlewares(app)

app.include_router(books_router)
app.include_router(authors_router)
app.include_router(books_authors_router)
app.include_router(tags_router)
app.include_router(books_tags_router)
app.include_router(volumes_router)
app.include_router(chapters_router)
app.include_router(users_router)


frontend_main.init(app)
