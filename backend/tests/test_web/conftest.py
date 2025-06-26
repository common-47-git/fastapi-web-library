import uuid
from datetime import date

import pytest

from backend.src.authors.schemas import AuthorInDB
from backend.src.books.schemas import BookInDB
from backend.src.enums import TranslationStatusEnum


@pytest.fixture
def test_book_in_db():
    return BookInDB(
        book_id=uuid.UUID("80be17fa-afd8-4b0c-ac5d-a4a5c8eae8a5"),
        book_name="testbook",
        book_country="TESTCOUNTRY",
        book_release_date=date.today(),
        book_translation_status=TranslationStatusEnum.ABSENT,
        book_description="test description.",
    )


@pytest.fixture
def test_author_in_db():
    return AuthorInDB(
        author_id=uuid.UUID("80be18fa-afd8-4b0c-ac5d-a4a5c8eae8a5"),
        author_name="Testname",
        author_surname="Testsurname",
    )
