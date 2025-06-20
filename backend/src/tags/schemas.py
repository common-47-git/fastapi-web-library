from pydantic import UUID4, BaseModel, Field


class TagBase(BaseModel):
    tag_name: str = Field(max_length=50)


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    tag_id: UUID4


class TagUpdate(TagBase):
    pass


class TagDelete(TagBase):
    pass


class TagInDB(TagBase):
    tag_id: UUID4
