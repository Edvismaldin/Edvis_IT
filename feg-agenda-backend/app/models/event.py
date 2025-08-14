from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Event(Base):
	__tablename__ = "events"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	title: Mapped[str] = mapped_column(String(255), nullable=False)
	description: Mapped[str] = mapped_column(String(1024), nullable=True)
	room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False, index=True)
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
	start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
	end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
	status: Mapped[str] = mapped_column(String(30), default="confirmed", nullable=False)

	room = relationship("Room")
	owner = relationship("User")