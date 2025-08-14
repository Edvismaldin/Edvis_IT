from datetime import datetime
from pydantic import BaseModel, model_validator


class EventBase(BaseModel):
	title: str
	description: str | None = None
	room_id: int
	start_time: datetime
	end_time: datetime
	status: str = "confirmed"

	@model_validator(mode="after")
	def validate_time_range(self):
		if self.end_time <= self.start_time:
			raise ValueError("end_time must be after start_time")
		return self


class EventCreate(EventBase):
	pass


class EventRead(EventBase):
	id: int
	owner_id: int

	class Config:
		from_attributes = True