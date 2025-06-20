from pydantic import UUID4, BaseModel, Field


class ChapterBase(BaseModel):
    chapter_number: int
    chapter_name: str = Field(max_length=50)
    chapter_content: str


class ChapterCreate(ChapterBase):
    volume_id: UUID4


class ChapterRead(ChapterBase):
    volume_id: UUID4


class ChapterUpdate(ChapterBase):
    pass


class ChapterInDB(ChapterBase):
    chapter_id: UUID4
    volume_id: UUID4
