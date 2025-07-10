from datetime import date

from pydantic import UUID4, BaseModel, Field

from backend.src.authors import schemas as authors_schemas
from backend.src.enums import TranslationStatusEnum
from backend.src.tags import schemas as tags_schemas


class BookBase(BaseModel):
    book_name: str = Field(min_length=2, max_length=50)
    book_country: str | None = Field(default=None, min_length=2, max_length=50)
    book_release_date: date | None = None
    book_translation_status: TranslationStatusEnum = (
        TranslationStatusEnum.ABSENT
    )
    book_description: str | None = Field(default=None, min_length=2, max_length=1500)
    book_cover: str = Field(
        default="https://ranobehub.org/img/ranobe/posters/default.jpg",
        max_length=500,
    )


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    book_id: UUID4


class BookUpate(BookBase):
    book_id: UUID4


class BookDelete(BookBase):
    book_id: UUID4


class BookInDB(BookBase):
    book_id: UUID4


class BookFullInfo(BookBase):
    book_id: UUID4
    book_tags: list[tags_schemas.TagRead] | None
    book_authors: list[authors_schemas.AuthorRead] | None
    book_shelf: str | None
