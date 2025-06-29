import pytest

from backend.src.authors.schemas import AuthorInDB
from backend.src.books.schemas import BookInDB
from backend.src.tags.schemas import TagInDB
from backend.src.volumes.schemas import VolumeInDB
from backend.src.enums import TranslationStatusEnum


@pytest.fixture
def test_book_in_db(faker):
    return BookInDB(
        book_id=faker.uuid4(),
        book_name=faker.user_name(),
        book_country=faker.country(),
        book_release_date=faker.date(),
        book_translation_status=TranslationStatusEnum.ABSENT,
        book_description=faker.text(),
    )


@pytest.fixture
def test_author_in_db(faker):
    return AuthorInDB(
        author_id=faker.uuid4(),
        author_name=faker.name().split()[0],
        author_surname=faker.name().split()[1],
    )

@pytest.fixture
def test_tag_in_db(faker):
    return TagInDB(
        tag_id=faker.uuid4(),
        tag_name=faker.name(),
    )

