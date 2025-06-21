from enum import Enum


class ModulesEnum(str, Enum):
    AUTHORS = "authors"
    BOOKS = "books"
    BOOKS_AUTHORS = "books_authors"
    BOOKS_TAGS = "books_tags"
    CHAPTERS = "chapters"
    TAGS = "tags"
    USERS = "users"
    USERS_BOOKS = "users_books"
    VOLUMES = "volumes"


class TranslationStatusEnum(Enum):
    TRANSLATED = "Translated"
    IN_PROGRESS = "In progress"
    ABANDONED = "Abandoned"
    ABSENT = "Absent"


class BookShelfEnum(str, Enum):
    READING = "Reading"
    HAVE_READ = "Have read"
    TO_READ = "To read"
    FAVORITES = "Favorites"
