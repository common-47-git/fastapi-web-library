from pydantic import UUID4, BaseModel, Field


class VolumeBase(BaseModel):
    book_id: UUID4
    volume_number: int = Field(ge=0)
    volume_name: str = Field(min_length=2, max_length=50)


class VolumeCreate(VolumeBase):
    pass


class VolumeRead(VolumeBase):
    volume_id: UUID4


class VolumeUpdate(VolumeBase):
    pass


class VolumeInDB(VolumeBase):
    volume_id: UUID4
