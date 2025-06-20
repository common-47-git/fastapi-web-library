from pydantic import UUID4, BaseModel, Field


class VolumeBase(BaseModel):
    book_id: UUID4
    volume_number: int
    volume_name: str = Field(max_length=50)


class VolumeCreate(VolumeBase):
    pass


class VolumeRead(VolumeBase):
    volume_id: UUID4


class VolumeUpdate(VolumeBase):
    pass


class VolumeInDB(VolumeBase):
    volume_id: UUID4
