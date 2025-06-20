from enum import Enum


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
