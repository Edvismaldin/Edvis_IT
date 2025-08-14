from pydantic import BaseModel


class RoomBase(BaseModel):
	name: str
	capacity: int
	location: str | None = None
	resources: str | None = None
	is_active: bool = True


class RoomCreate(RoomBase):
	pass


class RoomRead(RoomBase):
	id: int

	class Config:
		from_attributes = True